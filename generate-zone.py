#!/usr/bin/python3

import requests 
import json 
import sys

def dectodms(coord):
   pos = (coord>0)
   abs_coord = abs(coord)
   minutes,seconds = divmod(abs_coord*3600,60)
   degrees,minutes = divmod(minutes,60)
   degrees = degrees if pos else -degrees
   return (int(degrees),int(minutes),seconds)


def generate_loc(jsondata,ttl=86400):
    
    for row in jsondata:
        if 'geometry' not in row:
            continue 
        fields = row['fields']
        ortname = fields['ortbez18']
        # 'buchs zh' -> 'buchs_zh'
        ortname = ortname.replace(' ','_')

        # langnau i.e.
        ortname = ortname.replace('.','_')

        # idna encoding 
        ort_idna = ortname.lower().encode('idna').decode()

        postleitzahl = fields['postleitzahl']
        lon,lat=row['geometry']['coordinates']
        lat_h,lat_m,lat_s = dectodms(lat)
        lon_h,lon_m,lon_s = dectodms(lon)

        plz_record = f'{postleitzahl} {ttl} IN LOC {lat_h} {lat_m} {lat_s:.3f} N {lon_h} {lon_m} {lon_s:.3f} E 1.00m 1.00m 10000.00m 10.00m'
        ort_record = f'{ort_idna} {ttl} IN LOC {lat_h} {lat_m} {lat_s:.3f} N {lon_h} {lon_m} {lon_s:.3f} E 1.00m 1.00m 10000.00m 10.00m'
        yield plz_record
        yield ort_record

if __name__=='__main__':
    url = 'https://swisspost.opendatasoft.com/explore/dataset/plz_verzeichnis_v2/download/?format=json&timezone=Europe/Berlin&lang=de'
    if len(sys.argv)>1:
        jsondata = json.load(open(sys.argv[1],'r'))
    else:
        jsondata = requests.get(url).json()
    
    ZONE='testloc.ch'
    NS=[
        'ns.ed448.ch'
    ]
    SOA_EMAIL=f'hostnamster.{ZONE}'
    print(f'$ORIGIN {ZONE}')
    print(f'@ SOA {NS[0]}. {SOA_EMAIL}. 1 900 600 1123200 900')
    for nameserver in NS:
        print(f'@ 3600 IN NS {nameserver}.')
    for row in generate_loc(jsondata):
        print(row)
    
