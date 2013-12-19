#!/usr/bin/env python
# encoding: utf-8
"""
cfo.py

Created by Peder Jakobsen on 2013-12-18.
Compare CFO data with other datasets

Their TOTAL 632,583,555.87 D82 =SUM(D4:F80)

57.5%   =D82/1100000000

* Global Fund to Fight AIDS, Tuberculosis and Malaria (GFATM) only counts as 46% towards Muskoka according to the Methodology for Calculating Baselines and Commitments: G8 Member Spending on Maternal, Newborn and Child Health 
* 2012/2013 figures are preliminary and subject to change following further quality assurance.

"""

import sys
import os
import locale
from petl import *
from pprint import pprint
from sqlalchemy import *
from collections import Counter
from jinja2 import Template

def main():
    cnt = Counter()
    
    engine = create_engine('postgres://localhost/crs')
    conn = engine.connect()
    
    cfo_file = "/Users/peder/dev/cidp/data/cfo.csv"
    cfo = fromcsv(cfo_file)
    pprint(header(cfo))
    cfo_ids=columns(cfo)['project_number']


    print "How many project ids ", len(cfo_ids)
    print "Are they all unique?", len(set(cfo_ids))

    result =conn.execute("select full_project_number from project").fetchall()
    db =  [row[0] for row in result]
    
    print "Number of project Ids ", len(db)
    print "Are they unique ", len(set(db))
    
    db_result =conn.execute("select full_project_number from project where id in (select project_id from initiative_project where initiative_id=1)").fetchall()
    musk=[row[0] for row in db_result]
    print "Number of project Ids ", len(musk)
    print "Are they unique ", len(set(musk))
    
    print "Is Muskoka a subset of  cfo? ", set(musk).issubset(set(cfo))
    print "Is CFO  subset of  Master DB? ",  set(cfo_ids).issubset(set(db))
    diff = set(cfo_ids).difference(set(musk))
    print "New Projecst in CFO not in Muskoka", diff
    diff = set(cfo_ids).difference(set(db))
    print "New Projecst in CFO not in Master DB", diff
    #print set(cfo).symmetric_difference(set(musk))
    
    print db[0:1]
    
    act =conn.execute("select project_number from activity").fetchall()
    iati=[row[0] for row in act]
    print "Number of project ids in activities ", len(iati)
    print "Are they unique ", len(set(iati))
    
    print "Is CFO  subset of  IATI? ",  set(cfo_ids).issubset(set(iati))
    diff = set(cfo_ids).difference(set(iati))
    print "New Projecst in CFO not in IATI", diff
    cfo = fromcsv(cfo_file)
    print header(cfo)
    for c in cfo:
        if c[1] in diff: print c[1],c[2] 
        
  
    print look(cfo)
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    cfo = convert(cfo, '2010-11',lambda c: 0 if c == '' else locale.atof(c))
    cfo = convert(cfo, '2011-12', lambda c: 0 if c == '' else locale.atof(c))
    cfo = convert(cfo, '2012-13', lambda c: 0 if c == '' else locale.atof(c))

    print look(cfo)
    cfo2 = addfield(cfo, 'total', expr('{2010-11} + {2011-12} + {2012-13}') )
    print look(cfo2)
    result =conn.execute("select project_number, maximum_cida_contribution from cida").fetchall()
    
    contrib = dict(result)

    def cida_numbers(pid):
        # Just keeping this here to illustrate the use of lambda with method
        r = lambda x: 0 if not contrib[pid] else contrib[pid]
        return r
 
    cfo3 = addfield(cfo2, 'commitment', lambda rec: contrib[rec['project_number']])
    
    cfo3 = addfield(cfo3, 'target %', lambda rec: 0 if not rec['commitment'] else "{0:.0f}%".format((rec['total'] / rec['commitment'])*100))
    print look(cfo3)
    #commitments list by country
    #breakdown by country
    
    
    sys.exit()
    print "--------------The Numbers--------------"
    
    print '2011-12', stats(cfo, '2011-12')
    print '2012-13', stats(cfo, '2012-13')
    foo =  '99'
    cfo11 =  stats(cfo, '2010-11').values()

    cfo11 = 'Entries: {0} Min: {2}  Max: {3}  Total: {4}'.format(*cfo11)

    data = {
        'cfo1':cfo11,
        'cfo11':stats(cfo, '2010-11'),
        'yy':'3000'}
        
    print data
    template = '''        
------------ Quick Report ------------- 
CFO Dataset:   
    Number of Projects: 78
        2011: {cfo1}
                2012:
                2013:
        
---------------------------------------
        
    '''.format(**data)
   
    print template
    
    template = Template('''
    
    Hello {{ name }}
    '''
    )
    foo =template.render({
        'knights':  'we say nih',
        'spam':     'and eggs',
        'name':'woowoow'
    })
    
    print foo

if __name__ == '__main__':
	main()

