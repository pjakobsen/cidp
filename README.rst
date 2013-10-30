Canadian International Development Platform
-------------------------------------------

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

The Data
--------

The Focus is on Canadian International Development Data:

- CIDA Project Browser http://www.acdi-cida.gc.ca/acdi-cida/acdi-cida.nsf/eng/CAR-530122033-M6W
- CIDA Historical Project Datasets http://www.acdi-cida.gc.ca/acdi-cida/ACDI-CIDA.nsf/eng/CAR-1128144934-R9J
- Tracking Post-2015
- IATI Registry

More data could eventually be added from:

- OECD CRS
- World Bank
- etc. etc. 



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







