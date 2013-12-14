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
    metadata = MetaData('sqlite:///tutorial.sqlite')
    user_table = Table(
        'tf_user', metadata,
        Column('id', Integer, primary_key=True), 
        Column('user_name', Unicode(16), unique=True, nullable=False), 
        Column('password', Unicode(40), nullable=False), 
        Column('display_name', Unicode(255), default=u''), 
        Column('created', DateTime, default=datetime.now))
    group_table = Table(
        'tf_group', metadata,
        Column('id', Integer, primary_key=True), 
        Column('group_name', Unicode(16),unique=True, nullable=False))
    permission_table = Table(
        'tf_permission', metadata,
        Column('id', Integer, primary_key=True), 
        Column('permission_name', Unicode(16),unique=True, nullable=False))
    user_group_table = Table(
        'tf_user_group', metadata,
        Column('user_id', None, ForeignKey('tf_user.id'),
        primary_key=True),
        Column('group_id', None, ForeignKey('tf_group.id'),
        primary_key=True))
    group_permission_table = Table(
        'tf_group_permission', metadata,
        Column('permission_id', None, ForeignKey('tf_permission.id'),
        primary_key=True),
        Column('group_id', None, ForeignKey('tf_group.id'),
        primary_key=True))
    
    metadata.create_all()
    
    stmt = user_table.insert()
    stmt.execute(user_name=u'rick', password=u'secret', display_name=u'Rick Copeland')
    stmt.execute(user_name=u'rick1', password=u'secret', display_name=u'Rick Copeland Clone')

def devdata_db():
    metadata = MetaData('sqlite:///devdata.sqlite')
    country_table = Table(
        'dd_country', metadata,
        Column('id', Integer, primary_key=True), 
        Column('country_name', Unicode(40),unique=True, nullable=False), 
        Column('country_code', Unicode(3),unique=True,nullable=False), 
        Column('short_name', Unicode(40),   unique=True))
    metadata.create_all()
 

def main():
    engine = create_engine('sqlite:///devdata.sqlite')
    engine.echo = True
    connection = engine.connect()
    metadata = MetaData(engine)
    meta = MetaData()
    meta.reflect(bind=engine)
    for table in reversed(meta.sorted_tables):
        print table
    country = Table('dd_country', metadata, autoload=True, autoload_with=engine)
    print [c.name for c in country.columns]
    

    stmt = country.insert()
    stmt.execute(id='1', country_name='Canada', country_code='KC',short_name="Canuck")

if __name__ == '__main__':
    #create_db()
    #devdata_db()
    main()

