# encoding: utf-8
"""
brewer.py

Created by Peder Jakobsen on 2013-11-05.

"""

import sys
import os
import pdb
import brewery

def main():
    URL = "projects.csv"

    b = brewery.create_builder()
    b.csv_source(URL,encoding="UTF8")
    b.audit(distinct_threshold=None)
    b.pretty_printer()

    b.stream.run()


if __name__ == '__main__':
    #pdb.set_trace()
    main()

