import bubbles
import sys

URL="projects.csv"
#URL = "http://www.acdi-cida.gc.ca/cidaweb/cpo.nsf/vLUOpenDataFile/PBOpenData/$file/Project%20Browser%20English.csv"

# Prepare list of stores, we just need one temporary SQL store

stores = {
    "target": bubbles.open_store("sql", "sqlite:///cida.db")
}

        


#p = bubbles.Pipeline(stores=stores)
p = bubbles.Pipeline()
p.source_object("csv_source", resource=URL,infer_fields=True)
p.field_filter(keep=["Project Number","Country"])


# We create a table
# Uncomment this line and see the difference in debug messages
#p.create("target", "data")

#p.distinct("Category")
p.pretty_print()
p.run()

