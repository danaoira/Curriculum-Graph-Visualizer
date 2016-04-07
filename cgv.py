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

re_courses = re.compile('\w+\s\d+\w*')

f = open(sys.argv[1], 'r')

class Node(object):

	def __init__(self, data):
		self.data = data
		self.priority = False
		self.units = 0
		self.children = []

	def add_child(self, obj):
		self.children.append()

	def priority(self):
		self.priorty = True

courses = []
tracks = []
elective = 0
completed = []

for line in f:
	if '## Major:' in line:
		major = line[10:-1]
		break

print('\nAll elective tracks in ' + str(major) + ':\n')

# find elective tracks
for line in f:
	if '##' in line:
		pass
	elif ('required' not in line) and ('#' in line):
		tracks.append(line[2:-1])

# print elective tracks
for i, item in enumerate(tracks, start=1):
	print('[' + str(i) + '] ' + item)

print('\nSelect ONE elective track:')

# user input for elective track
try:
	elective = int(input())
except:
	print('\nInvalid input, please try again:')
	elective = int(input())

elective = tracks[elective-1]

f = open(sys.argv[1], 'r')

# toggle to read courses for user's study plan
read = False

# read courses for user's study plan
for line in f:
	if ('required' in line) or (elective in line):
		read = True
	elif '#' in line:
		read = False
	elif read is True and re_courses.findall(line):
		if re_courses.findall(line)[0] not in courses:
			courses.append(re_courses.findall(line)[0])
		try:
			if re_courses.findall(line)[1] not in courses:
				courses.append(re_courses.findall(line)[1])
		except:
			pass

print('\nAll courses in ' + str(major) + ':')

# print list of courses
for i, item in enumerate(sorted(courses), start=0):
	if i % 7 == 0:
		print()
	else:
		print('{0:10s}'.format(item), end=' ')

print('\n\nInput courses completed, type X to finish:\n')

# handles course completed input
def input_match(course):
	for i in course:
		if i in completed:
			print('> repeat info: ' + str(i))
		elif i in courses:
			completed.append(i)
		else:
			print('> does not exist: ' + str(i))

# course completed input & error check
course_completed = re_courses.findall(input().upper())
while len(course_completed) > 0:
	input_match(course_completed)
	course_completed = re_courses.findall(input().upper())

print('Completed Courses: ' + str(completed))

	# # # find title
	# # if 'Title:' in line:
	# # 	print(line.split('# Title: ')[1])
	# # 	# cgv.set_name = line[9:]
	# # # find tracks
	# # if '#' in line:
	# # 	pass

	# # # find tracks
	# # if line.find('#') == 0:
	# # 	print(line, end='')

	# # find nodes or edges
	# if '->' in line:
	# 	mpt.add_prereq(re_courses.findall(line)[0], re_courses.findall(line)[1])
	# elif '--' in line:
	# 	mpt.add_coreq(re_courses.findall(line)[0], re_courses.findall(line)[1])
	# elif line == '\n':
	# 	continue
	# # else:
	# # 	print('node')
	# # else:
	# # 	print(line, end='')

# print('\nAll courses in ' + str(mpt.name).upper() + ':')

# # print list of courses
# for i, item in enumerate(sorted(mpt.courses), start=0):
# 	if i % 7 == 0:
# 		print()
# 	else:
# 		print('{0:10s}'.format(item), end=' ')

# print('\n\nInput courses completed, type X to finish:\n')

# # handles course completed input
# def input_match(course):
# 	for i in course:
# 		if i in cgv.completed:
# 			print('> repeat info: ' + str(i))
# 		elif i in mpt.courses:
# 			cgv.add_completed(i)
# 		else:
# 			print('> does not exist: ' + str(i))

# # course completed input & error check
# course_completed = re_courses.findall(input().upper())
# while len(course_completed) > 0:
# 	input_match(course_completed)
# 	course_completed = re_courses.findall(input().upper())

# print('Completed Courses: ' + str(cgv.completed))

# convert to python graphviz

# generate graph