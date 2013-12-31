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
home = os.path.expanduser("~")
data_dir = home+'/dev/cidp/data/'
hpds_dir =data_dir+'/hpds/'

def save_file(url,filename):
    path=None
    if "browser" in filename:
        path= os.path.normpath(data_dir+filename)
    else:
        path= os.path.normpath(hpds_dir+filename)
    try:
        urllib.urlretrieve(url, path)
        print "OK file ", path
    except:
        raise
    finally:
        print "---- OK ----"


def combine_hpds():
    # Combine HPDS files
    f = open(hpds_dir+"HDPS-2005-2012-eng.csv", "w")
    for subdir, dirs, files in os.walk(hpds_dir):
        for file in files:
            sourcefile=open(subdir+ file,'r')
            f.write(sourcefile.read())
            sourcefile.close()
    f.close()

def save_files():   
    save_file("http://www.acdi-cida.gc.ca/cidaweb/cpo.nsf/vLUOpenDataFile/PBOpenData/\$file/Project%20Browser%20English.csv","browser.csv")
    save_file("http://www.acdi-cida.gc.ca/INET/IMAGES.NSF/vLUImages/Open%20Data/\$file/HPDS-2011-2012-eng.csv","hpds-2012.csv")
    save_file("http://www.acdi-cida.gc.ca/INET/IMAGES.NSF/vLUImages/Open%20Data/\$file/HPDS-2010-2011-eng.csv","hpds-2011.csv")
    save_file("http://www.acdi-cida.gc.ca/INET/IMAGES.NSF/vLUImages/Open%20Data/\$file/HPDS-2009-2010-eng.csv","hpds-2010.csv")
    save_file("http://www.acdi-cida.gc.ca/INET/IMAGES.NSF/vLUImages/Open%20Data/\$file/HPDS-2008-2009-eng.csv","hpds-2009.csv")
    save_file("http://www.acdi-cida.gc.ca/INET/IMAGES.NSF/vLUImages/Open%20Data/\$file/HPDS-2007-2008-eng.csv","hpds-2008.csv")
    save_file("http://www.acdi-cida.gc.ca/INET/IMAGES.NSF/vLUImages/Open%20Data/\$file/HPDS-2006-2007-eng.csv","hpds-2007.csv")
    save_file("http://www.acdi-cida.gc.ca/INET/IMAGES.NSF/vLUImages/Open%20Data/$file/HPDS-2005-2006-eng.csv", "hpds-2006.csv")

if __name__ == '__main__':
    combine_hpds()
