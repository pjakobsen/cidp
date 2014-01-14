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


basedir='/Users/peder/dev/cidp/data/crs/'
def utf_fix(file):
    file = basedir+file
    new_filename=file.replace(" ","_")
    infile = codecs.open(file, encoding='utf-16') # open file for appending
    outfile = open(new_filename,"a") # open file for appending

    for i,line in enumerate(infile.readlines()):
    #     if i==0:continue
    #     if i==2:
    #         for n,l in enumerate(line):
    #             try:
    #                 print l
    #                 print repr(l)
    #                 print l.decode('utf-8')
    #                 print "---------",n
    #             except:
    #                 print "ERROR",n
    #                 print l
    #                 pass
        #if i==0:continue
        #if i==1:continue
        #print repr(line)
        #print line
        try:
            nl = line[:-3].encode('utf-8')
            
            outfile.write(nl+"\n")
            print i, " OK"
        except:
            print i, " FAIL"
  
            raise
        

    infile.close()
    outfile.close()
    #Now use fromcsv("foo.csv", dialect='excel', delimiter="|")

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
    utf_fix('CRS 2008 data.txt')
    utf_fix('CRS 2009 data.txt')
    utf_fix('CRS 2010 data.txt')
    utf_fix('CRS 2011 data.txt')
    utf_fix('CRS 2012 data.txt')
    #report()
    #foo()
	#main()
    # print to_hex('abcdef', 1)
    # print to_hex('abcdef', 2)

