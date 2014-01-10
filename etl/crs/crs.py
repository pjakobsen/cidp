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
import codecs
import csv
from BeautifulSoup import BeautifulSoup



def to_hex(t, nbytes):
    "Format text t as a sequence of nbyte long values separated by spaces."
    chars_per_item = nbytes * 2
    hex_version = binascii.hexlify(t)
    num_chunks = len(hex_version) / chars_per_item
    def chunkify():
        for start in xrange(0, len(hex_version), chars_per_item):
            yield hex_version[start:start + chars_per_item]
    return ' '.join(chunkify())

def fixfile():
    cd = codecs.open('/Users/peder/dev/cidp/data/crs/CRS_2012_data.csv', 'rU', 'utf-16','ignore')
    #cd = open('/Users/peder/dev/cidp/data/crs/2011-fix2.csv')

    lines = cd.readlines()

    out = open('foo.csv','w')
    out.write(lines[0])

    for i,l in enumerate(lines):
        if "|Canada" in l:
            out.write(l.encode('utf-8'))
            print i

def guess_encode():

    for l in  cd:
        soup = BeautifulSoup(l)
        print soup.contents[0]
        print soup.originalEncoding
        
        
def main():

    # 'ascii'
    table = fromcsv("foo.csv", dialect='excel', delimiter="|")
    pprint(header(table))

    table = cut(table, "Year", 'projecttitle','purposecode','purposename','bi_multi','donorcode','donorname', 'agencyname','recipientname','flowname','channelname','regionname','completiondate', 'crsid', 'projectnumber','commitment_national','disbursement_national')
    table = rename(table, "Year","year")
    pprint(header(table))
    #print look(table)
    con = psycopg2.connect(database='cidp', user='peder') 
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS crs3")
    sql = '''CREATE table crs3 (id SERIAL PRIMARY KEY, 
        year TEXT,
        projecttitle TEXT,
        purposecode TEXT, 
        purposename TEXT,
        bi_multi TEXT,
        donorcode TEXT, 
        donorname  TEXT, 
        agencyname  TEXT, 
        recipientname TEXT,
        flowname TEXT,
        channelname TEXT,
        regionname TEXT,
        completiondate TEXT,
        crsid TEXT,
        projectnumber TEXT,
        commitment_national TEXT,
        disbursement_national TEXT
    
    );'''
    try:
        cur.execute(sql)
        #cur.execute("SELECT crs2 FROM information_schema.tables WHERE table_schema = 'public'")
        con.commit()
        #print cur.fetchall()
    except:
        raise
    
    todb(table, con, 'crs3')

if __name__ == '__main__':
    report()
    #foo()
	#main()
    # print to_hex('abcdef', 1)
    # print to_hex('abcdef', 2)

