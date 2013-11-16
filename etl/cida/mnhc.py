#!/usr/bin/env python
# encoding: utf-8
"""
mnhc.py

Created by Peder Jakobsen on 2013-11-13.

Geratate reports about MNHC related CIDA projects by:

1. Joining CIDA csv files
2. Scraping web

"""

import sys
import os
from bs4 import BeautifulSoup
from urllib2 import urlopen
from urlparse import urlparse, parse_qs

BASE_URL = "http://www.acdi-cida.gc.ca/cidaweb/cpo.nsf/vWebProjSearchEn/"

def scrape_project_profile_csv(ids):
  
    url = BASE_URL + ids
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "lxml")
    csvlink = soup.find("a", "button_surrogate")['href']
    return csvlink
    #category_links = [BASE_URL + dd.a["href"] for dd in boccat.findAll("dd")]
    #return category_links
 
def scrape_csv_urls():
    f = open("MNCH-raw.ids")
    o = open("MNCH-project.ids",'w')
    for i in f.readlines():
        l = scrape_project_profile(i)
        i = parse_qs(urlparse(l).query)
        # we only want the id
        o.write(str(i['wbs_number'][0])+"\n")
    o.close()

def mnhc_totals():
    data=[]
    
    f = open("MNCH-project.ids",'r')
    # Should come from a pickle
    mnhc_ids = [line.rstrip("\n") for line in f.readlines()] 
    cida_tbl=fromcsv(datadir+"merged.csv")

    # grab only ids that are in the mnhc_ids
    t = select(cida_tbl, lambda rec: rec[6] in mnhc_ids)
    table =convert(t, 'amount', float)

    print look(table)
    print nrows(table)
    table1 =  aggregate(table, 'project', sum, 'amount')
    print nrows(table1)
    print look(table1)
    tocsv(table1, datadir+"mnhc-totals.csv")   

def mnhc_report():
    totals = fromcsv(datadir+"mnhc-totals.csv")
    totals = rename(totals, 'key', 'project')
    totals = rename(totals, 'value', 'Affected Amount')
    browser = fromcsv(csvfiles['browser'])
    browser = skip(browser, 1)
    browser = rename(browser, 'Project Number', 'project')
    pb = cut(browser, 'project','Title','Maximum CIDA Contribution')
    #print look(pb)
    #print look(totals)
    report = join(pb,totals,key="project")
    report = convert(report,'Maximum CIDA Contribution', 'replace', '$ ', '') # Get rid of the dollar sign
    report = convert(report,'Maximum CIDA Contribution', 'replace', ',', '')
    print look(report)
    tocsv(report, datadir+"mnhc-report.csv")



def scraped_report():
 
    #FIXME: paths are relative to calling function
    f = open("cida/MNCH-raw.ids")
    for linkid in f.readlines():
        url = BASE_URL + linkid
        print url
        sys.exit()
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")
        #amount = soup.find("a", "button_surrogate")['href']
        
def report():
    scraped_report()
