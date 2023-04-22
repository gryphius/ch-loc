#!/usr/bin/python3

import requests 
import json 
import sys
import time
from datetime import datetime

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
        lieu = fields['ortbez18']
        postleitzahl = fields['postleitzahl']
        meridien,grado_di_latitudine=row['geometry']['coordinates']
        lat_h,lat_m,lat_s = dectodms(grado_di_latitudine)
        lon_h,lon_m,lon_s = dectodms(meridien)

        plz_loc_record = f'{postleitzahl} {ttl} IN LOC {lat_h} {lat_m} {lat_s:.3f} N {lon_h} {lon_m} {lon_s:.3f} E 1.00m 1.00m 10000.00m 10.00m'
        yield plz_loc_record

        plz_txt_record = f'{postleitzahl} {ttl} IN TXT "{lieu}"'
        yield plz_txt_record

        plz_uri_record = f'{postleitzahl} {ttl} IN URI 10 1 "http://www.openstreetmap.org/?mlat={grado_di_latitudine}&mlon={meridien}&zoom=12"'
        yield plz_uri_record

        # 'buchs zh' -> 'buchs_zh'
        lieu = lieu.replace(' ','_')

        # langnau i.e.
        lieu = lieu.replace('.','_')

        # remove parentheses
        lieu = lieu.replace(')','')
        lieu = lieu.replace('_(','_')
        lieu = lieu.replace('(','_')

        # some locations have multiple names, i.e. "biel" / "bienne" - create records for all of them
        all_names = lieu.split('/')

        for ortname in all_names:
            # idna encoding 
            ort_idna = ortname.lower().encode('idna').decode()

            ort_loc_record = f'{ort_idna} {ttl} IN LOC {lat_h} {lat_m} {lat_s:.3f} N {lon_h} {lon_m} {lon_s:.3f} E 1.00m 1.00m 10000.00m 10.00m'
            yield ort_loc_record

            ort_txt_record = f'{ort_idna} {ttl} IN TXT "{postleitzahl}"'
            yield ort_txt_record

            ort_uri_record = f'{ort_idna} {ttl} IN URI 10 1 "http://www.openstreetmap.org/?mlat={grado_di_latitudine}&mlon={meridien}&zoom=12"'
            yield ort_uri_record
        

if __name__=='__main__':
    url = 'https://swisspost.opendatasoft.com/explore/dataset/plz_verzeichnis_v2/download/?format=json&timezone=Europe/Berlin&lang=de'
    if len(sys.argv)>1:
        jsondata = json.load(open(sys.argv[1],'r'))
    else:
        jsondata = requests.get(url).json()
    
    ZONE='zipdns.ch'
    NS=[
        'fries.anooky-dns.ch',
        'steak.anooky-dns.ch',
        'burger.anooky-dns.ch',
    ]
    SOA_EMAIL=f'anooky.anooy-dns.ch'
    SOA_SERIAL=datetime.now().strftime("%Y%m%d%H")
    print(f'$ORIGIN {ZONE}')
    print(f'@ SOA {NS[0]}. {SOA_EMAIL}. {SOA_SERIAL} 900 600 1123200 900')
    for nameserver in NS:
        print(f'@ 3600 IN NS {nameserver}.')
    print(f'@ 3600 IN MX 10 .')
    print(f'@ 3600 IN TXT "v=spf1 -all"')
    print(f'_dmarc 3600 IN TXT "v=DMARC1; p=reject;"')

    sorted_unique_recs = sorted(set([r for r in generate_loc(jsondata)]))
    for row in sorted_unique_recs:
        print(row)
