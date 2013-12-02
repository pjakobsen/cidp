++++++++++++++++++
Using the CIDP API
++++++++++++++++++

The API is located at http://cidp.herokuapp.com

This API uses JSON: 

Looking at API Meatadata, the structure of the API:
---------------------------------------------------

The best way to examine the result is to install JSONView for Chrome
or to use python json mtool

It is a cube model. You can examine the cube by asking the OLAP server for it's application model:

http://cidp.herokuapp.com/model

You can also get a list of the cubes.  Each data source has a cube

http://cidp.herokuapp.com/model/cubes

So far, the model contains only 1 cube, projects. 

http://cidp.herokuapp.com/model/cube/projects

Projects have 5 dimensions:

http://cidp.herokuapp.com/model/cube/projects/dimensions

"project",
"year",
"amount",
"continent",
"sector"

You can look at a single dimension:

http://cidp.herokuapp.com/model/dimension/sector

http://cidp.herokuapp.com/model/dimension/sector

Browsing and Aggregation
------------------------

/cube/<cube_name>/<browser_action> where the browser action might be aggregate, facts, fact, dimension and report.

For example: 

http://cidp.herokuapp.com/cube/projects/aggregate

http://cidp.herokuapp.com/cube/projects/aggregate?drilldown=continent