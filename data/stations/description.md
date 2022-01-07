# Description

In the directory should be placed .csv file `stations.csv` contains information about stations.

The directory must contain `wykaz_stacji.csv` file. The file (for Poland) you can download from [here](https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/).

## Expected structure `stations.csv` file

| Column | Description                      |
|--------|----------------------------------|
| code   | Short station code               |
| name   | Station name                     |
| ln_dd  | Latitude degrees                 |
| ln_mm  | Latitude minutes                 |
| ln_ss  | Latitude seconds                 |
| lt_dd  | Longitude degrees                |
| lt_mm  | Longitude minutes                |
| lt_ss  | Longitude seconds                |
| river  | River name                       |
| type   | Station type (`k` or `o` or `s`) |
| ln     | Latitude decimal degrees         |
| lt     | Longitude decimal degrees        |

Example:
```
code,name,ln_dd,ln_mm,ln_ss,lt_dd,lt_mm,lt_ss,river,type,ln,lt
3150,BABIMOST,15,47,,52,8,,OBRZYCA,k,15.78333333,52.13333333
```
