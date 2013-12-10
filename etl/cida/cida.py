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
import ConfigParser
import messytables


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
  	# Combine HPDS files
    f = open("HDPS-2005-2012-eng.csv", "w")
    for subdir, dirs, files in os.walk("data/hdps"):
        for file in files:
            
            tempfile=open("data/hdps/" + file,'r')
            
            f.write(tempfile.read())
            tempfile.close()
    f.close()

def project_id_sets():
    browser = project_browser()
    print rowcount(browser)
    print rowcount(unique(browser,'project'))

def messy_guess():
    # guess column types using messytables.
    # this is not useful when every field is a string
    fh = open('data/fixed_merge.csv', 'rb')
    table_set = messytables.CSVTableSet(fh)
    # A table set is a collection of tables:
    row_set = table_set.tables[0]
    print row_set.sample.next()
    types = messytables.type_guess(row_set.sample, strict=True)
    
    pprint(types)   

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
    
    
    create_postgres_table()
    try:
        todb(table, con, table_name)
        print "-------------- Load OK: Testing one record -------------"
        cur.execute('SELECT * from projects where project_id=10000')
        r  = cur.fetchone()
        print r

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

def browser_ids():
    b = fromcsv("data/Project Browser English.csv")
    b=skip(b,1)
    b = cut(b,'Project Number')
    ids = skip(b,1)
    return [i for i, in ids]

def merged_ids():
    b = fromcsv("data/full_merge.csv")

    print header(b)
    ids = cut(b,"Project number")
    ids = skip(ids,1)
    return [i for i, in ids]

def joined_report():
    ids = merged_ids()
    print rowcount(ids)
    ids = skip(ids,1)
    u=[i for i in ids]
    print len(u)
    uniq = set(u)
    print len(uniq)



def join_test():
    '''


        Number of HPDS records:  247782
        Unique Project numbers in HPDS:  8252

        To ensure join is being properly performed, iterate through 
        project browser ids, and count the number of matching rows in 
        merged HDPS

    '''
    hpds=merged_ids()
    print "Number of HPDS records: ", len(hpds)
    print "Unique Project numbers in HPDS: ", len(set(hpds))
    brow=browser_ids()
    print "Unique Browser project numbers: ", len(set(brow))

    print "Intersection of IDs: ", len(set(hpds).intersection(set(brow)))
    print "Union of IDs: ", len(set(hpds).union(set(brow)))
    print "IDs in HDPS but not in Project Browser : ", len(set(hpds).difference(set(brow)))
    print "IDs in Project Browser, but not in HPDS : ", len(set(brow).difference(set(hpds)))

    # There must be some numbers in the Project Browser that is not the in HDPS
    ''' OUTPUT:

        Number of HPDS records:  247782  
        Unique Project numbers in HPDS:  8252
        Unique Browser project numbers:  2801
        Intersection of IDs:  2482
        Union of IDs:  8571
        IDs in HDPS but not in Project Browser :  5770
        IDs in Project Browser, but not in HPDS :  319

        Number of HPDS records after join:  19566  + 319 Projects 
        that are in Project browser but not in HDPS.  TOTAL: 19885 

        ---------------------------------------------

        Second time around: 

        Number of HPDS records:  90106
        Unique Project numbers in HPDS:  2801
        Unique Browser project numbers:  2801
        Intersection of IDs:  2801
        Union of IDs:  2801
        IDs in HDPS but not in Project Browser :  0

        This is a great test, because it means the merge was successful :)

        '''

def compare_headers():
    pb = skip(fromcsv(csvfiles['browser']),1)
    pb = header(rename(pb, 'Project Number', 'Project number'))
    hdps = header(skip(fromcsv(csvfiles['hdps-2012']),0))
    pprint(pb)
    pprint(hdps)
    s = set(pb).intersection(set(hdps) )
    pprint(s)
    
def merge_and_join():
    '''
        Some notes about these files:
        * There are 2801 records in the Project Browser file
        * Each project ID is unique eg. rowcount(b) == rowcount(unique(b,0))
        * We need all the rows from HDPS files that correspond to one of these project IDS
        * 

    '''
    b = fromcsv("data/Project Browser English.csv")
    # Skip first line, which contains publish data(?)
    # 'CIDA Project Browser - 2013-11-12 19:00:51 - all published projects'

    b = skip(b,1)
    # Rename key column to match HPDS files
    b = rename(b, 'Project Number', 'Project number')
    pprint(header(b))
    print rowcount(b)

    '''
    # cut some stuff out so it's easier to work with
    b1=cut(rowslice(b, 1,5),0,2,6,7,9)
    # Remove Description, Country, DAC Sector, Expected Results, Progress and Results Achieved'
    b2 = cutout(b,3,7,10,12,13)
    f = search(b2,'2013')
    print look(f)
    sys.exit()
    pprint(look(b1))
    '''

    #open hdps
    h = fromcsv("data/HDPS-2005-2012-eng.csv")
    h = skip(h, 1)
    pprint(header(h))
    
    h1=cut(rowslice(h, 1,5),1,2,47,49)
    print rowcount(h)
    print "---- Merging -----"
    j = rightjoin(h,b, "Project number")
    print rowcount(j)
    tocsv(j, "data/full_merge.csv")
    sys.exit()
    # Join them
    joined = outerjoin(h1, b1, key="Project number")  
    pprint(header(joined))
    pprint(look(joined,style='simple'))
    # Compare sizes
    print rowcount(b1),rowcount(h1),rowcount(joined)

