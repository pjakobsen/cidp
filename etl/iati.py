# encoding: utf-8

import os
import sys
from pprint import pprint
from lxml import etree
from lxml import objectify
from data_sources import datadir
from petl import fromcsv, look, head

        
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
    for x in  xmlfiles():
        xmltodict(x)

