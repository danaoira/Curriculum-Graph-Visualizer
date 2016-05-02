# cgv.py - Curriculum Graph Visualizer - Dana Toribio

import graphviz
import os
import re
import sys

re_courses = re.compile('\w+\s\d+\w*')	# regex for courses

f = open(sys.argv[1], 'r')

class Node:

	def __init__(self, data):
		self.data = data
		self.priority = False
		self.units = 0
		self.children = []

	def add_child(self, obj):
		self.children.append(obj)

	def priority(self):
		self.priority = True

	def get_child(self):
		return self.children

nf = open('studyplan.txt', 'w')

print('finished creating study plan')
print('opening study plan')

courses = []
tracks = []
completed = []
elective = 0

track_hash = {}

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

print('\nPlease select ONE elective track:', end=' ')

# user input for elective track
try:
	elective = int(input())
except:
	print('\n> Invalid input, please try again:', end=' ')
	elective = int(input())

elective = tracks[elective-1]

f.seek(0)

# toggle to read courses for user's study plan
read = False

# read courses for user's study plan
track_hash_key = ''
track_hash_value = ''
for line in f:
	if '##' in line:
		pass
	elif ('required' in line) or (elective in line):
		if track_hash_key is not '':
			track_hash[track_hash_key] = track_hash_value
			nf.write(track_hash_key)
			nf.write(track_hash[track_hash_key] + '\n')
			track_hash_key = ''
			track_hash_value = ''
		read = True
		track_hash[line] = ''
		track_hash_key = line
	elif '#' in line:
		if track_hash_key is not '':
			track_hash[track_hash_key] = track_hash_value
			nf.write(track_hash_key)
			nf.write(track_hash[track_hash_key] + '\n')
			track_hash_key = ''
			track_hash_value = ''
		read = False
	elif read is True and re_courses.findall(line):
		track_hash_value = track_hash_value + line
		if re_courses.findall(line)[0] not in courses:
			courses.append(re_courses.findall(line)[0])
		try:
			if re_courses.findall(line)[1] not in courses:
				courses.append(re_courses.findall(line)[1])
		except:
			pass

# STUDY PLAN TREE OPERATION

print('\nAll courses in ' + str(major) + ':\n')

# print list of courses
def courses_table(courses):
	for i, item in enumerate(sorted(courses), start=1):
		if i % 7 == 0:
			print()
		else:
			print('{:10s}'.format(item), end=' ')

courses_table(courses)

print('\n\nInput courses completed:\n')

# handles course completed input
def input_match(course):
	for i in course:
		if i in completed:
			print('> Repeat info: ' + str(i))
		elif i in courses:
			completed.append(i)
		else:
			print('> Does not exist: ' + str(i))

# course completed input & error check
course_completed = re_courses.findall(input().upper())
if len(course_completed) == 0:
	print('> Invalid input, please try again:')
	course_completed = re_courses.findall(input().upper())
while len(course_completed) > 0:
	input_match(course_completed)
	course_completed = re_courses.findall(input().upper())

# UPDATE STUDY PLAN TREE WITH COMPLETED
# STUDY PLAN SUGGESTION OPERATION

print('Generating study plan.')
# convert to python graphviz

os.startfile('cgc.py')

# generate graph