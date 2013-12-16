#!/usr/bin/env python
# encoding: utf-8
"""
persist.py

Created by Peder Jakobsen on 2013-12-13.

"""

import sys
import os
from sqlalchemy import *
from datetime import datetime

def create_db():
    #metadata = MetaData('sqlite:///dev.sqlite')
    metadata = MetaData('postgres://localhost/crs')
    country_table = Table(
        'country', metadata,
        Column('id',Integer,primary_key=True), 
        Column('country_name', Unicode(40),unique=True, nullable=False), 
        Column('country_code', Unicode(3),unique=True,nullable=False), 
        Column('short_name', Unicode(40),unique=True))
    
    #See http://www.acdi-cida.gc.ca/acdi-cida/acdi-cida.nsf/eng/CAR-613134747-NVG
    project_table = Table(
        'project', metadata,
        Column('id', Integer, primary_key=True), 
        Column('project_number', Unicode(7), nullable=False),
        Column('sub_project_number', Unicode(3), nullable=False),
        Column('full_project_number', Unicode(10), nullable=False),
        Column('url', UnicodeText,nullable=False), 
        Column('project_name',Unicode(255), unique=False))
        
    '''
    activity_table = Table(
        'dd_country', metadata,
        Column('id', Integer, primary_key=True), 
        Column('country_name', Unicode(40),unique=True, nullable=False), 
        Column('country_code', Unicode(3),unique=True,nullable=False), 
        Column('short_name', Unicode(40),   unique=True))
    '''
    metadata.create_all()

 
if __name__ == '__main__':
    create_db()



