#!/usr/bin/env python
# encoding: utf-8
"""
cfo.py

Created by Peder Jakobsen on 2013-12-18.
Compare CFO data with other datasets

Their TOTAL 632,583,555.87 D82 =SUM(D4:F80)

57.5%   =D82/1100000000

* Global Fund to Fight AIDS, Tuberculosis and Malaria (GFATM) only counts as 46% towards Muskoka according to the Methodology for Calculating Baselines and Commitments: G8 Member Spending on Maternal, Newborn and Child Health 
* 2012/2013 figures are preliminary and subject to change following further quality assurance.

"""

import sys
import os
from petl import *
from pprint import pprint
from sqlalchemy import *

def main():
    
    engine = create_engine('postgres://localhost/crs')
    conn = engine.connect()
    
    cfo_file = "/Users/peder/dev/cidp/data/cfo.csv"
    cfo = fromcsv(cfo_file)
    pprint(header(cfo))
    cfo=cut(cfo, "project_number")
    cfo=skip(cfo,1)
    cfo= [i[0] for i in cfo]
    print cfo

    print "How many project ids ", len(cfo)
    print "Are they all unique?", len(set(cfo))

    result =conn.execute("select full_project_number from project").fetchall()
    db =  [row[0] for row in result]
    
    print "Number of project Ids ", len(db)
    print "Are they unique ", len(set(db))
    
    db_result =conn.execute("select full_project_number from project where id in (select project_id from initiative_project where initiative_id=1)").fetchall()
    musk=[row[0] for row in db_result]
    print "Number of project Ids ", len(musk)
    print "Are they unique ", len(set(musk))
    
    print "Is Muskoka a subset of  cfo? ", set(musk).issubset(set(cfo))
    print "Is CFO  subset of  Master DB? ",  set(cfo).issubset(set(db))
    diff = set(cfo).difference(set(musk))
    print "New Projecst in CFO not in Muskoka", diff
    diff = set(cfo).difference(set(db))
    print "New Projecst in CFO not in Master DB", diff
    #print set(cfo).symmetric_difference(set(musk))
    
    print db[0:1]
    
    act =conn.execute("select project_number from activity").fetchall()
    iati=[row[0] for row in act]
    print "Number of project ids in activities ", len(iati)
    print "Are they unique ", len(set(iati))
    
    print "Is CFO  subset of  IATI? ",  set(cfo).issubset(set(iati))
    diff = set(cfo).difference(set(iati))
    print "New Projecst in CFO not in IATI", diff
    cfo = fromcsv(cfo_file)
    for c in cfo:
        if c[1] in diff:
            print c[1],c[2] 
    
if __name__ == '__main__':
	main()

