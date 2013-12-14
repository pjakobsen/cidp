#!/usr/bin/env python
# encoding: utf-8
"""
d3data.py

Created by Peder Jakobsen on 2013-12-09.
Create some data from API for D3 demo
"""
import pycountry
import petl
from petl import *
import json
import urllib2
from pprint import pprint 
from petl import *
import sys
from collections import defaultdict, Counter



def main():
    
    '''
    Get additional data from each country in MNCH data
    
    
    '''
    mnhc = fromcsv('raw-mnhc-fixed.csv')
    links = fromcsv('../../etl/cida/project_links.csv')
    links = {l[0]:l[2] for l in data(links)}
   

    h = fromcsv('who-health.csv')
 
    
    d = cut(h, "Indicator Name")
    print look(distinct(d), 0,2)
   

    year_range= [str(n) for n in range(1995, 2012)]
    health_expenditure = select(h,"{Indicator Name} == 'Health expenditure, total (% of GDP)'")
    birth_rate = select(h,"{Indicator Name} == 'Birth rate, crude (per 1,000 people)'")
    electricity = select(h,"{Indicator Name} == 'Access to electricity (% of population)'")
    vitamin_a = select(h,"{Indicator Name} == 'Vitamin A supplementation coverage rate (% of children ages 6-59 months)'")
    print "------- Health Expenditure % of GDP -------"
    print look(cut(health_expenditure,"Country Code",*year_range),10,20)
    # print "------- ELECTRICTY -------"
    # print look(cut(electricity,"Country Code","2000","2011","2012"))
    #h = cut(h,'Country Code','Indicator Name','2010','2011')
    # Create a new column of country codes and add it to the table
    country_codes = []
    web_links=[]
    for d in iterdata(mnhc):
        link=links[d[0]]
        web_links.append(link)
        code=pycountry.countries.get(name=d[3]).alpha3

        country_codes.append(code)
    mnhc = addcolumn(mnhc, 'Country code', country_codes)
    mnhc = addcolumn(mnhc, 'weblink', web_links)
    #print look(mnhc)
    
    
    health_expenditure = select(h,"{Indicator Name} == 'Health expenditure, total (% of GDP)'")
    birth_rate = select(h,"{Indicator Name} == 'Birth rate, crude (per 1,000 people)'")
    electricity = select(h,"{Indicator Name} == 'Birth rate, crude (per 1,000 people)'")
    vitamin_a = select(h,"{Indicator Name} == 'Vitamin A supplementation coverage rate (% of children ages 6-59 months)'")
    #print look(vitamin_a,10,40)
   
if __name__ == '__main__':
    main()
	
	

