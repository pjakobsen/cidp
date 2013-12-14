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
    
    engine = create_engine('sqlite:///../db/devdata.sqlite')
    engine.echo = True
    connection = engine.connect()
    metadata = MetaData(engine)
    country = Table('project', metadata, autoload=True, autoload_with=engine)
    
    url_list = ["http://www.acdi-cida.gc.ca/cidaweb/cpo.nsf/vWebProjByNumEn?OpenView",
    "http://www.acdi-cida.gc.ca/cidaweb/cpo.nsf/vWebProjByNumEn?OpenView&start=1001&end=2000",
    "http://www.acdi-cida.gc.ca/cidaweb/cpo.nsf/vWebProjByNumEn?OpenView&start=2001&end=3000"]
 

    for url in url_list:
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")
        table = soup.find("table")
        rows = table.findAll('tr')
        stmt = project.insert()
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
                
                stmt.execute(id='2', country_name='Canada2', country_code='KC2',short_name="Canuck3")
            except IndexError:
                pass
            except:
                raise

    table = petl.fromdicts(links)

    
def todb(): 


   
   
    

if __name__ == '__main__':
    #pass
    #todb()
    main()

