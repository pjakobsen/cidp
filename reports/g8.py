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
import locale


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
    table = fromcsv("/Users/peder/dev/cidp/data/crs/h.csv", dialect='excel', delimiter="|")
    pprint(header(table))
    sys.exit()
    #table = fromcsv("crs_canada_2012.csv", dialect='excel', delimiter="|")
     # create crs project objects
    #table = selectis(table,'donorname','Canada')
    table = reduce_table(table)
    codes = bilateral_codes()
    report_2011=[]
    report_2012=[]
    for code,value in codes.iteritems():
        print code,value
        # Select all records with code
        t = select(table,lambda rec: rec[2] == code)
        purposename=values(t,'purposename')[0]
        t = values(t,'disbursement_national')
        for n in t:
            print float(n)
        amount = round(sum([float(a) for a in t])*1000000,0)
        adjusted = amount * (float(value)/100)
        
        report.append({'purposename':purposename,'code':code, 'amount': amount, 'rate':value, 'adjusted':adjusted})
        
    rep=fromdicts(report)
    print look(rep)
    


def main():
    multilat = fromcsv('multilat-contrib.csv')
    print header(multilat)
    print look(multilat)
    
    k =  lookup(multilat,'agency_initiative','imputed_percent')
    
    print k['World Food Programme']
    doug = project()  
    doug.number_of_legs = 4  
    doug.count_legs()
    
def g8_report_from_csv(mnch_exclude=False):
    bilaterals_g8=[]
    multilaterals_g8=[]
    
    
    bilat_codes = bilateral_codes()
    
    bilat_counter=Counter()
    titles=[]
    bilateral=[]
    multilateral=[]
    projectnumbers=[]
    # Eliminate records with cat  f.csv | grep -v "2009|301" -a  >> g.csv
    table = fromcsv("/Users/peder/dev/cidp/data/crs/h.csv", delimiter="|")  
    pprint(header(table))

    mnch=fromcsv('../etl/mnch/mnch_secret.csv')
    print look(mnch)
    print header(mnch)
    print len(mnch)
    print len(set(mnch))
    #sys.exit()
    mnch_ids=values(mnch,'Project Number')
    #print mnch_ids
    for row in records(table):
        # skip any records not from CIDA
        if row[3] != '1':
            
            continue
        elif row['projectnumber'] in mnch_ids and mnch_exclude:
            
            continue 
        else:
            titles.append(row['projecttitle'].split(" / ")[0])
            projectnumbers.append(row['projectnumber'])
            #print row['Year'], row['projectnumber'],row['bi_multi'],row['usd_disbursement'], row['purposecode'],  row['projecttitle']
            #print ">> " , row['usd_disbursement']
            
            try:
                amount = float(row['usd_disbursement'])
                if row['bi_multi'] == '1': 
                    bilateral.append(amount)
                    # NOW THE MEAT
                        
                    if row['purposecode'] in bilat_codes:
                        bilat_counter[row['purposecode']]+=1
                        bilaterals_g8.append((row['purposecode'],row['usd_disbursement']))
                elif row['bi_multi'] == '3':
                    multilateral.append(amount)
            except ValueError:
                pass
            
    print "-----TITLES--------"
    print len(titles)
    print len(set(titles))
    
    print "-----PROJECT NUMBERS--------"
    print len(projectnumbers)
    print len(set(projectnumbers))
    
    print "--------TOTAL SUMS----------"
    print "Bilateral Disembursements Total:", sum(bilateral)
    print "Multilateral Disembursements Total:", sum(multilateral)
    
    print "-------------- Bilateral Project Codes ---------------"
    print list(bilat_counter)
    
    print "-------------- Bilateral Totals  ---------------"
    bi_total=[]
    for r in bilaterals_g8:
        percent = float(bilat_codes[r[0]])/100
        a = float(r[1]) * percent
        bi_total.append(a)
    print sum(bi_total)

def multilateral_spending():
    table=fromcsv('../etl/mnch/crs_multilat_spending.csv')
    print header(table)
    for row in records(table):
        print row['Sector Recipient']#,row['G8rate']
 
def fusion_report():
    
    table = fromcsv("data/crs dac kc 2011 2012-summary.csv")
    print header(table)
    t2011=selecteq(table,'Year','2011')
    t2012=selecteq(table,'Year','2012')
    print look(t2011)
    print look(t2012)
    #for r in records(table):
    

    def dollars(a, sumit=False):
            mult=1000000
            if sumit:
                t = int(round(sum(a)*mult,0))
            else:
                t = int(round(a*mult,0))

            locale.setlocale( locale.LC_ALL, '' )
            return locale.currency( t, grouping=True )
    
    def fast_count(t,y):
        amounts = [float(r['SUM(usd_disbursement)']) for r in records(t) if r['purposecode'] in  bilateral_codes()]
        g8_amounts = [float(r['SUM(usd_disbursement)'])*(bilateral_codes()[r['purposecode']]/100) for r in records(t) if r['purposecode'] in  bilateral_codes()]
           
        print y, "Total Spending for MNCH Purposecodes\t", dollars(amounts,True)
        print y, "Total Spending with G8 formula applied\t", dollars(g8_amounts,True)
        print "------"
        
    
    def full_report(t):
        report=[]
        for k,v in bilateral_codes().iteritems():

            r = selecteq(t,'purposecode',k)
            l = records(r)[0]
            full=dollars(float(l[4]))
            
            g8=dollars(float(l[4])*(v/100))
            report.append({'code':l[0],'name':l[1],'full_amount':full, 'g8_amount':g8, 'rate':v})
        
        #pprint(report)
        rep=fromdicts(report)
        #print look(rep)
        #reorder columns
        rep2 = cut(rep,2,3,1,4,0)
        print lookall(rep2)
        
        
    print "\n\n\n\n"
    print "<h2>{}</h2>".format('2011')
    full_report(t2011)
    print "<h2>{}</h2>".format('2012')
    full_report(t2012)
    
    fast_count(t2011, "2011")
    fast_count(t2012, "2012")
    
if __name__ == '__main__':
    fusion_report()
    #bilateral_report()
	#g8_report_from_csv()
	#multilateral_spending()

