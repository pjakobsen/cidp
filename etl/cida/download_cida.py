'''
A script that downloads files from cida and puts them in a local directory

Files required are described here:

http://cidpnsi.ca/blog/portfolio/open-aid-data-explorer-canadian-aid-projects-around-the-world/

Scroll down to :

"
Methodology and Data Sources

This visualization is based on two main data sources. The CIDA project browser (PB) and Historical Project Dataset (HPDS). We join these distinct but complementary sources on project number. Each project has a unique project ID number. Joining multiple sources using this approach avoids complications such as double counting, and other potential errors."

'''

import os

dowload_dir = os.normapth("~/temp/cida")


