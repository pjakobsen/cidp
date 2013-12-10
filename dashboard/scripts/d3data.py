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
from collections import defaultdict, Counter



def main():
    mort = fromcsv('mortality.csv')
    mort = skip(mort,2)
    mort = cut(mort,"Country Name","2006","2007","2008","2009","2010","2011","2012")
    mort = petl.rename(mort, 'Country Name', 'country')
    mort_rates = facetcolumns(mort, 'country')
    def getmort(c,y):
        try:
          return float(mort_rates[c][y][0])
        except:
          return None
        
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
                'Lao, Dem. Rep.':'Lao',
                'Congo, Dem Rep.':'Congo'}

    '''
    use project browser instead,since there seems to be nothing that uniquely identifies historical activities, 
    for example there are 6 entries for #A033033007
    '''

    mashup_file=open('mashup.json','w')
    mashup_data=[]
    for id in list(f)[0:-1]:

        project_data = json.load(urllib2.urlopen(fact_url + id))
         # now we can append aggregates
        aggr = json.load(urllib2.urlopen(aggregate_url + id))['summary']
        # just grab the first record
            
        p=project_data[0]
        c= p['country_region_name']
        country =  renamethis[c] if  c in renamethis.keys() else c
    
        if country not in bads:
            mashup_data.append({
                  'id':p['id'],
                  'project':p['project_number'],
                  'year':p['fiscal_year'],
                  'continent':p['continent_name'],
                  'country':country,
                  'max':int(round(p['maximum_cida_contribution'])),
                  'spent':int(round(aggr['amount_spent_sum'])),
                  'mortality_rate':getmort(c,p['fiscal_year'])})

            
    mashup=fromdicts(mashup_data)
    tocsv(mashup,'raw-mnhc.csv')
    
    print look(mashup)
    sys.exit()
    key_fields = ['project', 'max', 'year', 'country', 'mortality_rate', 'id', 'continent']
    value_field = 'spent'
    ''''
    tbl_out = (
        tbl_in
        .aggregate(key=key_fields, aggregation=sum, value=value_field)
        .unpack('key', key_fields)
        .rename('value', value_field)
    )   
    '''
    tbl_out = aggregate(mashup, ['country','year','mortality_rate'], sum, 'spent')
    tbl_out = unpack(tbl_out, 'key',['country','year','mortality_rate'])
    tbl_out = rename(tbl_out, 'value','spent')
    tbl_out = cut(tbl_out, 'country','year','spent','mortality_rate') #cut to reorder
    
    
    print look(tbl_out)
    tocsv(tbl_out,"mnhc-report.csv")
def mashup_combine():
    with open('mashup.json') as f:
        dat = json.loads(f.read())
        countries = set([d['country'] for d in dat])
        for c in countries:
            c_dat=[(c,d) for d in dat if d['country']==c]
            print c_dat
            print "---------"

def mashup_counter():
    counter = Counter()
    with open('mashup.json') as f:
        dat = json.loads(f.read())[0]
        
        
        
            

if __name__ == '__main__':
	main()
	#mashup_combine()
	#mashup_counter()
	

