#!/usr/bin/env python
# encoding: utf-8
"""
mnch-projects.py

Created by Peder Jakobsen on 2013-11-11.

MNHC:  Maternal, Newborn and Child Health 

Given the cuts etc. this signature area has been affected at all? 

It is a valid question. The answer (from other more aggregate data) in my opinion so far is no. i.e. 
MNCH hasn’t been affected and expenditure is as per commitments. 
Journalists looking for a story don’t want to hear this which I suppose is why they check with me first. 
 
There is another, related issue here, which is coding reliability. 
The main way development project data is “fudged around” for lack of a better term is by coding it slightly differently so it fits one category over the other. 
Or sometimes split across sectors. 
For us as data analysts this just creates headaches and I’d argue doesn’t add much to the overall analysis. So I told the journalists that may be worth looking into. There is no easy way to do that however but go through long description fields one by one. Since there aren’t that many in this case it may be possible, but I have not decided if I want to go that far for this little project.
 
The way I typically go about this, since there is no MNCH coding in any of the datasets (a major issue to begin with), is to first try to run an sql join on title. 
In fact  I ran this just now for a few test cases and it seemed to work. 
But it will only work if the title in the spreadsheet and our dataset is exactly the same.
 
You will notice that all the titles are links, and the link goes to the project page where all the other info is given. (This is PB info, not HPDS, but we can get that in our linked files as well, given we will have unique project nos.).
 
The main thing I’d like to see is whether using what you are developing we have any easier way to populate the other info for these projects alongside and generate a new sheet that builds on this; easier than the method I have already.
 
Cheers, thanks
 
Aniket   


"""

import sys
import os
from sqlalchemy import *
#from sqlalchemy.orm import sessionmaker



def main():
	# Connect to the database so we can ask questions
    engine = create_engine('postgres://localhost/crs')
    #engine.echo = True
    metadata = MetaData(engine)
    project_table = Table('project', metadata, autoload=True, autoload_with=engine)
    metadata.reflect(engine)
    print metadata.tables.keys()
    stmt = project_table.select(project_table.c.id=='1')
    print stmt.execute().fetchall()   
    sql = 'select * from project where project_id'
    result = engine.execute(sql)
    for  r in result.fetchall()[0:20]:
        print r

    

if __name__ == '__main__':
	main()

