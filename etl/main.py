# encoding: utf-8
"""
petl.py

Created by Peder Jakobsen on 2013-11-05.

"""
import sys  
from petl import *
from petl.fluent import etl
import urllib2
from pprint import pprint
import simplejson as json
from data_sources import datadir, cida, iati_registry



def download_iati_metadata():
    sample_sets="http://www.iatiregistry.org/api/search/dataset?filetype=activity&offset=1000&limit=10"
    iati_files=[]
    if sample_sets:
        req = urllib2.Request(sample_sets)
    else:
        req = urllib2.Request(iati_registry['datasets'])
    opener = urllib2.build_opener()
    f = opener.open(req)
    ds = json.load(f)
    print ds
    for d in ds['results']:
        print d
        dataset_url = "{}{}".format("http://www.iatiregistry.org/api/rest/dataset/",d)
        print dataset_url
        
        req = urllib2.Request(dataset_url)
        f = opener.open(req)
        package = json.load(f)
        print package
        for i,p in enumerate(package['resources']):
            #print i+1,p['url']
            iati_files.append((i,p['url']))
    
    print iati_files
    fp = open(datadir+'iati.csv','w')
    fp.write('\n'.join('%s %s' % i for i in iati_files))   
    fp.close() # you can omit in most cases as the destructor will call if
    
    
def iati():

    req = urllib2.Request(iati_registry['datasets'])
    opener = urllib2.build_opener()
    f = opener.open(req)
    ds = json.load(f)
    tbl = etl(zip(ds)).pushheader(['dataset'])
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
    	
	download_iati_metadata()

	

