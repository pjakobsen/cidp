# encoding: utf-8
"""
petl.py

Created by Peder Jakobsen on 2013-11-05.

"""



from petl import fromcsv,look
from data_sources import data

def main():
    
    table1 = fromcsv(data['cida-projects'])
    print look(table1)


if __name__ == '__main__':
	main()