def create_postgres_table(ini):

    config = ConfigParser.RawConfigParser()
    # dont' change  names to lower case
    config.optionxform = str
    config.read(ini)
    for name, type in config.items('FieldMap'):
        print type.split(" ")
   
    sql_fields = [type for (name,type) in config.items('FieldMap') if type != "DROP"]
    print sql_fields

    db= config.get("DataStore","db")
    user= config.get("DataStore","db_user")
    table_name = config.get("DataStore","db_table")
    print db,user,table_name
    
    try:
        con = psycopg2.connect(database=db, user=user) 
        #con = psycopg2.connect(database='cidp_dev', user='cidp') 
        #con.autocommit = True
        cur = con.cursor()
        
        # see if the table exists
        try:
            cur.execute("select * from information_schema.tables where table_name=%s", ('cida',))
            if bool(cur.rowcount):
                # drop table
                print "---------- Dropping table -----------"
                cur.execute("DROP TABLE cida")
                
        except:
            pass
            
        cur.execute("SET CLIENT_ENCODING TO 'iso-8859-1'")
        print cur
        cur.execute('SELECT version()')  
        print cur.fetchone()

        sql = "CREATE TABLE cida (id SERIAL PRIMARY KEY," + ", ".join(sql_fields) + " );"
        cur.execute(sql)
        #Not needed since automcommit is set to true: con.commit()
        con.commit()
    except Exception, e:

        print e.pgerror

def auto_load_postrges(csvfile, ini):
    
    table = fromcsv(csvfile)
    print len(header(table))
    # remove rows without title or amount
    #table = select(table, 'browser_title', lambda v: v != '')
    #table = select(table, 'amount', lambda v: v != '')
    config = ConfigParser.RawConfigParser()
    # dont' change  names to lower case
    config.optionxform = str
    config.read(ini)
    print "--------- Removing Fields and renaming ----------"

    for name, type in config.items('FieldMap'):
        new = type.split(" ")[0]
        if type == "DROP":
            print name
            table = cutout(table, name)
            
        else:
            table = rename(table, name, new)
    #FIXME
    table = cutout(table, "status")
    pprint (header(table))    
    print "--------- Renaming Done  ----------"  


    # http://pythonhosted.org/petl/0.11.1/#petl.convert
    #table = convert(table1, ('foo', 'bar', 'baz'), unicode)
    table1= convert(table)
    #table1 = convert(table1, 'maximum_cida_contribution', 'replace', '$ ', '') # Get rid of the dollar sign
    #table1 = convert(table1, 'maximum_cida_contribution', 'replace', ',', '') # Get rid of commas
    #table1['maximum_cida_contribution'] = 'replace', '$ ', ''

    table1['start_date'] = int
    table1['fiscal_year'] = lambda year: int(year.split("/")[1])
    #table1['fiscal_year'] = int
    table1['end_date'] = int
    table1['maximum_cida_contribution'] = float
    table1['amount_spent'] = float
    table1['untied_amount'] = float
 
    print look(cut(table1,"fiscal_year", "maximum_cida_contribution"),1000,1200)

    db= config.get("DataStore","db")
    user= config.get("DataStore","db_user")
    table_name = config.get("DataStore","db_table")
    try:
        print db,user,table_name
        con = psycopg2.connect(database=db, user=user) 

        cur = con.cursor()
        todb(table1, con, 'cida')
        print "-------------- Load OK: Testing one record -------------"
        cur.execute('SELECT * from cida where id=10000')
        r  = cur.fetchone()
        print r

    except Exception, e:
        print e.pgerror
        print e


def main():
    print "Use me when it's time to run everything in crontab"   
    
if __name__ == '__main__':
    create_postgres_table("../cida.ini")
    #merge_and_join()
	#joined_report()
	#manual_count()

    #combine_hpds()
    # May need to run 
    print "did you use: iconv -f ASCII -t utf-8//IGNORE fixed_merge.csv >  fixed_chars.csv"
    auto_load_postrges('data/fixed_chars.csv','../cida.ini')



