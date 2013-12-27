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
from sqlalchemy import *

BASE_URL = "http://www.acdi-cida.gc.ca/cidaweb/cpo.nsf/vWebProjSearchEn/"

def scrape_project_profile_csv(ids):
    ''' This uses the special URL ids'''
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

def scrape_project_ids():
    '''
      Get a list of MNHC ids put and put them in the initiative_projet table
    '''
    engine = create_engine('postgres://localhost/crs')
    engine.echo = True
    connection = engine.connect()      
    metadata = MetaData(engine)
    '''
    initiative_table = Table('initiative', metadata, autoload=True, autoload_with=engine)
    stmt = initiative_table.insert()
    result = stmt.execute(
            name="Maternal, Natal, and Child Health Intiative",
            alternate_name='Moskoka Intiative',
            short_name='MNCH',
            url="http://www.acdi-cida.gc.ca/cidaweb/cpo.nsf/fWebProjListEn?ReadForm&profile=SMNE-MNCH"
            )
    '''
    initiative_id = 1#result.lastrowid    
    
    initiative_project_table = Table('initiative_project', metadata, autoload=True, autoload_with=engine)
    stmt = initiative_project_table.insert()
    project_table = Table('project', metadata, autoload=True, autoload_with=engine)
    p_stmt = project_table.select()
    
    links=[]
    print "-------- GET A LIST OF MNHC PROJECTS BY SCRAPING DFAIT WEB SITE -------------"
    url = "http://www.acdi-cida.gc.ca/cidaweb/cpo.nsf/fWebProjListEn?ReadForm&profile=SMNE-MNCH"
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table", {"class" : "viewtable"})
    for row in table.findAll("a", "noline"):
        links.append("http://www.acdi-cida.gc.ca" +  row['href'])
    
    ids=[]
    for l in links:
        html = urlopen(l).read()
        soup = BeautifulSoup(html, "lxml")
        info = soup.findAll("div", "cpodata")
        project_number = "".join(info[0].text.split("-"))
        p_stmt = project_table.select(project_table.c.full_project_number==project_number)
        p_id= p_stmt.execute().fetchall()[0][0]
        print "-------------------", project_number, p_id
        stmt.execute(
                project_id=p_id,
                initiative_id=initiative_id)
    
    
        
        
        
if __name__ == '__main__':
    scrape_project_ids()
