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

def main():
    url = "http://www.acdi-cida.gc.ca/cidaweb/cpo.nsf/vWebProjByNumEn?OpenView&start=10&end=11"
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table")
    rows = table.findAll('tr')
    links=[]
    for r in rows:

        try:
            col1,col2 = r.findAll('td')[0],r.findAll('td')[1]
            print col1.find('a').string,"http://www.acdi-cida.gc.ca/"+col1.find('a')['href'],col2.string
            
            #print r.find('a').string, r.find('a')['href']
        except:
            pass
        #links.append((r.find('a').string, r.find('a')['href']))
        
    print links
    #link = soup.find("a", "col1 alignCenter")['href']
    #print link


if __name__ == '__main__':
	main()

