#!/usr/bin/env python
# encoding: utf-8
"""
d3data.py

Created by Peder Jakobsen on 2013-12-09.
Create some data from API for D3 demo
"""
import petl
from petl import *
import json
import urllib2
from pprint import pprint 
from petl import *
import sys
from collections import defaultdict



def main():
    mort = fromcsv('mortality.csv')
    mort = skip(mort,2)
    mort = cut(mort,"Country Name","1973","2006","2007","2008","2009","2010","2011","2012")
    mort = petl.rename(mort, 'Country Name', 'country')
    mort_rates = facetcolumns(mort, 'country')
    pprint(mort_rates['Malaysia'])
    pprint(mort_rates['Denmark'])
    pprint(mort_rates['Japan'])
    
    sys.exit()
    f = open('mnhc.ids')
    base_url = 'http://cidp.herokuapp.com/cube/cida/facts?cut=project_number:'#A033033007
    bads = ['Africa MC','Americas MC','Asia MC','Europe MC']
    renamethis={'Afghanistan TIS':'Afghanistan',
                'Tanzania,Un Rep':'Tanzania',
                'Lao, Dem. Rep':'Lao',
                'Congo, Dem Rep.':'Congo'}

    '''
    use project browser instead,since there seems to be nothing that uniquely identifies historical activities, 
    for example there are 6 entries for #A033033007
    '''
    dat=[]
    for id in list(f)[0:1]:
        print base_url + id
        project_data = json.load(urllib2.urlopen(base_url + id))
        print renamethis.keys()
        for p in project_data:
            c= p['country_region_name']
            country =  renamethis[c] if  c in renamethis.keys() else c
            #mortality_rates = 
            if country not in bads:
                dat.append( {
                      'id':p['id'],
                      'project':p['project_number'],
                      'year':p['fiscal_year'],
                      'continent':p['continent_name'],
                      'country':country,
                      'max':int(round(p['maximum_cida_contribution'])),
                      'spent':int(round(p['amount_spent']))}
                      
                )
                
    c = petl.fromdicts(dat) 

    
    '''
    browser =  fromcsv("../../etl/cida/data/Project Browser English.csv")

    browser = skip(browser, 1)
    pprint(header(browser))
    ex()
    browser = rename(browser, "Country","country")
    browser = cut(browser, "country","Maximum CIDA Contribution")
    print header(browser)
    print look(browser)
    new = petl.lookupjoin(c,mort,"country")
    '''
    
    
    
    print look(new)
    sys.exit()
    petl.tojson(new, 'mashup.json')

if __name__ == '__main__':
	main()

