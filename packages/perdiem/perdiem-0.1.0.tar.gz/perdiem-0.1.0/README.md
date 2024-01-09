# PerDiem

A library that allows a user to get the per diem rates for a location and calculate the per diem rates for a given period of time. It takes the data from GSA's per diem page and the computer handles the rest!

## Usage

```python
from perdiem import PerDiem

# Look up the rates for Washington, DC (accept the first result)
rates = PerDiem.get_rates("Washington, DC")[0]

# Alternatively, look up the rates by zip code!
# rates = PerDiem.get_rates("20002")[0]

start_date = "2024-01-01"
end_date = "2024-01-08"

# Calculate the total costs for a trip
trip = PerDiem.calculate_per_diem(rates, start_date, end_date)
print(trip["total"])
# 2136.5
```

## Install

```sh
pip install perdiem
```

## Features

- [x] Look up Per Diem rate by Zip Code
- [x] Compute the total (factoring first and last day travel reductions)

## Future?

- [] An API?
- [] A CLI?
- [] Export to Excel?

## License

Apache 2.0
