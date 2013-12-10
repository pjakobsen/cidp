#!/usr/bin/env python
# encoding: utf-8
"""
test.py

Created by Peder Jakobsen on 2013-12-10.
Test ETL data from start to finsih
"""

import sys
import os
from petl import *
import psycopg2
import ConfigParser
import cubes
import json
import urllib2
from pprint import pprint
from collections import Counter


def from_hdps(project_id):
    print "-----------  FROM HPDS FILES ---------"
    hpds=fromcsv('data/HDPS-2005-2012-eng.csv')
    hpds=skip(hpds,1)
    #print header(hpds)
    hpds = select(hpds, lambda rec: rec[1] == project_id)
    hpds=cut(hpds, 'Fiscal year','Project number','Amount spent')
    hpds=convert(hpds, 'Amount spent', float) # Get rid of the dollar sign
    hpds = aggregate(hpds, ['Fiscal year','Project number'], sum, 'Amount spent')
    hpds = unpack(hpds, 'key',['Fiscal year','Project number'])
    hpds = rename(hpds, 'value','Amount spent')
    hpds = cut(hpds, 'Fiscal year','Project number','Amount spent')
    print look(hpds)
    #return hpds
    
    
def from_mergefile(project_id):
    print "----------- AFTER MERGE WITH PROJECT BROWSER ---------"
    merge=fromcsv('data/fixed_chars.csv')
    merge=cut(merge, 'Fiscal year','Project number','Amount spent')
    hpds = select(merge, lambda rec: rec[1] == project_id)
    hpds= cut(hpds, 'Fiscal year','Project number','Amount spent')
    hpds= convert(hpds, 'Amount spent', float) # Get rid of the dollar sign
    hpds = aggregate(hpds, ['Fiscal year','Project number'], sum, 'Amount spent')
    hpds = unpack(hpds, 'key',['Fiscal year','Project number'])
    hpds = rename(hpds, 'value','Amount spent')
    hpds = cut(hpds, 'Fiscal year','Project number','Amount spent')
    print look(hpds)
	
def from_db(project_id):
    config = ConfigParser.RawConfigParser()
    config.read("../cida.ini")
    db= config.get("DataStore","db")
    user= config.get("DataStore","db_user")
    table_name = config.get("DataStore","db_table")
    try:
        print db,user,table_name
        con = psycopg2.connect(database=db, user=user) 

        cur = con.cursor()
        print "--------------  FROM POSTGRES  ------------- " + project_id
        sql = "SELECT project_number,fiscal_year,amount_spent from cida where project_number='{}'".format(project_id)
        sql = "SELECT SUM(amount_spent) from cida where project_number='{}'".format(project_id)
        
        print sql
        cur.execute(sql)
        for c in cur:
            print c

    except Exception, e:
        print e.pgerror
        print e

def from_cubes(project_id):
    cnt=Counter()
    print "--------------  FROM CUBE  ------------- " + project_id
    model = cubes.load_model("../../cida_model.json")
    ws = cubes.create_workspace("sql",model,url="postgres://localhost/crs")

    cube = model.cube("cida")

    browser = ws.browser(cube)

    cell = cubes.Cell(cube)
    cut = cubes.PointCut("project_number", [project_id])
    cut = cubes.PointCut("project_number", [project_id])
    cell2 = cell.slice(cut)
    result = browser.aggregate(cell2,drilldown =["fiscal_year","country_region_name","id"])
    
    for i,c in enumerate(result.cells):
        cnt[sum]+=c['amount_spent_sum']
        #print i,c['id'],project_id, c['fiscal_year'],c['country_region_name'],c['amount_spent_sum']
    print cnt[sum]
def from_api(project_id):
    print "--------------  FROM WEB SERVICE API  ------------- " + project_id
    base_url = 'http://localhost:7000/cube/cida/'
    url = "{}aggregate?cut=project_number:{}".format(base_url,project_id)
    data = json.load(urllib2.urlopen(url))
    pprint(data['summary']['amount_spent_sum'])
if __name__ == '__main__':
    from_hdps("A035207001")
    from_mergefile("A035207001") # 3232396
    from_db("A035207001")  #3232396.0
    from_cubes("A035207001")
    from_api("A035207001")
    



