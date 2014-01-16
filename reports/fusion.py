#!/usr/bin/env python
# encoding: utf-8
"""
fusion.py

Created by Peder Jakobsen on 2014-01-15.

"""

import sys
import os
import requests

def main():
    
    '''
    https://www.googleapis.com/fusiontables/v1/query?sql=SELECT ROWID FROM tableId
        { WHERE <filter_condition> | <spatial_condition> { AND <filter_condition> }* }
    
    SELECT ROWID FROM tableId&key=your_API_key
    
    '''
    
    
    base = 'https://www.googleapis.com/fusiontables/v1/query?sql='
    sql_select = 'SELECT purposecode FROM'
    table = '1gcpnsCVQ9T5wbPSr_g6Tb1pqke15R71MBxN3w7w'
    key = 'AIzaSyCjwPywDZ386cghyi0V8-k4kmoM3iNrJOg'
    sql_conditions=''
    
    req = '{}{} {}?key={}'.format(base,sql_select,table,key,sql_conditions)
    print req
    r = requests.get(req)
    print r.text


if __name__ == '__main__':
    main()

