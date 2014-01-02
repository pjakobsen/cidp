#!/bin/sh

# Due this in a script instead of python to radically improve performance
# Count the number of lines


function skip2 () {
    # arguments to function are positional
    echo "Number of lines " in $1
    grep -c ^ $1
    echo "Number of lines after skipping two frist lines"
    tail -n+2 $1 | grep -c ^
}

DIR=~/dev/cidp/data/hpds/
echo ~/dev/cidp/data/hpds/
#skip2  ${DIR}'hpds-2012.csv'


#grap the first line from any file
sed -n '2p' ${DIR}hpds-2011.csv >> final.csv
for file in ${DIR}hpds-20*.csv
do
   echo $file
   
   tail -n+3 "$file" >> final.csv
   echo >> final.csv
   
done
TODO remove blank lines grep -v '^$' input.txt > output.txt
iconv -f ASCII -t utf-8//IGNORE final.csv >  final_fixed_chars.csv
rm final.csv
mv final_fixed_chars.csv ${DIR}
