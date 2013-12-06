ETL Module (Extract, transform, load)
-------------------------------------

Usage
-----

python main.py

Postgres Problems on OS X?

virtualenv your_virtual_env_name
. your_virtual_env_name/bin/activate
export ARCHFLAGS="-arch i386 -arch x86_64"
export PATH=$PATH:/Library/PostgreSQL/9.1/bin
pip install psycopg2

Migrata Data to Heroku
----------------------

Export local database:


pg_dump -Fc --no-acl --no-owner -h localhost -U peder crs > dbexport.dump
scp -P 7822  dbexport.pgsql jakobsen@a2s64.a2hosting.com:~/public_html/data/
heroku pgbackups:restore HEROKU_POSTGRESQL_COBALT_URL 'http://www.jakobsen.ca/data/dbexport.pgsql'

heroku run bash 
heroku pg to see databases




Data Sources
------------

CIDA Project Browser
http://www.acdi-cida.gc.ca/cidaweb/cpo.nsf/vLUOpenDataFile/PBOpenData/$file/Project%20Browser%20English.csv

------------
What is ETL?
------------

Typical ETL use cases:

Extract
-------
Read databases through a generic DB-API adapter.
Read flat files through a similar adapter.
Read spreadsheets through a similar adapter.
Cleanse.
Arbitrary rules
Filter and reject
Replace
Add columns of data
Profile Data.
Statistical frequency tables.

Transform (and Cleanse)
-----------------------
Do dimensional conformance lookups.
Replace values, or add values.
Aggregate.
At any point in the pipeline

Load
----
Or prepare a flat-file and run the DB product's loader.
Further, there are some additional requirements that aren't single use cases.

Each individual operation has to be a separate process that can be connected in a Unix pipeline, with individual records flowing from process to process. This uses all the CPU resources.

You need some kind of time-based scheduler for places that have trouble reasoning out their ETL preconditions.

You need an event-based schedule for places that can figure out the preconditions for ETL processing steps.

Note. Since ETL is I/O bound, multiple threads does you little good. Since each process runs for a long time -- especially if you have thousands of rows of data to process -- the overhead of "heavyweight" processes doesn't hurt.

Source:  http://stackoverflow.com/users/10661/s-lott


Occasional experimental transformation script uses the bubbles framework.  It requires python 3, so it's necessary to switch to a virtualenv that is based on python 3.3

To set up a virtualenv using python 3 instead of default 2.7, pass the -p flag to virtualenv, in this case via Doug Hellmans virtualenvwrapper script :

mkvirtualenv -p /usr/local/bin/python3 my_py3_env