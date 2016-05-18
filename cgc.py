# cgc.py - Curriculum Graph Converter - Dana Toribio

import graphviz
import os
import re
import subprocess
import sys

re_courses = re.compile('\w+\s\d+\w*')	# regex for courses

header = r'''from graphviz import Digraph
g = Digraph('studyplan', filename='studyplan.gv')
g.attr('graph', fontname='Helvetica')
g.attr('node', fontname='Helvetica')'''
legend = r'''c0 = Digraph('cluster_0')
c0.body.append('label = "LEGEND"')
c0.body.append('color=lightgrey')
c0.node_attr.update(style='filled', color='white')
c0.edge_attr.update(color='white')
c0.node('Semester 6', color='plum')
c0.node('Semester 7', color='crimson')
c0.node('Semester 3', color='peachpuff')
c0.node('Semester 4', color='darkseagreen')
c0.node('Semester 5', color='lightblue')
c0.node('Completed', color='grey')
c0.node('Semester 1', color='pink')
c0.node('Semester 2', color='lightsalmon')
c0.node('Semester 8', color='chocolate')
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
c1.body.append('style=filled')
c1.body.append('labelloc = "b"')
c1.body.append('label = "'''
req_electives_footer = "c1.body.append('label = \""
trk_electives = r'''
c2 = Digraph('cluster_2')
c2.body.append('color=aliceblue')
c2.body.append('style=filled')
c2.body.append('labelloc = "b"')
c2.body.append('label = "'''
trk_electives_footer = "c2.body.append('label = \""
completed_courses = ''
suggestions = ''
core_courses = ''
elec_prereqs = ''

def node(value):
	return ".node('" + value + "')\n"

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

f = open('studyplan.txt', 'r')
nf = open('studyplan.py', 'w')
write_to = ''
legend_index = 0
legend_color = ['pink', 'lightsalmon', 'peachpuff', 'darkseagreen', 'lightblue', 'plum', 'crimson', 'chocolate', 'goldenrod']

for line in f:
	if ('#' in line.split(' ')) and ('Core' in line):
		write_to = 'core'
		core_courses = core_courses + '\n' + line
	elif ('#' in line.split(' ')) and ('required' in line):
		write_to = 'req_electives'
		req_electives = req_electives + line[2:-1] + '"\')\n' 
	elif ('Track' in line):
		write_to = 'trk_electives'
		trk_electives = trk_electives + line[2:-1] + '"\')\n'
	elif ('#' in line.split(' ')) and ('taken' in line):
		write_to = 'suggestions'
		suggestions = suggestions + '\n' + line + "g.attr('node', style='filled', color='grey')\n"
	elif ('#' in line.split(' ')) and ('semester' in line):
		write_to = 'suggestions'
		suggestions = suggestions + '\n' + line + "g.attr('node', style='filled', color='" + legend_color[legend_index] + "')\n"
		legend_index = legend_index + 1
	elif line is '\n':
		write_to = ''
	course = re_courses.findall(line)
	if write_to is 'core':
		if (course) and ('->' in line) and ('*' in line):
			core_courses = core_courses + 'g' + prereq_edge(course[0], course[1], True)
		elif (course) and ('--' in line) and ('*' in line):
			core_courses = core_courses + 'g' + coreq_edge(course[0], course[1], True)
		elif (course) and ('->' in line):
			core_courses = core_courses + 'g' + prereq_edge(course[0], course[1], False)
		elif (course) and ('--' in line):
			core_courses = core_courses + 'g' + coreq_edge(course[0], course[1], False)
		elif (course):
			core_courses = core_courses + 'g' + node(course[0])
	elif write_to is 'req_electives':
		if (course) and ('->' in line):
			req_electives = req_electives + 'c1' + prereq_edge(course[0], course[1], False)
		elif (course) and ('--' in line):
			req_electives = req_electives + 'c1' + coreq_edge(course[0], course[1], False)
		elif (course):
			req_electives = req_electives + 'c1' + node(course[0])
	elif write_to is 'trk_electives':
		if (course) and ('->' in line):
			trk_electives = trk_electives + 'c2' + prereq_edge(course[0], course[1], False)
		elif (course) and ('--' in line):
			trk_electives = trk_electives + 'c2' + coreq_edge(course[0], course[1], False)
		elif (course):
			trk_electives = trk_electives + 'c2' + node(course[0])
	elif (write_to is 'suggestions') and course:
		suggestions = suggestions + 'g' + node(course[0])
	else:
		pass

nf.write(header + '\n')
nf.write(legend + '\n')
nf.write(req_electives + '\n')
nf.write(trk_electives + '\n')
nf.write(suggestions + '\n')
nf.write(core_courses + '\n')
# write track prerequisites

# subgraph calls
nf.write('g.subgraph(c1)' + '\n')
nf.write('g.subgraph(c2)' + '\n')
nf.write('g.subgraph(c0)' + '\n')
nf.write('g.view()')

os.startfile('studyplan.py')