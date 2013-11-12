# encoding: utf-8
"""
cida.py

Created by Peder Jakobsen on 2013-11-05.

"""
import sys
import csv
from pprint import pprint
from petl import *
from petl.fluent import etl
#import sqlite3
import psycopg2
from bs4 import BeautifulSoup
from urllib2 import urlopen
from urlparse import urlparse, parse_qs

datadir = '/Users/peder/dev/cidp/'
csvfiles = {'browser': datadir + 'Project Browser English.csv',
 'hdps-2012': datadir + 'HPDS-2011-2012-eng.csv',
 'hdps-2011': datadir + 'HPDS-2010-2011-eng.csv',
 'hdps-2010': datadir + 'HPDS-2009-2010-eng.csv',
 'hdps-2009': datadir + 'HPDS-2008-2009-eng.csv',
 'hdps-2008': datadir + 'HPDS-2007-2008-eng.csv',
 'hdps-2007': datadir + 'HPDS-2006-2007-eng.csv',
 'hdps-2006': datadir + 'HPDS-2005-2006-eng.csv'}
fieldmap = {'Fiscal year': 'year',
 'Project number': 'project',
 'Status': 'status',
 'Maximum CIDA contribution (project-level)': 'cida_contrib',
 'Organisation name': 'org',
 'Continent name': 'continent',
 'Project Browser country ID': 'br_country_id',
 'Country/region name': 'region',
 'Country/region percent': 'region_percent',
 'Sector name': 'sector',
 'Sector ID': 'sector_id',
 'Sector percent': 'sector_percent',
 'Amount spent': 'amount'}

def combine_hpds():
    pprint(header(fromcsv(csvfiles['hdps-2012'])))

    def cutem(key, value):
        c = fromcsv(value)
        if 'Date created' in ''.join(header(c)):
            c = skip(c, 1)
        c = cut(c, fieldmap.keys())
        c = rename(c, fieldmap)
        c = convert(c, 'year', {
         '2011/2012': 2012,
         '2010/2011': 2011,
         '2009/2010': 2010,
         '2008/2009': 2009,
         '2007/2008': 2008,
         '2006/2007': 2007,
         '2005/2006': 2006})
        return (key, c)

    csv = dict((cutem(key, value) for key, value in csvfiles.items()))
    merged = mergesort(csv['hdps-2012'], csv['hdps-2011'], csv['hdps-2010'], csv['hdps-2009'], csv['hdps-2008'],csv['hdps-2007'],csv['hdps-2006'], key='project')
    print rowcount(merged)
    tocsv(rowslice(merged), datadir + 'merged.csv')


def setup_db():
    pass


def project_browser():
    rawfile = fromcsv(csvfiles['browser'])
    projects = skip(rawfile, 1)
    projects = rename(projects, 'Project Number', 'Project number')
    pprint(header(projects))
    projects = cut(projects, 'Project number', 'Title', 'Start', 'End')
    print look(projects)
    print '------------- HDPS ----------------'
    hdps2012 = fromcsv(csvfiles['hdps-2012'])
    hdps2012 = cut(projects, 'Project number', 'Title', 'Start', 'End')
    print look(hdps2012)
    sys.exit()
    t1, t2 = diffheaders(projects, hdps2012)
    joined = join(projects, hdps2012, key='Project number')
    print look(joined, 30)
    pprint(header(joined))


def load_sqlite_db():
    
    fields = ','.join(fieldmap.values())
    print fields
    
   
    table = fromcsv(datadir + 'merged.csv')
    table_name = 'projects'
    try:
        conn = sqlite3.connect('cida.db')
        c = conn.cursor()
        sql = 'create table  {} ({})'.format(table_name, fields)
        print sql
        c.execute(sql)
        conn.commit()
    except:
        raise

    todb(table, conn, table_name)

