# mpt.py - Dana Toribio

import sys
import re
import graphviz

# create new python file
	# python filename: YYYYMMDD_computer_science.py
	# graphviz filename: YYYYMMDD_computer_science.gv

# write header info
# print('''# finalmpt.py - Curriculum Graph Visualizer''')
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

class Curriculum:

	def __init__(self):
		self.courses = []
		self.completed = []
		self.tracks = []

	def add_course(self, course):
		pass

	def add_completed(self, course):
		self.completed.append(course)

	def add_track(self, track):
		pass

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

w = '# Major Prerequisite Tree'
x = '"CPSC 120" -> "CPSC 121" [priority]'
y = '"PHYS 225" -- "PHYS 225L"'

re_courses = re.compile('\w+\s\d+\w*')

cgv = Curriculum()
mpt = Track('Major Prerequisite Tree')

# file parser
for line in f:
	# # find tracks
	# if line.find('#') == 0:
	# 	print(line, end='')

	# find nodes or edges
	if '->' in line:
		mpt.add_prereq(re_courses.findall(line)[0], re_courses.findall(line)[1])
	elif '--' in line:
		mpt.add_coreq(re_courses.findall(line)[0], re_courses.findall(line)[1])
	elif line == '\n':
		continue
	# else:
	# 	print('node')
	# else:
	# 	print(line, end='')

print('\nAll courses in ' + str(mpt.name).upper() + ':')

# print list of courses
for i, item in enumerate(sorted(mpt.courses), start=0):
	if i % 7 == 0:
		print()
	else:
		print('{0:10s}'.format(item), end=' ')

print('\n\nInput courses completed, type X to finish:\n')

# handles course completed input
def input_match(course):
	for i in course:
		if i in cgv.completed:
			print('> repeat info: ' + str(i))
		elif i in mpt.courses:
			cgv.add_completed(i)
		else:
			print('> does not exist: ' + str(i))

# course completed input & error check
course_completed = re_courses.findall(input().upper())
while len(course_completed) > 0:
	input_match(course_completed)
	course_completed = re_courses.findall(input().upper())

print('Completed Courses: ' + str(cgv.completed))

# convert to python graphviz

# generate graph