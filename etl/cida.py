import sys  
from pprint import pprint
from petl import *
from petl.fluent import etl

datadir="/Users/peder/dev/cidp/";
csvfiles = { "browser":datadir+"Project Browser English.csv",
         "hdps-2012":datadir+"HPDS-2011-2012-eng.csv",
         "hdps-2011":datadir+"HPDS-2010-2011-eng.csv",
         "hdps-2010":datadir+"HPDS-2009-2010-eng.csv",
         "hdps-2009":datadir+"HPDS-2008-2009-eng.csv",
         "hdps-2008":datadir+"HPDS-2007-2008-eng.csv"}

         
fieldmap=  {'Fiscal year':'year',
                    'Project number':'project',
                    'Status':'status',
                    'Maximum CIDA contribution (project-level)':'cida_contrib',
                    'Organisation name':'org',
                    'Continent name':'continent',
                    'Project Browser country ID':'br_country_id',
                    'Country/region name':'region',
                    'Country/region percent':'region_percent',
                    'Sector name':'sector',
                    'Sector ID':'sector_id',
                    'Sector percent':'sector_percent',
                    'Amount spent':'amount'}

def combine_hdps():
    pprint (header(fromcsv(csvfiles['hdps-2012'])))
    #sys.exit()
    # Utility for cleaning up tables
    def cutem(key,value):
        c = fromcsv(value)
        # some fiels have the date in the first line which needs to be skipped
        if "Date created" in "".join(header(c)):
            c = skip(c,1)     
        c = cut(c,fieldmap.keys())
        c = rename(c,fieldmap)
        return key,c
        
    # Turn file locations into petl.io.CSVView objects
    csv=dict(cutem(key,value) for key, value in csvfiles.items())

    print look(csv['hdps-2012'])
    print look(csv['hdps-2011'])
    merged = mergesort(csv['hdps-2012'], csv['hdps-2011'], key='project')
    print "-----------"
    print look(merged)
    
    

def project_browser():
    
    rawfile = fromcsv(csvfiles['cida-project-browser'])

    projects=skip(rawfile,1)
    # Now we have to rename 'Project Number' field to 'Project number' so we can do a join
    projects = rename(projects,'Project Number','Project number')
    pprint(header(projects))
    projects = cut(projects,"Project number","Title",'Start','End')
    print look(projects)
    print "------------- HDPS ----------------"
    hdps2012 = fromcsv(csvfiles['hdps-2012'])
    hdps2012 = cut(projects,"Project number","Title",'Start',"End")
    print look(hdps2012)
    sys.exit()
    t1,t2 = diffheaders(projects,hdps2012)
    joined = join(projects, hdps2012, key='Project number')
    print look(joined)
    pprint(header(joined))
    #tocsv(joined, datadir+'test.csv')
    #print h1
    #print look(hdps2012)
    
def main():
    combine_hdps()