def load_postrges():
    fields = ['id INT PRIMARY KEY',
                  'year INT',
                  'continent VARCHAR(20)',
                  'cida_contrib VARCHAR(20)',
                  'org VARCHAR(20)',
                  'status VARCHAR(20)',
                  'br_country_id VARCHAR(20)',
                  'region VARCHAR(20)',
                  'project VARCHAR(210)',
                  'region_percent VARCHAR(20)',
                  'sector VARCHAR(20)',
                   'sector_id VARCHAR(20)',
                   'sector_percent VARCHAR(20)',
                   'amount FLOAT'
                   ]
    table = fromcsv(datadir + 'merged.csv')
    table_name = 'projects'
    try:
        con = psycopg2.connect(database='crs', user='peder') 
        cur = con.cursor()
        
        cur.execute('DROP TABLE projects')
        sql = 'CREATE TABLE {} ({})'.format(table_name, ",".join(fields))
        cur.execute('SELECT version()')  
        print sql
        
        ver = cur.fetchone()
        cur.execute(sql)
        con.commit()
        print ver
    except:
        raise
    
    todb(table, con, table_name)

def simple_merge():
    '''
    Create a very simple CSV file that only has most essential fields from 3 sources:
    IATI
    PB
    Merged HPDS
    '''
    
    
    # Project Browswer
    a = fromcsv(csvfiles['browser'])
    a = skip(a,1)

    
    b = rename(a, 'Project Number', 'project')
    b = rename(b, 'Maximum CIDA Contribution','amount')
    b = convert(b,'amount', 'replace', '$ ', '') # Get rid of the dollar sign
    b = convert(b,'amount', 'replace', ',', '') # Get rid of commas
    b = rename(b, 'End','year')
    pb = cut(b, 'project','amount','year')
    pb = addfield(pb, 'source', "PB")
    pb =convert(pb, 'year', int)
    pb =convert(pb, 'amount', float)

    m = fromcsv(datadir+'merged.csv')
    h=cut(m, 'project','amount','year')
    h =convert(h, 'year', int)
    h =convert(h, 'amount', float)
    hist = addfield(h, 'source', "HPDS")
    merged= mergesort(pb, hist, key='project')
    print rowcount(merged)
    print look(merged)
    tocsv(merged, datadir+"minimerge.csv")
  
BASE_URL = "http://www.acdi-cida.gc.ca/cidaweb/cpo.nsf/vWebProjSearchEn/"

def scrape_project_profile(ids):
  
        url = BASE_URL + ids
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")
        csvlink = soup.find("a", "button_surrogate")['href']
        return csvlink
        #category_links = [BASE_URL + dd.a["href"] for dd in boccat.findAll("dd")]
        #return category_links
 
def scrape_mnhc():
    f = open("MNCH-raw.ids")
    o = open("MNCH-project.ids",'w')
    for i in f.readlines():
        l = scrape_project_profile(i)
        i = parse_qs(urlparse(l).query)
        # we only want the id
        o.write(str(i['wbs_number'])+"\n")
    o.close()
    
     
    
def compare_headers():
    pb = skip(fromcsv(csvfiles['browser']),1)
    pb = header(rename(pb, 'Project Number', 'Project number'))
    hdps = header(skip(fromcsv(csvfiles['hdps-2012']),0))
    pprint(pb)
    pprint(hdps)
    s = set(pb).intersection(set(hdps) )
    pprint(s)
    
def mnhc_report():
    d={}
    with open(datadir+'minimerge.csv') as f: 
        f.readline()
        for line in f:
            l = line.split(',')
            d[l[0]]=l[1]
            
        
    # with open(datadir+'minimerge.csv') as f:
    #     f.readline() # ignore first line (header)
    #     data = dict(csv.reader(f, delimiter=','))

     
    f = open("MNCH-project.ids",'r')
     
    for line in f:
        id = line
        print id
        #print d[line]
        
         

def main():
    #mnhc_report()
    scrape_mnhc()
    #simple_merge()
    #combine_hpds()
    #compare_headers()
    #load_postrges()

