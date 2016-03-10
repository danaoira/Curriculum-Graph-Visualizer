# cgv.py - Dana Toribio

import sys
import graphviz

# read in .dot file

f = open(sys.argv[1], 'r')

for line in f:
	if line.find('->') > 0:
		print('TRUE')
	else:
		print(line, end='')

# convert to python graphviz 

# generate graph