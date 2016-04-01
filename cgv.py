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

w = "# Major Prerequisite Tree"
x = '"CPSC 120" -> "CPSC 121" [priority]'
y = '"PHYS 225" -- "PHYS 225L"'

re_courses = re.compile('\w+\s\d+\w*')

cgv = Curriculum()
mpt = Track("Major Prerequisite Tree")

# mpt.add_prereq("CPSC 120", "CPSC 121")
# mpt.add_prereq("CPSC 121", "CPSC 131")
# mpt.add_prereq("CPSC 240", "CPSC 440")
# mpt.add_prereq("CPSC 254", "CPSC 301")
# mpt.add_prereq("CPSC 254", "CPSC 351")
# mpt.add_prereq("CPSC 301", "CPSC 323")
# mpt.add_prereq("CPSC 301", "CPSC 335")
# mpt.add_prereq("CPSC 301", "CPSC 362")
# mpt.add_prereq("CPSC 311", "CPSC 315")
# mpt.add_prereq("CPSC 311", "CPSC 362")
# mpt.add_prereq("CPSC 335", "CPSC 481")
# mpt.add_prereq("CPSC 351", "CPSC 471")
# mpt.add_prereq("ENGL 101", "CPSC 311")
# mpt.add_prereq("CPSC 131", "CPSC 240")
# mpt.add_prereq("CPSC 131", "CPSC 254")
# mpt.add_prereq("CPSC 131", "CPSC 311")
# mpt.add_prereq("CPSC 131", "CPSC 332")
# mpt.add_prereq("MATH 150A", "MATH 150B")
# mpt.add_prereq("MATH 150B", "MATH 338")
# mpt.add_prereq("MATH 270A", "CPSC 240")
# mpt.add_prereq("MATH 270A", "MATH 270B")
# mpt.add_prereq("MATH 270B", "CPSC 335")
# mpt.add_prereq("MATH 338", "CPSC 335")
# print("track_name = " + core.name)
# print("courses = " + str(core.courses))
# print("prereq = " + str(core.prereq))

for i in all_courses:
	print(i)

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

print('\nAll courses in ' + str(mpt.name).upper() + ':\n')

# print list of courses
for i, item in enumerate(mpt.courses, start=0):
	if i % 7 == 0:
		print()
	else:
		print('{0:10s}'.format(item), end=' ')
	# if len(course_list) is not 6:
	# 	course_list.append(i)
	# else:
	# 	print('{0:10s} {1:10s} {2:10s} {3:10s} {4:10s} {5:10s}'.format(course_list[0], course_list[1], course_list[2], course_list[3], course_list[4], course_list[5]))
		# course_list = []

print('\nInput courses completed, type X to finish:\n')

def input_match(course):
	if course in mpt.courses:
		cgv.add_completed(course)
	elif course == 'X':
		pass
	else:
		print("Error")

# course completed input & error check
course_completed = input().upper()
input_match(course_completed)
while not course_completed == "X":
	course_completed = input().upper()
	input_match(course_completed)
print(cgv.completed)
	



# convert to python graphviz

# generate graph