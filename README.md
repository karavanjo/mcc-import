# Import tool for "My city's climate"

The command line application imports historical weather data in MongoDB Atlas database.

## Technical notes

The application requires MongoDB > 5.0 with support time series.

You should specify connection credentials. The application only supports X.509 Authentication with `.pem` certificate.

### How to use

1. Copy your weather data files to `data/observations` and `data/stations`.
2. Apply your credentials to `config.yaml`.
3. Install [poetry](https://python-poetry.org/docs/#installation).
4. `poetry install --no-dev`
5. `poetry run import`

## About data

It is assumed that input weather data format corresponds to public data IMGW-PIB format.

You can explore the dataset on a page of Institute of Meteorology and Water Management by [link](https://danepubliczne.imgw.pl/).
