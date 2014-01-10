# encoding: utf-8

import os
import sys
import urllib
from pprint import pprint
from lxml import etree
from lxml import objectify
from data_sources import datadir
from petl import fromcsv, look, head

 
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
        
def xmlfiles():
    ''' Traverse through every XML document and put 
        important fields into a dict 
    '''
    xmldir=datadir + "iati_xml/"
    xfiles = []
    for root, dirs, files in os.walk(xmldir): # Walk directory tree
        for f in files:
            xfiles.append(root+f)
    return xfiles

def xmltodict(xmlFile):
    parser = etree.XMLParser(remove_blank_text=True)
    with open(xmlFile) as f:
        xml = f.read()
    root = objectify.fromstring(xml)
    print type(root)
    d = dict((e.tag, e.text) for e in root['iati-activity'].iterchildren())
    pprint(d)
    #Have a look at the format generated with CSV tool
    with open(datadir+"iati_transformations/iati_download_20131107_simple_aa-activity.csv") as f:
        k = fromcsv(f.read())
        
    sys.exit()
    
    

if __name__ == '__main__':
    #dowload_datastore_files()

