Maybe, someday, we will have a useful readme with actual sentences here. 

for now, just a list of stuff you can query:

## LOC record of town name

``` 
dig loc uzwil.zipdns.ch +short
47 26 13.573 N 9 8 12.100 E 1.00m 1m 10000m 10m
````

Note:
 * may return multiple records if the city has multiple zip codes
 * some locations have the canton in the name as well, especially if there are multiple towns with the same name. Separated with underscore:
  ```dig loc seewen_sz.zipdns.ch```
 * names with non-ascii characters are IDNA encoded. Some dig versions do this automatically, some don't.
  Example 'Rüdlingen': ```dig loc xn--rdlingen-65a.zipdns.ch```


## LOC record of zip

``` 
dig loc 8604.zipdns.ch +short
47 23 43.987 N 8 40 58.480 E 1.00m 1m 10000m 10m
``` 


## TXT Record of  town name -> get ZIP

```
dig txt embrach.zipdns.ch +short
"8424"
```

##  TXT record of zip -> Town name

``` 
dig txt 8302.zipdns.ch +short
"Kloten"
``` 

## URI Record for town name or zip

Returns openstreetmap link

``` 
dig uri montreux.zipdns.ch +short
10 1 "http://www.openstreetmap.org/?mlat=46.4280492746&mlon=6.90336861785&zoom=12"
``` 

``` 
dig uri 8304.zipdns.ch +short
10 1 "http://www.openstreetmap.org/?mlat=47.4187043631&mlon=8.59603214251&zoom=12"
```


# But why?!

Because JP Mens [tweeted])(https://twitter.com/jpmens/status/1312372433777766402) and [blogged](https://jpmens.net/2020/10/04/airports-of-the-world/) about it. 

Implementation idea: M. Rimann ( https://twitter.com/mrimann/status/1313150991630585857 ) 
URI and TXT records stolen from Stéphane Bortzmeyer ( https://www.bortzmeyer.org/dns-code-postal-lonlat.html )
