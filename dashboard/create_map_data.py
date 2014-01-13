import sys
import os
import psycopg2
import json
from petl import *
from pprint import pprint
import datetime

db='cidp'
user='cidp_admin'
con = psycopg2.connect(database=db, user=user) 
cur = con.cursor()

def mnch_data():

    # Get a list of project ids
    sql = "select * from browser where project_number in (select full_project_number from project where id in (select project_id from initiative_project where initiative_id=1))"

    browser = fromdb(con,  sql)
    pprint(header(browser))
    return browser

def create_json(browser, ignore_multi=True):
    geo={}
    with open('../etl/geolocations.json') as f:
        for item in json.load(f):
            geo[item['country']]=(item['longitude'],item['latitude'])


    ''' This method won't work because we loose all the records that are not in the hpds because lack of spending '''
    #combo   = join(browser, spent, key='project_number')

    ''' 
        Create table with fields, totals, and geocode
        Some projects do not exist in hpds, so no totals.  
        Thus, we must iterate through browser data, and leave out totals  
    '''
   
    report = []
    for r in  dicts(browser):
        # Get amount spent if available
        try:
            ''' Get the sum from each project id from hpds '''
            historical = fromdb(con, "select project_number, fiscal_year, amount_spent, country_region_name,country_region_percent from hpds where project_number='%s'"%r['project_number'])
            '''
            We may have to igore multi country splits for now until further notice from Aniket:
            For example
            print look(spent)
            +------------------+-----------------------+-----------------------+--------------------------+
            | 'project_number' | 'amount_spent'        | 'country_region_name' | 'country_region_percent' |
            +==================+=======================+=======================+==========================+
            | 'S065348001'     | Decimal('474982.616') | 'Ethiopia'            | '0.71'                   |
            +------------------+-----------------------+-----------------------+--------------------------+
            | 'S065348001'     | Decimal('118745.654') | 'Ethiopia'            | '0.71'                   |
            +------------------+-----------------------+-----------------------+--------------------------+
            | 'S065348001'     | Decimal('194006.984') | 'Zimbabwe'            | '0.29'                   |
            +------------------+-----------------------+-----------------------+--------------------------+
            | 'S065348001'     | Decimal('48501.746')  | 'Zimbabwe'            | '0.29'                   |
            +------------------+-----------------------+-----------------------+--------------------------+
            
            So for now, ignore any projects that have anything other than '1' for 'country_region_percent'
            '''
            if ignore_multi:
                # Check for precense of percentages
                percentages=values(historical,'country_region_percent')
                if '1' not in percentages: 
                    continue
                else:
                    # This record is OK, use it
                    r['disembursed']= sum(values(historical,'amount_spent'))
                    r['country_region_name'] = values(historical,'country_region_name')[0]
                    r['geo']=list(geo[r['country_region_name']])
                    pprint(r)
                    # fix broken datatypes
                    for k,v in r.iteritems():
                        try:
                            r[k]=float(v)
                        except:
                            pass
                        try:
                            if type(v)==datetime.date: 
                                r[k]=str(v)
                        except:
                            pass
                    print "----------------"
                    
                    pprint(r)
                
                    report.append(r)
                    
            else:
                print "Uh-oh, more coding here"
                sys.exit()

        except Exception, e:
            print str(e)
            spent =0
        f = open('app/static/data/mnch_full.json','w')
        f.write(json.dumps(report)) # python will convert \n to os.linesep
        f.close()
        #pprint()
        #tojson(report, 'app/static/data/mnch_full.json')

if __name__ == '__main__':

	create_json(mnch_data())

