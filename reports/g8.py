#!/usr/bin/env python
# encoding: utf-8
"""
methodology.py

Created by Peder Jakobsen on 2013-12-19.

UofT Calculation Rules
http://www.g8.utoronto.ca/summit/2010muskoka/methodology.html

"""

import sys
import os
import ast
from petl import *
import model
from model import *
from pprint import pprint
from collections import Counter

def bilateral_codes():
    codes = fromcsv('bilateral_contribution_rates.csv')
    codes = convert(codes, 'percent',float)
    codes = dict(records(codes))
    return codes
    
def report():
    cnt_commit = Counter()
    cnt_spent = Counter()
    cnt_commit_multi = Counter()
    cnt_spent_multi = Counter()


    # 'ascii'
    table = fromcsv("crs_canada_2012.csv", dialect='excel', delimiter="|")
    #pprint(header(table))
    table = cut(table, "Year", 'projecttitle','purposecode','purposename','bi_multi','donorcode','donorname', 'agencyname','recipientname','flowname','channelname','regionname','completiondate', 'crsid', 'projectnumber','commitment_national','disbursement_national')
    table = rename(table, "Year","year")    
    c = valuecounter(table, 'bi_multi')
    print "Multilateral Records", c['3']
    print "Bilateral Records", c['1']

    # print len(records(table))
    # multi = selectis(table, 'bi_multi','3')    
    mnch_commit=0
    mnch_spent=0
    '''
    Grab amounts for each row in all 2012 records.
    Find out what corresponding code is.
    Apply rate for that code.
    Add to total for 2012
    
    '''
    multi_report=[]
    report=[]
    for row in records(table):
        try:
            b = row['bi_multi']
            code=row['purposecode']
            #print code
           
            
            try:
                c = round(ast.literal_eval(row['commitment_national'].strip())*10000000,2)
            except:
                
                c = 0
            try:
                d = round(ast.literal_eval(row['disbursement_national'].strip())*10000000,2)
            except:
                d =0
            if b=='3' and bilat_calcs[code]:
                percent=eval(bilat_calcs[code])
                cnt_commit_multi[code] += c
                cnt_spent_multi[code] += d
                multi_report.append({
                    'projectnumber':row['projectnumber'],
                    'code': row['purposecode'], 
                    'title': row['projecttitle'].split(" / ")[0], 
                    'committed': c, 
                    'disembursed': d,
                    'comp':percent,
                    'final_committed': c*(percent/100),
                    'final_disembursed': d*(percent/100)
                    })
                            
            elif b=='1' and bilat_calcs[code]:
                percent=eval(bilat_calcs[code])
                cnt_commit[code] += c
                cnt_spent[code] += d
                report.append({
                    'projectnumber':row['projectnumber'],
                    'code': row['purposecode'], 
                    'title': row['projecttitle'].split(" / ")[0], 
                    'committed': c, 
                    'disembursed': d,
                    'comp':percent,
                    'final_committed': c*(percent/100),
                    'final_disembursed': d*(percent/100)
                    })
                
                
        except SyntaxError:

            print "SyntaxError"
 

        except KeyError:
            "Not relevant"
        except:
            raise
    
    print "Multilateral Commitment: ",  sum(cnt_commit_multi.values())
    print  "Multilateral Disembursements: ", sum(cnt_spent_multi.values())      
    print "Bilateral Commitment: ", sum(cnt_commit.values())
    print "Bilateral Disembursements: ", sum(cnt_spent.values())
    r = fromdicts(report)
    print look(r)

    tocsv(r,'G8.csv')
    r = fromdicts(multi_report)
    tocsv(r,'G8-multi.csv')   
def reduce_table(table):
    table = cut(table, "Year", 'projecttitle','purposecode','purposename','bi_multi','donorcode','donorname', 'agencyname','recipientname','flowname','channelname','regionname','completiondate', 'crsid', 'projectnumber','commitment_national','disbursement_national')
    table = rename(table, "Year","year")   
    return table
    
def bilateral_report():
    '''
     Collect every data point that is Canadian 
     For each code, add all disembursements together
     Report should look like this:
     
     year, code, disembursement
    
    '''
    table = fromcsv("crs_canada_2012.csv", dialect='excel', delimiter="|")
     # create crs project objects
    #table = selectis(table,'donorname','Canada')
    table = reduce_table(table)
    codes = bilateral_codes()
    print look(table)
    for code in codes:
        print "---------{}---------".format(code)
        # Select all records with code
        t = selectis(table,'purposecode',str(code))
        print look(t)
        sys.exit()

def main():
    multilat = fromcsv('multilat-contrib.csv')
    print header(multilat)
    print look(multilat)
    
    k =  lookup(multilat,'agency_initiative','imputed_percent')
    
    print k['World Food Programme']
    doug = project()  
    doug.number_of_legs = 4  
    doug.count_legs()
    
if __name__ == '__main__':
	bilateral_report()

