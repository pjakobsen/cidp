# encoding: utf-8
"""
crs.py

Created by Peder Jakobsen on 2014-01-04.

"""

import sys
import os
from petl import *
from pprint import pprint
import binascii
import psycopg2
import csv



basedir='/Users/peder/dev/cidp/data/crs/'

def csv_for_fusion():
    '''
    Prep CRS datafiles taken from combined CSV and make them smaller so they can be uploaded to 
    Fusion tables and comply with 100MB limit. 
    
    '''
    pass

def main():
    basedir='/Users/peder/dev/cidp/data/crs/'
    table = fromcsv(basedir+'canada_combined.csv', delimiter="|")
    pprint(header(table))

    table = cut(table, "Year", 'projecttitle','purposecode','purposename','bi_multi','donorcode','donorname', 'agencyname','recipientname','flowname','channelname','regionname','completiondate', 'crsid', 'projectnumber','commitment_national','disbursement_national')
    table = rename(table, "Year","year")
    pprint(header(table))
    tocsv(basedir+'cc_test.csv',table)
    # 
    # con = psycopg2.connect(database='cidp', user='peder') 
    # cur = con.cursor()
    
    

if __name__ == '__main__':
    main()

