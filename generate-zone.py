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
        ortbez = fields['ortbez18']
        postleitzahl = fields['postleitzahl']
        lon,lat=row['geometry']['coordinates']
        lat_h,lat_m,lat_s = dectodms(lat)
        lon_h,lon_m,lon_s = dectodms(lon)

        plz_loc_record = f'{postleitzahl} {ttl} IN LOC {lat_h} {lat_m} {lat_s:.3f} N {lon_h} {lon_m} {lon_s:.3f} E 1.00m 1.00m 10000.00m 10.00m'
        yield plz_loc_record

        plz_txt_record = f'{postleitzahl} {ttl} IN TXT "{ortbez}"'
        yield plz_txt_record

        plz_uri_record = f'{postleitzahl} {ttl} IN URI 10 1 "http://www.openstreetmap.org/?mlat={lat}&mlon={lon}&zoom=12"'
        yield plz_uri_record

        # 'buchs zh' -> 'buchs_zh'
        ortbez = ortbez.replace(' ','_')

        # langnau i.e.
        ortbez = ortbez.replace('.','_')

        # remove parentheses
        ortbez = ortbez.replace(')','')
        ortbez = ortbez.replace('_(','_')
        ortbez = ortbez.replace('(','_')

        # some locations have multiple names, i.e. "biel" / "bienne" - create records for all of them
        all_names = ortbez.split('/')

        for ortname in all_names:
            # idna encoding 
            ort_idna = ortname.lower().encode('idna').decode()

            ort_loc_record = f'{ort_idna} {ttl} IN LOC {lat_h} {lat_m} {lat_s:.3f} N {lon_h} {lon_m} {lon_s:.3f} E 1.00m 1.00m 10000.00m 10.00m'
            yield ort_loc_record

            ort_txt_record = f'{ort_idna} {ttl} IN TXT "{postleitzahl}"'
            yield ort_txt_record

            ort_uri_record = f'{ort_idna} {ttl} IN URI 10 1 "http://www.openstreetmap.org/?mlat={lat}&mlon={lon}&zoom=12"'
            yield ort_uri_record
        

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
    SOA_EMAIL=f'hostmaster.{ZONE}'
    print(f'$ORIGIN {ZONE}')
    print(f'@ SOA {NS[0]}. {SOA_EMAIL}. 1 900 600 1123200 900')
    for nameserver in NS:
        print(f'@ 3600 IN NS {nameserver}.')

    dupes={}
    for row in generate_loc(jsondata):
        if row in dupes:
            continue
        print(row)
        dupes[row]=1
    
