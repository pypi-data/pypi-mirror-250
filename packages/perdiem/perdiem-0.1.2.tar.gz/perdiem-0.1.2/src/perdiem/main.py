from datetime import date, timedelta
from pathlib import Path
import re
import sqlite3

con = sqlite3.connect(
    Path(__file__).resolve().parent / "perdiem.db", check_same_thread=False
)


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


con.row_factory = dict_factory
cur = con.cursor()


class PerDiem:
    """The main class

    Examples::

        from perdiem import PerDiem
        rates = PerDiem.get_rates("CO")
        print(rates)
    """

    def parse_lookup(lookup: str) -> dict:
        """Parse a lookup string and return a dict with zipcode, state, or location

        Args:
            lookup: The string to parse

        Returns:
            A dict with a zipcode key-value pair, or a state and optional location key-value pair
        """

        # Check for Zip Code lookup
        m = re.match(r"^\d{5}$", lookup)
        if m:
            return {"zipcode": m.group(0)}

        # Check for State only lookup
        m = re.match(r"\w{2}$", lookup)
        if m:
            return {"state": m.group(0)}

        # Look for a comma and split on it
        m = re.split(r",\s?", lookup)

        # If there's a comma and the string *after* the comma is a state code
        # Return the state and location
        if len(m) == 2 and re.match(r"^\w{2}$", m[1]):
            return dict(state=m[1], location=m[0])

        # Otherwise, yikes
        return None

    @classmethod
    def get_rates(cls, lookup: str):
        """Get the Per Diem Rates from the database by looking up a location

        Args:
            lookup: A string representing either a zip code or a named location

        Returns:
            A list of dicts
        """
        parsed = cls.parse_lookup(lookup)
        if not parsed:
            raise ValueError("Invalid location lookup")
        if zipcode := parsed.get("zipcode"):
            query = """SELECT * FROM perdiem where Zip = ? GROUP BY DestinationID;"""
            res = cur.execute(query, (zipcode,))
            results = res.fetchall()
        if state := parsed.get("state"):
            location = parsed.get("location", "")
            params = (f"%{location}%", f"%{location}%", state)
            query = f"""
                SELECT * FROM perdiem
                    WHERE
                        (UPPER(Name) LIKE ? OR
                        UPPER(LocationDefined) LIKE ?) AND
                    UPPER(State) = ?
                    GROUP BY DestinationID;"""
            res = cur.execute(query, params)
            results = res.fetchall()
        if results == []:
            raise ValueError(
                f"'{lookup}' not found in the database. Try just the state!"
            )
        return results

    @classmethod
    def get_rates_by_id(cls, destination_id: str):
        """Get the Per Diem Rates from the database by looking up a specific ID

        Args:
            destination_id: A str of the DestinationID field

        Returns:
            A dicts
        """
        query = """SELECT * FROM perdiem where DestinationID = ?;"""
        res = cur.execute(query, (destination_id,))
        results = res.fetchone()
        if results == None:
            raise ValueError(
                f"'{destination_id}' not found in the database. Try again!"
            )
        return results

    def calculate_per_diem(rates: dict, start_date: str, end_date: str):
        """Calculate the per diem for the number of days (taking into account the days in each month)"""
        result = 0
        start_date = date.fromisoformat(start_date)
        end_date = date.fromisoformat(end_date)
        number_of_days = (end_date - start_date).days

        # Calculate without meals
        for idx in range(number_of_days + 1):
            month = (start_date + timedelta(idx)).strftime("%b")
            result += rates[month]

            # Add meals
            if idx == 0 or idx == 1:
                result += rates["Meals"] * 0.75
            else:
                result += rates["Meals"]

        return {
            "total": result,
            "start_date": start_date,
            "end_date": end_date,
            "number_of_days": number_of_days,
            "referenced_rates": rates,
        }
