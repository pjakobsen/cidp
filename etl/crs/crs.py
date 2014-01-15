#!/usr/bin/env python
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

def main():

    table = fromcsv('/Users/peder/dev/cidp/data/crs/canada_combined.csv', delimiter="|")
    pprint(header(table))

    table = cut(table, "Year", 'projecttitle','purposecode','purposename','bi_multi','donorcode','donorname', 'agencyname','recipientname','flowname','channelname','regionname','completiondate', 'crsid', 'projectnumber','commitment_national','disbursement_national')
    table = rename(table, "Year","year")
    pprint(header(table))

    con = psycopg2.connect(database='cidp', user='peder') 
    cur = con.cursor()
    

if __name__ == '__main__':
    main()

