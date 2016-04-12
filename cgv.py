# mpt.py - Dana Toribio

import graphviz
import os
import re
# import subprocess
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

nf = open('studyplan.py', 'w')

nf_header = r'''from graphviz import Digraph
c = Digraph('studyplan', filename='studyplan.gv')'''

nf.write(nf_header + '\n')
nf.write('c.node("A")\n')
nf.write('c.view()')

print('finished creating study plan')
print('opening study plan')

os.startfile('studyplan.py')

from graphviz import Digraph

c = Digraph('finalcgv', filename='finalcgv.gv')

################################################

# z = Node("ROOT")
# a = Node("CPSC 120")
# b = Node("CSPC 121")
# c = Node("CPSC 131")
# d = Node("CPSC 223")
# e = Node("CPSC 240")
# f = Node("CPSC 254")
# g = Node("CPSC 311")
# h = Node("CPSC 332")
# z.add_child(a)
# a.add_child(b)
# b.add_child(c)
# c.add_child(d)
# c.add_child(e)
# c.add_child(f)
# c.add_child(g)
# c.add_child(h)

# print()

# for c in z.children:
# 	print(str(z.data) + ' -> ' + str(c.data))
# 	for i in c.children:
# 		print(str(c.data) + ' -> ' + str(i.data))
# 		for j in i.children:
# 			print(str(i.data) + ' -> ' + str(j.data))
# 			for k in j.children:
# 				print(str(j.data) + ' -> ' + str(k.data))


#################################

# courses = []
# tracks = []
# completed = []
# elective = 0

# for line in f:
# 	if '## Major:' in line:
# 		major = line[10:-1]
# 		break

# print('\nAll elective tracks in ' + str(major) + ':\n')

# # find elective tracks
# for line in f:
# 	if '##' in line:
# 		pass
# 	elif ('required' not in line) and ('#' in line):
# 		tracks.append(line[2:-1])

# # print elective tracks
# for i, item in enumerate(tracks, start=1):
# 	print('[' + str(i) + '] ' + item)

# print('\nPlease select ONE elective track:', end=' ')

# # user input for elective track
# try:
# 	elective = int(input())
# except:
# 	print('\n> Invalid input, please try again:', end=' ')
# 	elective = int(input())

# elective = tracks[elective-1]

# f = open(sys.argv[1], 'r')

# # toggle to read courses for user's study plan
# read = False

# # read courses for user's study plan
# for line in f:
# 	if ('required' in line) or (elective in line):
# 		read = True
# 	elif '#' in line:
# 		read = False
# 	elif read is True and re_courses.findall(line):
# 		if re_courses.findall(line)[0] not in courses:
# 			courses.append(re_courses.findall(line)[0])
# 		try:
# 			if re_courses.findall(line)[1] not in courses:
# 				courses.append(re_courses.findall(line)[1])
# 		except:
# 			pass

# print('\nAll courses in ' + str(major) + ':\n')

# # print list of courses
# def courses_table(courses):
# 	for i, item in enumerate(sorted(courses), start=1):
# 		if i % 7 == 0:
# 			print()
# 		else:
# 			print('{:10s}'.format(item), end=' ')

# courses_table(courses)

# print('\n\nInput courses completed:\n')

# # handles course completed input
# def input_match(course):
# 	for i in course:
# 		if i in completed:
# 			print('> Repeat info: ' + str(i))
# 		elif i in courses:
# 			completed.append(i)
# 		else:
# 			print('> Does not exist: ' + str(i))

# # course completed input & error check
# course_completed = re_courses.findall(input().upper())
# if len(course_completed) == 0:
# 	print('> Invalid input, please try again:')
# 	course_completed = re_courses.findall(input().upper())
# while len(course_completed) > 0:
# 	input_match(course_completed)
# 	course_completed = re_courses.findall(input().upper())

# print('Generating study plan.')
# # convert to python graphviz

# # generate graph