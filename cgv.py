# cgv.py - Dana Toribio

import sys
import re
import graphviz

# create new python file
	# python filename: YYYYMMDD_computer_science.py
	# graphviz filename: YYYYMMDD_computer_science.gv

# write header info
# print('''# finalcgv.py - Curriculum Graph Visualizer''')
# print('''from graphviz import Digraph

# c = Digraph('test_ie', filename='test_ie.gv')
# c.attr('graph', fontname="Helvetica")
# c.attr('node', fontname="Helvetica")''')

# write legend
# write elective track
# write completed courses
# write suggestion 1 to n
# write major prerequisite tree
# write elective track's prerequisite associations
# write science/math elective subgraph print
# write legend print
# write view graph

# read in .dot file
f = open(sys.argv[1], 'r')

# course list to console
all_courses = []

class Track:

	def __init__(self, name):
		self.name = name
		self.courses = []
		self.prereq = []
		self.coreq = []

	def add_course(self, course):
		if course not in self.courses:
			self.courses.append(course)
			all_courses.append(course)

	def add_prereq(self, prereq, postreq):
		self.prereq.append([prereq, postreq])
		self.add_course(prereq)
		self.add_course(postreq)

	def add_coreq(self, prereq, coreq):
		self.coreq.append([prereq, coreq])
		self.add_course(prereq)
		self.add_course(coreq)

w = "# Major Prerequisite Tree"
x = '"CPSC 120" -> "CPSC 121" [priority]'
y = '"PHYS 225" -- "PHYS 225L"'

re_courses = re.compile('\w+\s\d+\w*')

core = Track("Major Prerequisite Tree")

# core.add_prereq("CPSC 120", "CPSC 121")
# core.add_prereq("CPSC 121", "CPSC 131")
# core.add_prereq("CPSC 240", "CPSC 440")
# core.add_prereq("CPSC 254", "CPSC 301")
# core.add_prereq("CPSC 254", "CPSC 351")
# core.add_prereq("CPSC 301", "CPSC 323")
# core.add_prereq("CPSC 301", "CPSC 335")
# core.add_prereq("CPSC 301", "CPSC 362")
# core.add_prereq("CPSC 311", "CPSC 315")
# core.add_prereq("CPSC 311", "CPSC 362")
# core.add_prereq("CPSC 335", "CPSC 481")
# core.add_prereq("CPSC 351", "CPSC 471")
# core.add_prereq("ENGL 101", "CPSC 311")
# core.add_prereq("CPSC 131", "CPSC 240")
# core.add_prereq("CPSC 131", "CPSC 254")
# core.add_prereq("CPSC 131", "CPSC 311")
# core.add_prereq("CPSC 131", "CPSC 332")
# core.add_prereq("MATH 150A", "MATH 150B")
# core.add_prereq("MATH 150B", "MATH 338")
# core.add_prereq("MATH 270A", "CPSC 240")
# core.add_prereq("MATH 270A", "MATH 270B")
# core.add_prereq("MATH 270B", "CPSC 335")
# core.add_prereq("MATH 338", "CPSC 335")
# print("track_name = " + core.name)
# print("courses = " + str(core.courses))
# print("prereq = " + str(core.prereq))

# for i in all_courses:
# 	print(i)

# file parser
for line in f:
	# # find tracks
	# if line.find('#') == 0:
	# 	print(line, end='')

	# find nodes or edges
	if '->' in line:
		core.add_prereq(re_courses.findall(line)[0], re_courses.findall(line)[1])
	elif '--' in line:
		core.add_coreq(re_courses.findall(line)[0], re_courses.findall(line)[1])
	elif line == '\n':
		continue
	# else:
	# 	print('node')
	# else:
	# 	print(line, end='')

print('\nAll courses in ' + str(core.name).upper() + ':\n')

course_list = []
for i in core.courses:
	if len(course_list) is not 6:
		course_list.append(i)
	else:
		print('{0:10s} {1:10s} {2:10s} {3:10s} {4:10s} {5:10s}'.format(course_list[0], course_list[1], course_list[2], course_list[3], course_list[4], course_list[5]))
		course_list = []

print('\nInput courses completed, separated by commas (ex. CPSC 120, MATH 150A):')

# convert to python graphviz

# generate graph