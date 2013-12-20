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
from petl import *
import model
from model import *

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
	main()

