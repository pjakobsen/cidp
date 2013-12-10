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
    def getmort(c,y):
        try:
          return mort_rates[c][y]  
        except:
          return ''
        
    ''' faceting allows us to do for example:
    pprint(mort_rates['Malaysia']['2009'])
    pprint(mort_rates['Denmark'])
   
    '''

    f = open('mnhc.ids')
    base_url = 'http://localhost:7000/cube/cida/'
    fact_url = base_url+'facts?cut=project_number:'#A033033007
    aggregate_url = base_url+ 'aggregate?cut=project_number:'#A033033007
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
    for id in list(f)[0:-1]:

        project_data = json.load(urllib2.urlopen(fact_url + id))
         # now we can append aggregates
        aggr = json.load(urllib2.urlopen(aggregate_url + id))['summary']
        # just grab the first record
        #for p in project_data:
        p=project_data[0]
        c= p['country_region_name']
        country =  renamethis[c] if  c in renamethis.keys() else c

        if country not in bads:
            dat.append( {
                  'id':p['id'],
                  'project':p['project_number'],
                  'year':p['fiscal_year'],
                  'continent':p['continent_name'],
                  'country':country,
                  'max':int(round(p['maximum_cida_contribution'])),
                  'spent':int(round(aggr['amount_spent_sum'])),
                  'mortality_rate':getmort(c,p['fiscal_year'])}
                  
            )
       
    comb = petl.fromdicts(dat) 

    print look(comb)
    petl.tojson(comb, 'mashup.json')

if __name__ == '__main__':
	main()

