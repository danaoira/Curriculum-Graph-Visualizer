# cgc.py - Curriculum Graph Converter - Dana Toribio

import graphviz
import os
import re
import subprocess
import sys

re_courses = re.compile('\w+\s\d+\w*')	# regex for courses

header = r'''from graphviz import Digraph
g = Digraph('studyplan', filename='studyplan.gv')'''
legend = r'''c0 = Digraph('cluster_0')
c0.body.append('color=lightgrey')
c0.node_attr.update(style='filled', color='white')
c0.edge_attr.update(color='white')
c0.node('Semester 6', color='plum')
c0.node('Semester 7')
c0.node('Semester 3', color='peachpuff')
c0.node('Semester 4', color='darkseagreen')
c0.node('Semester 5', color='lightblue')
c0.node('Completed', color='grey')
c0.node('Semester 1', color='pink')
c0.node('Semester 2', color='lightsalmon')
c0.node('Semester 8')
c0.edge('Semester 6', 'Semester 7')
c0.edge('Semester 7', 'Semester 8')
c0.edge('Semester 3', 'Semester 4')
c0.edge('Semester 4', 'Semester 5')
c0.edge('Completed', 'Semester 1')
c0.edge('Semester 1', 'Semester 2')
c0.body.append('label = "LEGEND"')
'''
req_electives = ''
trk_electives = ''
completed_courses = ''
suggestions = ''
core_courses = ''
elec_prereq = ''

def prereq_edge(node1, node2):
	return "g.edge('" + node1 + "', '" + node2 + "')\n"

def coreq_edge(node1, node2):
	return "g.edge('" + node1 + "', '" + node2 + "', '', arrowhead='dot', arrowtail='dot', dir='both')\n"

f = open(sys.argv[1], 'r')
nf = open('studyplan.py', 'w')
write_to = ''

for line in f:
	if ('#' in line.split(' ')) and ('Core' in line):
		write_to = 'core'
		core_courses = core_courses + line
		continue
	elif ('#' in line.split(' ')):
		write_to = ''
	if write_to == 'core':
		course = re_courses.findall(line)
		if (course) and ('->' in line):
			core_courses = core_courses + prereq_edge(course[0], course[1])
		elif (course) and ('--' in line):
			core_courses = core_courses + coreq_edge(course[0], course[1])
	else:
		pass


# major prerequisite tree
# c.edge('CPSC 120', 'CPSC 121')
# c.edge('CPSC 121', 'CPSC 131')

nf.write(header + '\n')
nf.write(core_courses)
nf.write('g.view()')
os.startfile('studyplan.py')