#!/usr/bin/env python
# encoding: utf-8
"""
create_database.py

Created by Peder Jakobsen on 2014-01-01.

See http://zetcode.com/db/postgresqlpythontutorial/

Create a User:
$createuser cidp_admin
Shall the new role be a superuser? (y/n) n
Shall the new role be allowed to create databases? (y/n) y
Shall the new role be allowed to create more new roles? (y/n) n

List databases:
psql -U peder -l

Drop cidp database if present:
dropdb cidp

The create again with owner

$ createdb cidp -O cidp_admin

"""

import sys
import os
import psycopg2
import ConfigParser



def main():
    
    '''  Create sql script to   database tables using cida.ini mappings (based on csv) and extra fields and contraints'''
    con = None
    
    config = ConfigParser.RawConfigParser()
    # dont' change  names to lower case
    config.optionxform = str
    config.read('cida.ini')
        
    sql_fields = [type for (name,type) in config.items('browser_FieldMap') if type != "DROP"] 
    browser_sql = "CREATE TABLE browser (id SERIAL PRIMARY KEY," + ", ".join(sql_fields) + " );"
    
    sql_fields = [type for (name,type) in config.items('hpds_FieldMap') if type != "DROP"]
    hpds_sql = "CREATE TABLE hpds (id SERIAL PRIMARY KEY, browser_id INT references browser(id), " + ", ".join(sql_fields) + " );"    

    try:

        con = psycopg2.connect(database='cidp', user='peder') 
        cur = con.cursor()

        cur.execute('SELECT version()')      
        
        ver = cur.fetchone()
        print ver    
        cur.execute("DROP TABLE IF EXISTS browser, hpds")  # Dropping simultaenously takes care of restraint
        
          
        cur.execute(browser_sql)
        cur.execute(hpds_sql)
        
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        con.commit()
        print cur.fetchall()
        con.commit()
        
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e    
        sys.exit(1)


    finally:
        
        if con:
            con.close()
    # Make a sql file
    os.system('pg_dump cidp --schema-only > create_cidp.sql')

if __name__ == '__main__':
	main()

