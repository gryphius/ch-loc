#!/usr/bin/python3


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


def generate_loc(csvdata,ttl=86400):
    zoom=12

    for row in csvdata:
        if 'Ortschaftsname' not in row:
            continue 

        lieu = row['Ortschaftsname']
        postleitzahl = row['PLZ']
        longtitude = float(row['E'])
        latitude = float(row['N'])
        lat_h,lat_m,lat_s = dectodms(latitude)
        lon_h,lon_m,lon_s = dectodms(longtitude)

        plz_loc_record = f'{postleitzahl} {ttl} IN LOC {lat_h} {lat_m} {lat_s:.3f} N {lon_h} {lon_m} {lon_s:.3f} E 1.00m 1.00m 10000.00m 10.00m'
        yield plz_loc_record

        plz_txt_record = f'{postleitzahl} {ttl} IN TXT "{lieu}"'
        yield plz_txt_record

        plz_uri_record = f'{postleitzahl} {ttl} IN URI 10 1 "https://www.openstreetmap.org/#map={zoom}/{latitude}/{longtitude}"'
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

            ort_uri_record = f'{ort_idna} {ttl} IN URI 10 1 "https://www.openstreetmap.org/#map={zoom}/{latitude}/{longtitude}"'
            yield ort_uri_record
        

if __name__=='__main__':
    # the first argument must be a path to a csv file
    if len(sys.argv) < 2:
        print('Usage: generate-zone.py <path-to-csv-file>')
        print('Download the csv from https://www.swisstopo.admin.ch/de/amtliches-ortschaftenverzeichnis#Ortschaftenverzeichnis--Download')
        print('Use the CSV in WGS84 format ( the one that has no files in other formats)')
        sys.exit(1)

    # read the csv file into a list of dictionaries
    import csv
    with open(sys.argv[1], 'r',  encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        csvdata = list(reader)


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
    print(f'@ 3600 IN MX 0 .')
    print(f'@ 3600 IN TXT "v=spf1 -all"')
    print(f'_dmarc 3600 IN TXT "v=DMARC1; p=reject;"')

    sorted_unique_recs = sorted(set([r for r in generate_loc(csvdata)]))
    for row in sorted_unique_recs:
        print(row)
