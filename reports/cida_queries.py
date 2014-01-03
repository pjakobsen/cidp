#!/usr/bin/env python
# encoding: utf-8
"""
mnch-projects.py

Created by Peder Jakobsen on 2013-11-11.

MNHC:  Maternal, Newborn and Child Health 
MNCH is a large signature initiative of the GoC. The PM who has taken personal interest in it.

 
Given the cuts etc. this signature area has been affected at all? 

It is a valid question. The answer (from other more aggregate data) in my opinion so far is no. i.e. 
MNCH hasn’t been affected and expenditure is as per commitments. 
Journalists looking for a story don’t want to hear this which I suppose is why they check with me first. 
 
There is another, related issue here, which is coding reliability. 
The main way development project data is “fudged around” for lack of a better term is by coding it slightly differently so it fits one category over the other. 
Or sometimes split across sectors. 
For us as data analysts this just creates headaches and I’d argue doesn’t add much to the overall analysis. So I told the journalists that may be worth looking into. There is no easy way to do that however but go through long description fields one by one. Since there aren’t that many in this case it may be possible, but I have not decided if I want to go that far for this little project.
 
The way I typically go about this, since there is no MNCH coding in any of the datasets (a major issue to begin with), is to first try to run an sql join on title. In fact  I ran this just now for a few test cases and it seemed to work. But it will only work if the title in the spreadsheet and our dataset is exactly the same.
 
You will notice that all the titles are links, and the link goes to the project page where all the other info is given. (This is PB info, not HPDS, but we can get that in our linked files as well, given we will have unique project nos.).
 
The main thing I’d like to see is whether using what you are developing we have any easier way to populate the other info for these projects alongside and generate a new sheet that builds on this; easier than the method I have already.
 
Cheers, thanks
 
Aniket   


"""

import sys
import os
import psycopg2
import csv
from petl import *

 # migrate table with pg_dump -t table_to_copy source_db | psql target_db


'''
Generate CSV files and JSON files from CIDA and othere datasets here.
Since the data does not change, no need to do it in the web app

'''
# Connect to the database so we can ask questions
db='cidp'
user='cidp_admin'
home = os.path.expanduser("~")
report_dir = home+'/dev/cidp/reports/'
# Put reports in the static dir so web app can use them 
live_dir='../dashboard/sandbox/app/static/data/'


def all_data():
    '''  show every project for every year with total amount spent '''
    try:
        
        con = psycopg2.connect(database=db, user=user) 
        cur = con.cursor()
        browser = fromdb(con, 'select * from browser')
        browser = cutout(browser, 'description','dac_sector','country','cida_sector_of_focus','expected_results', 'progress_and_results_achieved')
        print look(browser)
        spent = fromdb(con, 'select project_number, sum(amount_spent) from hpds group by project_number')
        print look(spent)
        spent = convert(spent, 'sum',lambda a: round(a,0))
        spent = rename(spent, 'sum', 'Total Spent')
        print look(spent)
        # now join the tables 
        report = table3 = join(browser, spent, key='project_number')
        print look(report)
        tocsv(report, 'all_totals.csv')
        sys.exit()
        
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e    
        sys.exit(1)

    finally:
        pass
    ''' Here it would be good to keep a log file '''


def mnhc():
   
    try:
        con = psycopg2.connect(database=db, user=user) 
        cur = con.cursor()
        
         # Get a list of mnhc projects
        cur.execute( "select full_project_number, project_name,url from project where id in (select project_id from initiative_project where initiative_id=1)")
        mnhc_ids=[]
        report = []
        report.append(('Project Number','Maximum Contribution', 'Amount Spent'  ,'Project URL'))
        for r in cur.fetchall():
  
            id = r[0] 
  
            sql="select maximum_cida_contribution, sum(amount_spent) from hpds where project_number = '%s' group by maximum_cida_contribution" % id
            
            cur.execute(sql)
            d = cur.fetchone()
            if d:
                max_contrib, amount_spent = d
            
            
            sql="select amount, region from projects where project = '%s'" % id

            cur.execute(sql)
            commitment = cur.fetchone()
            
            record = (id,max_contrib, float(amount_spent)  ,r[1],r[2])
            report.append(record)

    except psycopg2.DatabaseError, e:
        print 'Error %s' % e    
        #sys.exit(1)

    finally:
        pass
    ''' Here it would be good to keep a log file '''
   
    
    print report
    with open('mnhc.csv','w') as out:
        csv_out=csv.writer(out)
        for row in report:
            csv_out.writerow(row)

if __name__ == '__main__':
	all_data()

