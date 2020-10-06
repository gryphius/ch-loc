# Update the zone

```
python3 generate-zone.py > zipdns.ch.zone
```

replace records in powerdns:

``` 
pdnsutil load-zone zipdns.ch zipdns.ch.zone
```

make sure everything is happy:

``` 
pdnsutil check-zone zipdns.ch
``` 

increase serial

``` 
pdnsutil increase-serial zipdns.ch
``` 



