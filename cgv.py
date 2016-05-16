# cgv.py - Curriculum Graph Visualizer - Dana Toribio

from collections import deque
from collections import OrderedDict
import graphviz
import os
import re
import sys

# ----- globals -----------------------

re_courses = re.compile('\w+\s\d+\w*')	# regex for courses

# ----- classes -----------------------

class Node:
	def __init__(self, data):
		self.data = data
		self.children = []
		self.priority = False
		self.units = 0
		self.taken = False

	def add_child(self, obj):
		self.children.append(obj)

	def get_child(self):
		return self.children

	def set_priority(self):
		self.priority = True

	def set_units(self):
		if 'CPSC' or 'PHYS' in self.data:
			if self.data[-1] is 'L':
				self.units = 1
			else:
				self.units = 3
		if 'MATH' in self.data:
			self.units = 4

	def set_taken(self):
		self.taken = True

# ----- functions ---------------------

# breadth first search sort on study plan tree
def bfs(root):
	# input: tree with nodes organized by prerequisites
	# output: bfs-sorted list of courses by order of prerequisites met
	visited = []
	queue = deque([root])
	while queue:
		vertex = queue.popleft()
		if vertex in visited:
			visited.remove(vertex)
		if vertex.data is not 'ROOT':
			visited.append(vertex)
		for i in vertex.children:
			queue.append(i)
	return visited

# print list of courses
def courses_table(courses):
	for i, item in enumerate(sorted(courses), start=1):
		if i % 7 == 0:
			print()
		else:
			print('{:10s}'.format(item), end=' ')

# suggestion algorithm
def create_studyplan(bfs):
	# input: bfs result
	# output: list of study plan suggestion by semester
	suggestion_hash = OrderedDict()
	suggestion_hash['taken'] = []

	count = 1
	unit_count = 0
	prev_count = 0
	suggestion_hash[count] = []
	for i in bfs:
		if i.taken is True:
			suggestion_hash['taken'].append(i)
		elif (prev_count != 0) and ((prev_count + i.units) <= 16):
			suggestion_hash[count].append(i)
		elif (unit_count + i.units) <= 16:
			suggestion_hash[count].append(i)
			unit_count = unit_count + i.units
		else:
			count = count + 1
			suggestion_hash[count] = []
			suggestion_hash[count].append(i)
			prev_count = unit_count
			unit_count = i.units
	return suggestion_hash

# populate study plan tree
def create_tree(file):
	# input: studyplan file, empty dictionary for tree
	# output: tree organized by courses and prerequisites
	tree = OrderedDict()
	tree['ROOT'] = Node("ROOT")

	for line in file:
		r = re_courses.findall(line)
		if r and r[0] not in tree:
			tree[r[0]] = Node(r[0])				# create Node obj
			tree['ROOT'].add_child(tree[r[0]])	# set as child to ROOT
			if '*' in line:
				tree[r[0]].set_priority()		# set priority
			tree[r[0]].set_units()				# set units
		try:
			if r and r[1] not in tree:
				tree[r[1]] = Node(r[1])
			tree[r[0]].add_child(tree[r[1]])
			if '*' in line:
				tree[r[1]].set_priority()
			tree[r[1]].set_units()
		except:
			pass
	return tree

# find major
def get_major(file):
	for line in file:
		if '## Major:' in line:
			major = line[10:-1]
			break
	return major

# find elective tracks
def get_tracks(file):
	track_list = []
	for line in file:
		if '##' in line:
			pass
		elif ('required' not in line) and ('#' in line):
			track_list.append(line[2:-1])
	return track_list

# handles course completed input
def handle_taken_input(usr_input, course_list, taken_list):
	for i in usr_input:
		if i in taken_list:
			print('> Repeat info: ' + str(i))
		elif i in course_list:
			taken_list.append(i)
		else:
			print('> Does not exist: ' + str(i))

# user input for elective track
def input_elective(elec_trk):
	elective = 0
	try:
		elective = int(input())
	except:
		print('\n> Invalid input, please try again:', end=' ')
		elective = int(input())
	return elec_trk[elective-1]

# user input for courses taken & error check
def input_taken_courses(course_list):
	course = re_courses.findall(input().upper())
	taken = []
	if len(course) == 0:
		print('> Invalid input, please try again:')
		course = re_courses.findall(input().upper())
	while len(course) > 0:
		handle_taken_input(course, course_list, taken)
		course = re_courses.findall(input().upper())
	return taken

