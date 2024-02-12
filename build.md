# Download the data
open https://www.swisstopo.admin.ch/de/amtliches-ortschaftenverzeichnis#Ortschaftenverzeichnis--Download

check the current link for the csv ( the second csv shich does not have more data options, in WGS84 format )

```
curl -O  'https://data.geo.admin.ch/ch.swisstopo-vd.ortschaftenverzeichnis_plz/ortschaftenverzeichnis_plz/ortschaftenverzeichnis_plz_4326.csv.zip'
unzip *.zip
```

# Update the zone

```
python3 generate-zone.py AMTOVZ_CSV_WGS84/AMTOVZ_CSV_WGS84.csv  > zipdns.ch.zone
```

replace records in powerdns:

``` 
pdnsutil load-zone zipdns.ch zipdns.ch.zone
```
rectify:
```
pdnsutil rectify-zone zipdns.ch
```

make sure everything is happy:

``` 
pdnsutil check-zone zipdns.ch
``` 

notify slaves if necessary:
``` 
sudo pdns_control notify zipdns.ch
```
