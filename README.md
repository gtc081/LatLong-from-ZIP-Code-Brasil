# LatLong-from-ZIP-Code-Brasil
Crawler that returns coordinates LatLong from Brazilian ZIP Codes.

## Steps
- First it reads the .csv with the zip codes
- For each one, it searches the address on Correios API
- With the address, it uses the geopy lib to search for the coordinates
- For last, it saves the LatLong information on a new .csv file
  - If the LatLoang was found, it saves on "out_validos.csv"
  - If not, it saves on "out_invalidos.csv"