# print elective tracks
def print_tracks(elec_trk):
	for i, item in enumerate(elec_trk, start=1):
		print('[' + str(i) + '] ' + item)

# for testing: print bfs result
def test_print_bfs(bfs):
	# input: bfs results
	# output: prints data of bfs results
	print('\n----- BREADTH FIRST SEACH RESULTS ------------\n')
	print('UNITS COURSE PRIORITY TAKEN')
	for i in bfs:
		print(i.units, i.data, i.priority, i.taken)

# for testing: print study plan suggestion
def test_print_studyplan(studyplan):
	# input: dictionary of study plan data
	# output: prints the study plan data by semester
	print('\n----- STUDY PLAN RESULTS ---------------------\n')
	for i in studyplan:
		print('cluster:', i)
		for j in studyplan[i]:
			print(j.units, j.data)
		print()

# for testing: print tree results
def test_print_tree(tree):
	# input: study plan tree
	# output: prints the tree results
	print('\n----- STUDY PLAN TREE RESULTS ----------------\n')
	for i in tree:
		if len(tree[i].children) > 0:
			if tree[i].priority == True:
				print('*', end=' ')
			print(str(tree[i].data) + ' -> ', end='')
		else:
			print(tree[i].data)
		for j in tree[i].children:
			if j != tree[i].children[-1]:
				print(j.data, end=', ')
			else:
				print(j.data)

# updates data of taken courses
def update_taken(tree, taken_list):
	# input: study plan tree, courses taken
	# output: updates courses taken to True in study plan tree
	for i in taken_list:
		tree[i].set_taken()

# write core and elective prereqs to studyplan.txt
def write_core_elecs(infile, outfile, elective, courses):
	read = False	# toggle to read courses for user's study plan
	trk_hash = {}
	key = ''
	val = ''

	for line in infile:
		r = re_courses.findall(line)
		if '##' in line:
			pass
		elif ('required' in line) or (elective in line):
			if key is not '':
				trk_hash[key] = val
				outfile.write(key)
				outfile.write(trk_hash[key] + '\n')
				key = ''
				val = ''
			read = True
			trk_hash[line] = ''
			key = line
		elif '#' in line:
			if key is not '':
				trk_hash[key] = val
				outfile.write(key)
				outfile.write(trk_hash[key] + '\n')
				key = ''
				val = ''
			read = False
		elif read is True and r:
			val = val + line
			if r[0] not in courses:
				courses.append(r[0])
			try:
				if r[1] not in courses:
					courses.append(r[1])
			except:
				pass

# write suggestions to studyplan.txt
def write_suggestions(studyplan, outfile):
	# input: studyplan, filename of output file
	# output: write course suggestions to output file
	of = open(outfile, 'a')
	for i in studyplan:
		if ('taken' in str(i)) and len(studyplan[i]) > 0:
			of.write('# ' + str(i) + '\n')
		elif type(i) is int:
			of.write('\n# semester ' + str(i) + '\n')
		for j in studyplan[i]:
			of.write(str(j.data) + '\n')

# ----- main --------------------------
def main():
	f = open(sys.argv[1], 'r')
	fn = 'studyplan.txt'		# filename
	of = open(fn, 'w')			# output file

	major = get_major(f)

	print('\nAll elective tracks in ' + str(major) + ':\n')
	tracks = get_tracks(f)
	print_tracks(tracks)

	print('\nPlease select ONE elective track:', end=' ')
	elective = input_elective(tracks)

	f.seek(0)

	courses = []

	write_core_elecs(f, of, elective, courses)

	print('\nAll courses in ' + str(major) + ':\n')
	courses_table(courses)

	print('\n\nInput courses taken:\n')
	taken_courses = input_taken_courses(courses)

	of.close()
	of = open(fn, 'r')

	tree_result = create_tree(of)
	update_taken(tree_result, taken_courses)
	# test_print_tree(tree_result)

	bfs_result = bfs(tree_result['ROOT'])
	# test_print_bfs(bfs_result)

	studyplan_result = create_studyplan(bfs_result)
	# test_print_studyplan(studyplan_result)

	of.close()

	write_suggestions(studyplan_result, fn)

if __name__ == '__main__':
	main()

# CONVERT PYTHON TO GRAPHVIZ

# os.startfile('cgc.py')

# generate graph