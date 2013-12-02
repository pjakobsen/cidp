#!/usr/bin/env python
# encoding: utf-8
"""
browser.py

Created by Peder Jakobsen on 2013-12-01.

"""
import sys
from messytables import CSVTableSet, type_guess, types_processor, headers_guess
from petl import fromcsv, header, skip, look, rename, outerjoin, rowcount, rowslice,cut
from pprint import pprint



def project_browser_to_postgres():
    b = fromcsv("data/Project Browser English.csv")
    # Skip first line, which contains publish data(?)
    # 'CIDA Project Browser - 2013-11-12 19:00:51 - all published projects'

    b = skip(b,1)
    # Rename key column to match HPDS files
    b = rename(b, 'Project Number', 'Project number')
    pprint(header(b))
    # cut some stuff out so it's easier to work with
    b1=cut(rowslice(b, 1,10),0,2,6,7,9)
    
    pprint(look(b1))

    #open hdps
    h = fromcsv("data/hpds/HPDS-2011-2012-eng.csv")
    pprint(header(h))
    h1=cut(rowslice(h, 1,5),1,2,47,49)
    
    pprint(look(h1))
    print len(header(h))
   
    # Join them
    joined = outerjoin(h1, b1, key="Project number")  
    pprint(header(joined))
    pprint(look(joined))
    # Compare sizes
    print rowcount(b1),rowcount(h1),rowcount(joined)

if __name__ == '__main__':
	project_browser_to_postgres()

