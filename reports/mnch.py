#!/usr/bin/env python
# encoding: utf-8
"""
mnch.py

Created by Peder Jakobsen on 2014-01-12.

"""

import sys
import os
from petl import *

def dbdata():
    db='cidp'
    user='cidp_admin'
    con = psycopg2.connect(database=db, user=user) 
    cur = con.cursor()
    # Get a list of project ids
    sql = "select * from browser where project_number in (select full_project_number from project where id in (select project_id from initiative_project where initiative_id=1))"

    browser = fromdb(con,  sql)
    print look(browser)
    #browser = cut(browser, 'start_date','end_date','country','description','dac_sector','title', 'status', 'executing_agency_partner', 'maximum_cida_contribution')
    #return browser

def compare_iati_crs():
    '''
        A report to compare amounts found in CIDA with CRS and IATI
    '''

def report():
    ''' 
        1. Find project numbers that are part of MNCH 
        2. Find correspoding HDPS activities
        3. Add them up
     
    '''


def extra_projects():
    '''
    Some projects are not listed at CIDA, and are provided in a separate spreadsheet
    '''

def main():
	pass


if __name__ == '__main__':
	#dbdata()
    spent = fromcsv('mnch_spent.csv')
    print look(spent)