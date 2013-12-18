================
MNCH Data Report
================
MNHC:  Maternal, Newborn and Child Health Initiative aka the Muskoka Initiative

MNCH is a large signature initiative of the GoC. The PM has taken personal interest in it.
An overview of the initiative can be found at http://www.acdi-cida.gc.ca/acdi-cida/acdi-cida.nsf/eng/FRA-127113657-MH7

-------------------------------------------
Where can we find data about MNCH projects?
-------------------------------------------

1.  MNHC Project List
---------------------

So, what projects are part of MNCH?

Sadly, the only way to obtain this information is to scrape the following page for project links:

http://www.acdi-cida.gc.ca/cidaweb/cpo.nsf/fWebProjListEn?ReadForm&profile=SMNE-MNCH

It provides a set of links to each project page in the form:

http://www.acdi-cida.gc.ca/cidaweb/cpo.nsf/vWebProjSearchEn/0055DF5B1DCB32BC85257AB1003B23F6

Then navigate to each page to obtain project information in the form:

<div class="cpodata">A035564-001</div>, 
<div class="cpodata">$20,000,000</div>, 
<div class="cpodata"><a class="external" href="http://www.unicef.org">UNICEF - United Nations Children's Fund</a></div> 
<div class="cpodata">Operational</div>, 
<div class="cpodata">2013-03-28 — 2015-03-31</div>

All we need is the project ID so we can use it to query the project browser datasets.

To do this, you must collect the information manually or use a programming language with a 
HTML scraping library to automate the task.   The ids are saved in a list for later use (mnch.ids)

If all goes well, you will end up with a list like this:

A035564-001
M013707-001
A035496-001
A035243-003
A035262-001
...etc


2.  Project Browser information
-------------------------------

Using each ID, we can now find project information from the project browser.

For example:

A035564-001


This is most easily done by using grep on the project file itself:

~/dev/cidp/data$ cat "Project Browser English.csv" | grep "A035564"

The same result can be achieved by using "Search" in your favourite text editor or Excel

The basic information tells us that:
"A035564001","2013-05-27","2013","2015","Mali: 100%","UNICEF - United Nations Children's Fund","Basic sanitation(014032): 75%,Basic drinking water supply(014031): 25%","$ 20,000,000"

To  obtain information in the aggregate, you would have to programatically make a list of all the projects
matching the ids in the mhch.ids file


3. HPDS - Historical Project Data Sets	
--------------------------------------

Using the same method, we can now search the HPDS files.  But in the case of A035564, there is no information since the project began in 2013

4. IATI Activity File
---------------------

cat activity_ca-3.csv | grep "A035564"  we do find an activity:

With a many to many table you can now do something like:

select * from project where id in (select project_id from initiative_project where initiative_id=1)




