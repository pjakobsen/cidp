#!/usr/bin/env python
# encoding: utf-8
"""
hdps.py

Created by Peder Jakobsen on 2013-12-01.

"""

import sys
import os


def main():
	# Combine HPDS files
    f = open("HDPS-2005-2012-eng.csv", "w")
    for subdir, dirs, files in os.walk("data/hdps"):
        for file in files:
            
            tempfile=open("data/hdps/" + file,'r')
            
            f.write(tempfile.read())
            tempfile.close()
    f.close()


if __name__ == '__main__':
	main()

