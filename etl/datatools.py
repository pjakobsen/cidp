#!/usr/bin/env python
# encoding: utf-8
"""
datatools.py

Created by Peder Jakobsen on 2013-12-02.

Automates a few things when receiving a new data source

"""

import sys
import os
import argparse
import ConfigParser
from petl import fromcsv, header, iterdata, rowslice,look,see

def create_config(csvfile,config_name):
    '''
        Creates a configuration file from a CSV file
    '''
    print csvfile
    var = ''
    try: 
        open(config_name+".ini")
        var = raw_input("This file already exists. Do you wish to continue? (Yes/No) ")
    except:
        pass
        

    if var == 'Yes':
        cfgfile = open(config_name+".ini", "w")
        examplefile = open(config_name+".example", "w")
    else:
        print "goodbye"
        sys.exit()
        

    c = fromcsv(csvfile)
    columns = header(c)
    it = iterdata(c)
    print it.next()
    examplefile.write(str(see(rowslice(c,2,3))))
    examplefile.close()


    # add the settings to the structure of the file, and lets write it out...
    Config = ConfigParser.ConfigParser()
    # dont' change  names to lower case
    Config.optionxform = str
    Config.add_section('FieldTypes')
    Config.add_section('FieldMap')
    for name in columns:
        #Config.set('FieldTypes',c)
        #print name
        new = name
        new = new.split("(", 1)[0].strip()
        # Connect words with underscore
        new = new.replace("/","_")
        new = new.replace(" ","_")
        new = new.replace("-","_")
        new = new.lower()
        # try to guess some of the names
        if "amount" in name: 
            print name
            Config.set('FieldMap',name, new + " FLOAT")
        else:
            print name
            Config.set('FieldMap',name, new + " VARCHAR(10)")
        
    Config.write(cfgfile)
    cfgfile.close()

def main():
	pass


if __name__ == '__main__':
 
    main_parser = argparse.ArgumentParser(add_help=False)
    main_parser.add_argument("-v", "--verbose", help="increase output verbosity", action='store_true')
    ckan_parser = argparse.ArgumentParser(parents=[main_parser])
    
    ckan_parser.add_argument('config', help='create a SQL config file', action='store')
    ckan_parser.add_argument("-f","--file", help="Make a config file for the data", action='store')
    ckan_parser.add_argument("-n","--name", help="Name of the config file", action='store')
    
    args = ckan_parser.parse_args()

    if args.config:
        create_config(args.file,args.name)
        

