#!/bin/sh

# In order for Kettle to do a proper table analysis, we need all the records combined. 
# Also, select only Canadian records that contain "|301|Canada|" 

DIR=~/dev/cidp/data/crs/
echo ~/dev/cidp/data/crs/
#skip2  ${DIR}'hpds-2012.csv'


#grap the first line from any file
sed -n '1p' ${DIR}CRS_2012_data.csv >> ${DIR}canada_combined.csv
for file in ${DIR}CRS_*_data.csv
do
   echo $file
   tail -n+1 "$file" | grep "|301|Canada|" >> ${DIR}canada_combined.csv
   #echo >> final.csv
   
done
#TODO remove blank lines grep -v '^$' input.txt > output.txt
#iconv -f ASCII -t utf-8//IGNORE final.csv >  final_fixed_chars.csv
#rm final.csv
#mv final_fixed_chars.csv ${DIR}
