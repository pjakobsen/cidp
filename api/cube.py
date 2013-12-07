'''

Cubes is all about facts.  A fact is a data cell in the cube, and cube is a collection of the facts
A face is something that is measurable, like a contract. 
A dimension is the context for the fact, location, time, type
Who signed the contract, how much was spent on the construction work, and where the transaction happen.

Also, cubes supports hierchies. So you can define levels for each dimension, eg. year month, day, or continent, continent, city

Levels and attributes
Hierarchy
Key Attributes
Label Attributes

"Multi-dimensional breadcrumbs"

'''
import sys
import cubes
from pprint import pprint
from itertools import islice

model = cubes.load_model("../cida_model.json")

#postgres://jdcqogwzkevwog:8z47cIJBDcBM3mefOiYfPVNBXy@ec2-23-23-177-33.compute-1.amazonaws.com:5432/de652in13m1noa
ws = cubes.create_workspace("sql",model,url="postgres://localhost/crs")

cube = model.cube("cida")

browser = ws.browser(cube)

cell = cubes.Cell(cube)
#cell = cell.slice("year", [2010])
result = browser.aggregate(cell, drilldown=["project_number"])
pprint(result.cells)
for i,c in enumerate(result.cells):
    print i
    pprint(c)

'''
print result.summary["record_count"]
print result.summary["amount_sum"]
result = browser.aggregate(cell, drilldown=["project"])
#for record in islice(result.cells,3,18):
for record in result.drilldown:
    pprint(record)
# result = browser.aggregate(drilldown=["continent"])    
# result = browser.aggregate(drilldown=["sector"])   
result = browser.aggregate(drilldown=["sector"])   
print result.summary
'''
print "--------------------"
