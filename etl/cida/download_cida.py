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
import urllib

urllib.urlretrieve("http://www.acdi-cida.gc.ca/cidaweb/cpo.nsf/vLUOpenDataFile/PBOpenData/\$file/Project%20Browser%20English.csv","browser.csv")
print "OK Browser file"
urllib.urlretrieve("http://www.acdi-cida.gc.ca/INET/IMAGES.NSF/vLUImages/Open%20Data/\$file/HPDS-2011-2012-eng.csv","hpds-2012.csv")
print "OK 2012"
urllib.urlretrieve("http://www.acdi-cida.gc.ca/INET/IMAGES.NSF/vLUImages/Open%20Data/\$file/HPDS-2010-2011-eng.csv","hpds-2011.csv")
print "OK 2011"
urllib.urlretrieve("http://www.acdi-cida.gc.ca/INET/IMAGES.NSF/vLUImages/Open%20Data/\$file/HPDS-2009-2010-eng.csv","hpds-2010.csv")
print "OK 2010"
urllib.urlretrieve("http://www.acdi-cida.gc.ca/INET/IMAGES.NSF/vLUImages/Open%20Data/\$file/HPDS-2008-2009-eng.csv","hpds-2009.csv")
print "OK 2009"
urllib.urlretrieve("http://www.acdi-cida.gc.ca/INET/IMAGES.NSF/vLUImages/Open%20Data/\$file/HPDS-2007-2008-eng.csv","hpds-2008.csv")
print "OK 2008"
urllib.urlretrieve("http://www.acdi-cida.gc.ca/INET/IMAGES.NSF/vLUImages/Open%20Data/\$file/HPDS-2006-2007-eng.csv","hpds-2007.csv")
print "ALL OK"


