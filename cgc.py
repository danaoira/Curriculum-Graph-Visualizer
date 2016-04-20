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
req_electives = r'''c1 = Digraph('cluster_1')
c1.body.append('color=aliceblue')
c1.body.append('style=filled')'''
req_electives_footer = "c1.body.append('label = \""
trk_electives = r'''
c2 = Digraph('cluster_2')
c2.body.append('color=aliceblue')
c2.body.append('style=filled')'''
trk_electives_footer = "c2.body.append('label = \""
completed_courses = ''
suggestions = ''
core_courses = ''
elec_prereq = ''

def prereq_edge(node1, node2, crit):
	if crit is True:
		return ".edge('" + node1 + "', '" + node2 + "', color='red')\n"
	else:
		return ".edge('" + node1 + "', '" + node2 + "')\n"

def coreq_edge(node1, node2, crit):
	if crit is True:
		return ".edge('" + node1 + "', '" + node2 + "', '', arrowhead='dot', arrowtail='dot', dir='both', color='red')\n"
	else:
		return ".edge('" + node1 + "', '" + node2 + "', '', arrowhead='dot', arrowtail='dot', dir='both')\n"

f = open(sys.argv[1], 'r')
nf = open('studyplan.py', 'w')
write_to = ''

for line in f:
	if ('#' in line.split(' ')) and ('Core' in line):
		write_to = 'core'
		core_courses = core_courses + '\n' + line
	elif ('#' in line.split(' ')) and ('required' in line):
		write_to = 'req_electives'
		req_electives = req_electives + '\n' + line
		req_electives_footer = req_electives_footer + line[2:-1] + "\"')"
	elif ('#' in line.split(' ')) and ('IE' in line):
		write_to = 'trk_electives'
		trk_electives = trk_electives + '\n' + line
		trk_electives_footer = trk_electives_footer + line[2:-1] + "\"')"
	elif line is '\n':
		write_to = ''
	if write_to is 'core':
		course = re_courses.findall(line)
		if (course) and ('->' in line) and ('*' in line):
			core_courses = core_courses + 'g' + prereq_edge(course[0], course[1], True)
		elif (course) and ('--' in line) and ('*' in line):
			core_courses = core_courses + 'g' + coreq_edge(course[0], course[1], True)
		elif (course) and ('->' in line):
			core_courses = core_courses + 'g' + prereq_edge(course[0], course[1], False)
		elif (course) and ('--' in line):
			core_courses = core_courses + 'g' + coreq_edge(course[0], course[1], False)
	elif write_to is 'req_electives':
		course = re_courses.findall(line)
		if (course) and ('->' in line):
			req_electives = req_electives + 'c1' + prereq_edge(course[0], course[1], False)
		elif (course) and ('--' in line):
			req_electives = req_electives + 'c1' + coreq_edge(course[0], course[1], False)
	elif write_to is 'trk_electives':
		course = re_courses.findall(line)
		if (course) and ('->' in line):
			trk_electives = trk_electives + 'c2' + prereq_edge(course[0], course[1], False)
		elif (course) and ('--' in line):
			trk_electives = trk_electives + 'c2' + coreq_edge(course[0], course[1], False)
	else:
		pass

nf.write(header + '\n')
nf.write(legend + '\n')
nf.write(req_electives + '\n')
nf.write(req_electives_footer + '\n')
nf.write(trk_electives + '\n')
nf.write(trk_electives_footer + '\n')
# write course suggestions
nf.write(core_courses + '\n')
# write track prerequisites
# write subgraph calls
nf.write('g.subgraph(c1)' + '\n')
nf.write('g.subgraph(c2)' + '\n')
nf.write('g.view()')

os.startfile('studyplan.py')