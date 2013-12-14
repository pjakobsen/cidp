#!/usr/bin/env python
# encoding: utf-8
"""
project_urls.py

Created by Peder Jakobsen on 2013-12-13.

Scrape http://www.acdi-cida.gc.ca/cidaweb/cpo.nsf/vWebProjByNumEn?OpenView&start=1&end=2
to get a list of project URLS matching project numbers



"""

import sys
import os
from bs4 import BeautifulSoup
from urllib2 import urlopen
from pprint import pprint
import petl
from sqlalchemy import *
from datetime import datetime

def main():
    url_list = ["http://www.acdi-cida.gc.ca/cidaweb/cpo.nsf/vWebProjByNumEn?OpenView",
    "http://www.acdi-cida.gc.ca/cidaweb/cpo.nsf/vWebProjByNumEn?OpenView&start=1001&end=2000",
    "http://www.acdi-cida.gc.ca/cidaweb/cpo.nsf/vWebProjByNumEn?OpenView&start=2001&end=3000"]
 
    links=[]
   
    for url in url_list:
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")
        table = soup.find("table")
        rows = table.findAll('tr')
    
        for r in rows:

            try:
                col1,col2 = r.findAll('td')[0],r.findAll('td')[1]
                dct={}
                dct['id']=col1.find('a').string
                dct['link']= "http://www.acdi-cida.gc.ca/"+col1.find('a')['href']
                try:
                    u = col2.string.encode('utf8')
                    dct['name']=u
                except:
                    raise
                
                print dct
                links.append(dct)
            except IndexError:
                pass
            except:
                raise

    table = petl.fromdicts(links)
    print petl.look(table)
    
    table = petl.cut(table,"id","name","link")
    petl.tocsv(table, "project_links.csv")
  
def todb():  
    engine = create_engine('sqlite:///../db/devdata.sqlite')
    engine.echo = True
    connection = engine.connect()
    meta = MetaData()
    meta.reflect(bind=engine)
    for table in reversed(meta.sorted_tables):
        print table
    

if __name__ == '__main__':
    todb()
    #main()

