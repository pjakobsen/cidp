#!/usr/bin/env python
# encoding: utf-8
"""

Created by Peder Jakobsen on 2013-12-05.

Example of using CUBE API to retrive information about healt projects

"""

import sys
import json
import urllib2
from pprint import pprint



def health_query():
    # We're interested in all health related sectors. First ask for all sectors
    url = "http://localhost:5000/aggregate?drilldown=sector"
    data = json.load(urllib2.urlopen(url))
    # Need to build a list of health sector names
    print [(c['sector'],c['record_count'],c['amount_sum']) for c in data['cells'] if 'ealth' in c['sector']]
    
    for d in health_data:
        print d
    
 

if __name__ == '__main__':
	health_query()

