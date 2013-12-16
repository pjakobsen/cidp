#!/usr/bin/env python
# encoding: utf-8
"""
project_urls.py

Created by Peder Jakobsen on 2013-12-13.

Scrape http://www.acdi-cida.gc.ca/cidaweb/cpo.nsf/vWebProjByNumEn?OpenView&start=1&end=2
to get a list of project URLS matching project numbers.

Update the project table to add these URLs

"""
from __future__ import unicode_literals
import sys
import os
from bs4 import BeautifulSoup
from urllib2 import urlopen
from pprint import pprint
from sqlalchemy import *
from datetime import datetime




def main():
    
    #engine = create_engine('sqlite:///../db/dev.sqlite')
    engine = create_engine('postgres://localhost/crs')
    engine.echo = True
    connection = engine.connect()
    metadata = MetaData(engine)
    project_table = Table('project', metadata, autoload=True, autoload_with=engine)
    
    url_list = ["http://www.acdi-cida.gc.ca/cidaweb/cpo.nsf/vWebProjByNumEn?OpenView",
    "http://www.acdi-cida.gc.ca/cidaweb/cpo.nsf/vWebProjByNumEn?OpenView&start=1001&end=2000",
    "http://www.acdi-cida.gc.ca/cidaweb/cpo.nsf/vWebProjByNumEn?OpenView&start=2001&end=3000"]
    print "---------- DELETE ----", project_table.delete()
    
    stmt = project_table.insert()
    
    for url in url_list:
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")
        table = soup.find("table")
        rows = table.findAll('tr')
        
        for r in rows:

            try:
                col1,col2 = r.findAll('td')[0],r.findAll('td')[1]
                try:
                    u = u"{0}".format(col2.string)
                    print u
                except:
                    raise
                p_nr = col1.find('a').string
                print p_nr

                p,s= p_nr[:7],p_nr[-3:]
                print p,s
                stmt.execute(
                    project_number=p, 
                    sub_project_number=s,
                    full_project_number=p_nr,
                    url="http://www.acdi-cida.gc.ca/"+col1.find('a')['href'],
                    project_name=u)
            except IndexError:
                raise
            except:
                raise



if __name__ == '__main__':
    main()

