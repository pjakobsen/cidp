#!/usr/bin/env python
# encoding: utf-8
"""
geocode.py

Created by Peder Jakobsen on 2014-01-12.

Create a list of geocodes for nations and pickle it for later use

"""

import sys
import os
from petl import *
import psycopg2
from geopy.geocoders import GoogleV3
import time



def main():
    db='cidp'
    user='cidp_admin'
    con = psycopg2.connect(database=db, user=user) 
    cur = con.cursor()
    # Get a list of project ids
    sql = "select country_region_name from hpds"

    t = fromdb(con,  sql)
    countries = set([t[0] for t in records(t)])
    geo=[]
    geolocator = GoogleV3()
    for c in countries:
        try:
            address, (latitude, longitude) = geolocator.geocode(c)
            #print address, latitude, longitude
            g ={'country': c, 'address':address, 'latitude':latitude, 'longitude':longitude}
            print g
            geo.append(g)
            time.sleep(1)
        except Exception,e:
            Deal wit Afghanistan TIS etc, Korea, Dem Rep. etc
            g ={'country': c, 'address':str(e), 'latitude':None, 'longitude':None}
            print g
            geo.append(g)
    table=fromdicts(geo)  
    print look(table)  
    tojson(table, 'geolocations.json')

if __name__ == '__main__':
	main()

