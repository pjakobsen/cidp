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
import sqlite3
import psycopg2
from petl.fluent import etl

datadir = ''
csvfiles = {'browser': datadir + 'browser.csv',
 'hdps-2012': datadir + 'hpds-2012.csv',
 'hdps-2011': datadir + 'hpds-2011.csv',
 'hdps-2010': datadir + 'hpds-2010.csv',
 'hdps-2009': datadir + 'hpds-2009.csv',
 'hdps-2008': datadir + 'hpds-2008.csv',
 'hdps-2007': datadir + 'hpds-2007.csv',
 'hdps-2006': datadir + 'hpds-2006.csv'}
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


def project_browser():
     rawfile = fromcsv(csvfiles['browser'])
     projects = skip(rawfile, 1)
     projects = rename(projects, 'Project Number', 'project')
     pprint(header(projects))
     projects = cut(projects, 'project', 'Title', 'Start', 'End')
     return projects
     # print look(projects)
     #    print '------------- HDPS ----------------'
     #    hdps2012 = fromcsv(csvfiles['hdps-2012'])
     #    hdps2012 = cut(projects, 'Project number', 'Title', 'Start', 'End')
     #    print look(hdps2012)
     #    
     #    t1, t2 = diffheaders(projects, hdps2012)
     #    joined = join(projects, hdps2012, key='Project number')
     #    print look(joined, 30)
     #    pprint(header(joined))


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
    
    merged = mergesort(csv['hdps-2012'], 
                         csv['hdps-2011'], 
                         csv['hdps-2010'], 
                         csv['hdps-2009'],           
                         csv['hdps-2008'],
                         csv['hdps-2007'],
                         csv['hdps-2006'], 
                        key='project')
    
   
    # Need to get title from Project browser
    # Count should be the same after performing this operation
    print rowcount(merged)
    browser = project_browser()
    joined = outerjoin(merged, browser, key="project")
    print rowcount(joined)
    print look(joined)
    tocsv(rowslice(joined), datadir + 'joined.csv')

def project_id_sets():
    browser = project_browser()
    print rowcount(browser)
    print rowcount(unique(browser,'project'))
    

def load_sqlite_db():
    ''' SQLite chokes on the character sets in the data, use Postgres instead'''
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
    '''
    Set up DB to run queries like:
    
    Currently running queries such as this:

    SELECT SUM(amount)  FROM projects where project = ‘M013354001’
    150,000,000

    SELECT SUM(amount)  FROM projects where project = ‘M013354002’
    70,000,000

    SELECT SUM(amount)  FROM projects where project like 'M01335400%'
    220,000,000
    '''
    
    fields = [    
                  'project_id serial primary key',
                  'year INT',
                  'amount FLOAT',
                  'continent VARCHAR(20)',
                  'cida_contrib VARCHAR(20)',
                  'org VARCHAR(100)',
                  'status VARCHAR(20)',
                  'br_country_id VARCHAR(20)',
                  'region VARCHAR(50)',
                  'project VARCHAR(10)',
                  'region_percent VARCHAR(10)',
                  'sector VARCHAR(100)',
                  'sector_id VARCHAR(10)',
                  'sector_percent VARCHAR(10)',
                  'browser_title VARCHAR(200)',
                  # 'browser_start_date  VARCHAR(100)',
                  # 'browser_end_date VARCHAR(100)'
                   ]
    table = fromcsv(datadir + 'joined.csv')
    table = rename(table, 'Title', 'browser_title')
    # table = rename(table, 'Start', 'browser_start_date')
    # table = rename(table, 'End', 'browser_end_date')
    table = cutout(table,"Start")
    table = cutout(table, "End")
    pprint(header(table))
    # remove rows without title
    table = select(table, 'browser_title', lambda v: v != '')
    table = select(table, 'amount', lambda v: v != '')
    for d in iterdata(table,0,1):
        if d[13]: print d
        
    print(look(tail(table)))
    
    
    table_name = 'projects'
    try:
        con = psycopg2.connect(database='cidp_dev', user='cidp') 
        cur = con.cursor()
        cur.execute("SET CLIENT_ENCODING TO 'iso-8859-1'")
	try: 
            cur.execute('DROP TABLE projects')
        except:
            pass   	
        sql = 'CREATE TABLE {} ({})'.format(table_name, ",".join(fields))
        try:
            cur.execute('SELECT version()')  
            print cur.fetchone()
            cur.execute(sql)
            con.commit()
            todb(table, con, table_name)
            print "-------------- Load OK: Testing one record -------------"
            cur.execute('SELECT * from projects where project_id=10000')
            r  = cur.fetchone()
            print r
        except Exception, e:
            print e.pgerror
    except Exception, e:
        print e.pgerror
        print e
    
    

def simple_merge():
    '''    Create a very simple CSV file that only has most essential fields from 3 sources:
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
    # try the above with the rowmapper function
    b = rename(b, 'End','year')
    pb = cut(b, 'project','amount','year')
    pb = addfield(pb, 'source', "PB")
    pb =convert(pb, 'year', int)
    pb =convert(pb, 'amount', float)
    m = fromcsv(datadir+'merged.csv')
    pprint (header(m))
    sys.exit()
    h=cut(m, 'project','amount','year')
    h =convert(h, 'year', int)
    h =convert(h, 'amount', float)
    hist = addfield(h, 'source', "HPDS")
    merged = mergesort(pb, hist, key='project')
    print rowcount(merged)
    print look(merged)
    #tocsv(merged, datadir+"minimerge.csv")

def compare_headers():
    pb = skip(fromcsv(csvfiles['browser']),1)
    pb = header(rename(pb, 'Project Number', 'Project number'))
    hdps = header(skip(fromcsv(csvfiles['hdps-2012']),0))
    pprint(pb)
    pprint(hdps)
    s = set(pb).intersection(set(hdps) )
    pprint(s)
    




def main():

    #combine_hpds()
    load_postrges()

