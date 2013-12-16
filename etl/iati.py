# encoding: utf-8

import os
import sys
import urllib
from pprint import pprint
from lxml import etree
from lxml import objectify
from data_sources import datadir
from petl import fromcsv, look, head


datadir="/Users/peder/dev/cidp/data/iati/datastore_files/"
def dowload_datastore_files():
    '''
    Transactions from the IATI Datastore
    '''
    base_url="http://iati-datastore.herokuapp.com/api/1/access/"
    command = "transaction/by_country.csv"
    urllib.urlretrieve(base_url+command,datadir+"transaction_by_country.csv")
    print "OK " + command
    
    
def transactions_to_db():
    '''
        Transactions from the IATI Datastore
    '''
    url = "http://iati-datastore.herokuapp.com/api/1/access/transaction/by_country.csv"
    

if __name__ == '__main__':
    #dowload_datastore_files()

