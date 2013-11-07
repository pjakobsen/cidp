# encoding: utf-8
"""
petl.py

Created by Peder Jakobsen on 2013-11-05.

"""

from petl import *
from petl.fluent import etl
import urllib2
from pprint import pprint
import simplejson as json
from data_sources import cida, iati_registry


    
def iati():

    req = urllib2.Request(iati_registry['datasets'])
    opener = urllib2.build_opener()
    f = opener.open(req)
    ds_json = json.load(f)
    tbl = etl(zip(ds_json)).pushheader(['dataset'])
    print look(tbl)
    
    
   

def cida():
    
    projects_raw = fromcsv(data['cida-project-browser'],skip)
    projects = skip(projects_raw,1)
    # Now we have to rename 'Project Number' field to 'Project number' so we can do a join
    
    #print look(projects)
    hdps2012 = fromcsv(data['hdps-2012'])
    pprint(header(projects))
    pprint(header(hdps2012))
    t1,t2 = diffheaders(projects,hdps2012)
    both = join(projects, hdps2012, key='Project number')
    print look(both)
    
    #print h1
    #print look(hdps2012)

if __name__ == '__main__':

	
	iati()

