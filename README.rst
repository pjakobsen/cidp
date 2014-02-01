CIDP
-------------------------------------------
--------
The Data
--------

International Aid Transparency Initiative
-----------------------------------------

The IATI Datastore is an online service that gathers all data published to the IATI standard into a single queryable source. This can deliver selections of IATI data in JSON or XML formats, or CSV (spreadsheet) for less-technical users.

Info:  http://iatistandard.org/datastore/
API: http://iati-datastore.herokuapp.com/

----
Team
----

Aniket Bhushan, North South Institute, Project Lead  ABhushan@nsi-ins.ca

Michael Roberts, Groupsia, Community Dissemination, @michaeloroberts, mroberts10@gmail.com

Peder Jakobsen, Technical Architect, Software Developer, @pederjakobsen, pjakobsen@gmail.com


Goals
-----
The Canadian International Development Platform (CIDP) is a unique data and analytical platform on Canada’s engagement with the developing world. The CIDP is hosted by the North-South Institute, Canada’s only independent development policy think-tank. - See more at: http://cidpnsi.ca/#sthash.feYYCRsO.dpuf

Replacing Tableau with a more flexible and dynamic approach to building real time data dashboards.

Clean data, make it more open and transparent

Provide an API that wraps data in a uniform fashion that is is well documented so that other developers can build visualizations or apps, eg. mobile apps, or to be used at Hackathons

Engage the community

Data Integration
----------------
The term data integration refers to the process of combining data from different sources to provide a single comprehensible view on all of the combined data.

The Focus here is on Canadian International Development Data

The data will need to be normalized, which requires custom transformation work.

For example, the Country field from the CIDA Project Browser appears as:

.. code-block::

	"Venezuela: 8.37%,Argentina: 8.33%,Bolivia: 8.33%,Brazil: 8.33%,Chile: 8.33%,Colombia: 8.33%,Ecuador: 8.33%,Guyana: 8.33%,Peru: 8.33%,Paraguay: 8.33%,Suriname: 8.33%,Uruguay: 8.33%"

It will need to be split and applied against the total contribution amount in order to be used for dimensional OLAP queries.
Other tasks includes mapping country names against standard ISO country codes, especially when there are different names for the same country, e.g. Congo, Democratic Republic of Congo, Congo, Republic of etc. 

Since there are many dozens of such task that will have to managed in separate processes, an ETL framework will need to be selected to ensure that the transformation code is manageable.
Popular ETL/BI frameworks include Pentaho Kettle, Jaspersoft, SpagoBI, OpenI, and Actuate.


Definition of Platform (DMP)
----------------------------

A data management platform (DMP), also called a unified data management platform (UDMP) is a centralized computing system for collecting, integrating and managing large sets of structured and unstructured data from disparate sources.

An effective DMP creates a unified development and delivery environment that provides access to consistent, accurate and timely data. The term is most often associated with products and development projects that promise to help marketers and publishers turn data from offline, online, web analytics and mobile channels into information that can be used to support business goals. 

An expensive vendor DMP might combine data management technologies and data analytics tools into a single software suite with an intuitive and easy to navigate executive dashboard. At its simplest, a DMP could just be a NoSQL database management system that imports data from multiple systems and allows marketers and publishers to view data in a consistent manner.

Definition Source:  http://searchcio.techtarget.com/definition/data-management-platform-DMP

Community Dissemination
-----------------------

Archicture
----------

- PaaS platform:  Platform as a Service - Heroku
- ETL - Extract, Transform, Load - aggregating, cleaning, and normalizing data from various sources
- Data Warehousing - Postgres (?)
- API - wrapping the data as with a JSON based API
- Visualization Dashboard - improve the current CIDP 
	- Project-Level Open Aid Data Explorer
- Track - use analytics to track the use of platform and dashboard
- Source Code Management and developer collaboration platform (e.g. GitHUB)







