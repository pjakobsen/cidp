'''

Query the AITI datastore, explore the results

Notes on searching for Canadian Data:
Use code lists at http://iatistandard.org/codelists/organisation/
Participating Canadian organization codes:

CA-1	CIDA	Canadian International Development Agency
CA-2	IDRC	International Development Research Centre
CA-31	EDC	    Export Development Corporation
CA-4	DF	    Department of Finance

Make query at IATI Datastore like:

http://iati-datastore.herokuapp.com/api/1/access/activity?transaction_provider-org=CA-1&limit=100

Although it has not been documented yet, you can also filter queries by attributes, for example

participating-org is not a particularly useful filter - can there be filters for each participating-org@role ? -- i.e.:

funding
extending
implementing
accountable

https://github.com/okfn/iati-datastore/issues/106
More info here https://github.com/okfn/iati-datastore/issues/121

'''
import json, requests
from pprint import pprint
import os,sys
from lxml import etree
from lxml import objectify
import urllib

def download_organization_files():
    #TODO: This should go in the database
    # Get a list of organizations
    url='http://www.iatiregistry.org/api/search/dataset?filetype=organisation&offset=0&limit=100'

    resp = requests.get(url=url)
    data = json.loads(resp.content)

    orgs = data['results']
    for org in orgs:
        url = "http://www.iatiregistry.org/api/rest/dataset/"+org
        print url
        resp = requests.get(url=url)
        data = json.loads(resp.content)
        urllib.urlretrieve(data['download_url'],"data/"+org+".xml")

def organization_report():
    path = r'iati_org_xml' 
    #parser = etree.XMLParser(remove_blank_text=True) 
    data = {}
    for dir_entry in os.listdir(path):
        dir_entry_path = os.path.join(path, dir_entry)
        if os.path.isfile(dir_entry_path):
            
            f =  open(dir_entry_path, "r")
            
            
            doc = etree.parse(f)
            # is it really an organization file?
            if doc.getroot().tag not  "iati-activities":
                
                #print dir_entry.split(".")[0],":", doc.getroot().tag
          
                try:    
                
                
                    #print doc.find("//iati-identifier").text
                    print "------------------", dir_entry_path
                    print doc.xpath('//name/text()')
                    print doc.xpath('//iati-identifier/text()')
                
                    #print etree.tostring(doc, pretty_print=True)
                
                except etree.XMLSyntaxError, e:
                
                    print dir_entry_path, e
                except:
                    print "---------------ERROR IN FILE", dir_entry_path
                    pass
                
organization_report()