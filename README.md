# Geocoding - From CSV to LatLng

## Intro

## Requirements

1. To use this application on macOS, ensure `python3` is installed,
along with `pip3` (python package manager). Easiest way to accomplish
this is to install the `brew` [package manager](https://brew.sh/).
2. Run

## CSV File Notes

it's important that the header row (first row in the csv file) only contains the necessary fields as follows:

1. `store_name`
2. `address_1`
3. `address_2`
4. `city`
5. `state`
6. `zip`
7. `phone`

The first line should be as follows:

`store_name,address_1,address_2,city,state,zip,phone`

## TODO

- Ensure api key is different from Javascript mapping API.
- Note which lines in CSV file do not correlate to a place in Google
- Create file with addresses missing stores
- Appending JSON if run with subset of stores (after addresses are fixed)
- document pyenv details
- document config file
- setuptools add path and virtualenv
- auto create directories if not existent already
