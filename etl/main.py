# encoding: utf-8
"""
petl.py

Created by Peder Jakobsen on 2013-11-05.

"""
import sys  
from petl import *
from petl.fluent import etl


datadir="/Users/peder/dev/cidp/";
cida = { "cida-project-browser":datadir+"Project Browser English.csv",
         "hdps-2012":datadir+"HPDS-2011-2012-eng.csv",
         "hdps-2011":datadir+"HPDS-2010-2011-eng.csv",
         "hdps-2010":datadir+"HPDS-2009-2010-eng.csv",
         "hdps-2009":datadir+"HPDS-2008-2009-eng.csv",
         "hdps-2008":datadir+"HPDS-2007-2008-eng.csv"}

def cida():
    
    projects_raw = fromcsv(cida['cida-project-browser'],skip)
    projects = skip(projects_raw,1)
    # Now we have to rename 'Project Number' field to 'Project number' so we can do a join
    
    #print look(projects)
    hdps2012 = fromcsv(data['hdps-2012'])
    pprint(header(projects))
    pprint(header(hdps2012))
    t1,t2 = diffheaders(projects,hdps2012)
    both = join(projects, hdps2012, key='Project number')
    print look(both)
    
    #print h1
    #print look(hdps2012)

if __name__ == '__main__':
    cida()

	

