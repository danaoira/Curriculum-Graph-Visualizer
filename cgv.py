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
		self.parents = []
		self.units = 0
		self.priority = False
		self.taken = False
		self.studyplan = False

	def add_child(self, obj):
		self.children.append(obj)

	def get_child(self):
		return self.children

	def add_parent(self, obj):
		self.parents.append(obj)

	def get_parent(self):
		return self.parents

	def set_priority(self):
		self.priority = True

	def set_units(self):
		if 'MATH' in self.data:
			self.units = 4
		elif ('PHYS' in self.data) and (self.data[-1] is 'L'):
			self.units = 1
		else:
			self.units = 3

	def set_taken(self):
		self.taken = True

	def set_studyplan(self):
		self.studyplan = True

# ----- functions ---------------------

# breadth first search sort on study plan tree
def bfs(root):
	visited = []
	queue = deque([root])
	while queue:
		vertex = queue.popleft()		# set vertex and remove from top queue
		if vertex in visited:
			visited.remove(vertex)		# if vertex already visited, remove it from visited
		if vertex.data is not 'ROOT':
			visited.append(vertex)		# else add it to end of visited list (prereqs met)
		for i in vertex.children:
			queue.append(i)				# add vertex's children to queue
	return visited

# suggestion algorithm
def create_studyplan(bfs):
	studyplan = OrderedDict()
	studyplan['taken'] = []
	queue = []

	term = 1
	unit_count = 0
	studyplan[term] = []

	for i in bfs:
		# print('\nSTART:', i.data, i.priority, prereqs_met(i), prereqs_dne(i, studyplan[term]), in_limit(i.units, unit_count))
		if i.taken:
			studyplan['taken'].append(i)
			i.set_studyplan()
		elif i.priority and prereqs_met(i) and prereqs_dne(i, studyplan[term]) and in_limit(i.units, unit_count):		# T T T T
			sp_to_studyplan(studyplan[term], i)
			unit_count = unit_count + i.units
		elif i.priority and prereqs_met(i) and prereqs_dne(i, studyplan[term]) and not in_limit(i.units, unit_count):	# T T T F
			queue = sp_do_queue(queue, unit_count, studyplan, term)
			term = sp_to_newterm(studyplan, term, i)
			unit_count = i.units
		elif i.priority and prereqs_met(i) and not prereqs_dne(i, studyplan[term]) and in_limit(i.units, unit_count):	# T T F T
			queue = sp_do_queue(queue, unit_count, studyplan, term)
			term = sp_to_newterm(studyplan, term, i)
			unit_count = i.units
		elif i.priority and prereqs_met(i) and not prereqs_dne(i, studyplan[term]) and not in_limit(i.units, unit_count):	# T T F F
			queue = sp_do_queue(queue, unit_count, studyplan, term)
			term = sp_to_newterm(studyplan, term, i)
			unit_count = i.units
		elif not i.priority:
			sp_to_queue(queue, i)

	for i in queue:
		queue = sp_end_queue(queue, unit_count, studyplan, term)
	
	return studyplan

# populate study plan tree
def create_tree(file):
	# input: studyplan file, empty dictionary for tree
	# output: tree organized by courses and prerequisites
	tree = OrderedDict()
	tree['ROOT'] = Node("ROOT")
	tree['ROOT'].in_studyplan = True

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
			tree[r[1]].add_parent(tree[r[0]])
			tree[r[0]].add_child(tree[r[1]])
			if '*' in line:
				tree[r[0]].set_priority()
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
def handle_taken_input(user_input, course_list, taken_list):
	for i in user_input:
		if i in taken_list:
			print('> Repeat info: ' + str(i))
		elif i in course_list:
			taken_list.append(i)
		else:
			print('> Does not exist: ' + str(i))

def in_limit(course_units, unit_count):
	if (unit_count + course_units) <= 16:
		return True
	else:
		return False

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

# check if courses' prereq is not in current term
def prereqs_dne(course, term):
	for i in course.parents:
		for j in term:
			if i.data is j.data:
				return False
	return True

def prereqs_met(course):
	for i in course.parents:
		while not (i.studyplan):
			return False
	return True

# print list of courses
def print_courses(courses):
	for i, item in enumerate(sorted(courses), start=1):
		if i % 7 == 0:
			print(item, end='')
			print()
		else:
			print('{:10s}'.format(item), end=' ')

# print elective tracks
def print_tracks(elec_trk):
	for i, item in enumerate(elec_trk, start=1):
		print('[' + str(i) + '] ' + item)

def priority(course):
	if course.priority == True:
		return True
	
def sp_to_studyplan(term, course):
	term.append(course)
	course.set_studyplan()

def sp_to_queue(queue, course):
	queue.append(course)

def sp_to_newterm(studyplan, term, course):
	term = term + 1
	studyplan[term] = []
	studyplan[term].append(course)
	course.set_studyplan()
	return term

def sp_do_queue(queue, unit_count, studyplan, term):
	new_queue = []
	for q in queue:
		# print('>>', q.data, unit_count, q.priority, prereqs_met(q), prereqs_dne(q, studyplan[term]), in_limit(q.units, unit_count))
		if in_limit(q.units, unit_count):
			if prereqs_dne(q, studyplan[term]) or 'L' in q.data[-1]:	# F T T T
				studyplan[term].append(q)
				q.set_studyplan()
				unit_count = unit_count + q.units
			else:
				new_queue.append(q)
		else:
			new_queue.append(q)
	queue = new_queue
	return queue

def sp_end_queue(queue, unit_count, studyplan, term):
	new_queue = []
	for q in queue:
		# print('>>', q.data, unit_count, q.priority, prereqs_met(q), prereqs_dne(q, studyplan[term]), in_limit(q.units, unit_count))
		if in_limit(q.units, unit_count):
			if prereqs_dne(q, studyplan[term]) or 'L' in q.data[-1]:
				studyplan[term].append(q)
				q.set_studyplan()
				unit_count = unit_count + q.units
		elif not in_limit(q.units, unit_count):
			term = term + 1
			studyplan[term] = []
			studyplan[term].append(q)
			q.set_studyplan()
			unit_count = q.units
	queue = new_queue
	return queue

# for testing: print bfs result
def test_print_bfs(bfs, test_file):
	# input: bfs results
	# output: prints data of bfs results
	test_file.write('\n\n----- BREADTH FIRST SEACH RESULTS ------------\n\n')
	test_file.write('UNITS COURSE PRIORITY TAKEN\n')
	for i in bfs:
		test_file.write(str(i.units) + ' ' + str(i.data) + ' ' + str(i.priority) + ' ' + str(i.taken) + '\n')

def test_print_sp_queue(queue, test_file):
	test_file.write('\n\n----- QUEUE RESULTS --------------------------\n\n')
	test_file.write('QUEUE: ')
	for i in queue:
		test_file.write(str(i.data) + ', ')
	test_file.write('\n')

def test_print_sp_result(studyplan, test_file):
	test_file.write('\n\n----- STUDY PLAN TRACE -----------------------\n\n')
	for i in studyplan:
		test_file.write('\n' + str(i) + ' -> ')
		for j in studyplan[i]:
			if j != studyplan[i][-1]:
				test_file.write(str(j.data) + ', ')
			else:
				test_file.write(str(j.data))


# for testing: print study plan suggestion
def test_print_studyplan(studyplan, test_file):
	# input: dictionary of study plan data
	# output: prints the study plan data by semester
	test_file.write('\n\n----- STUDY PLAN RESULTS ---------------------\n\n')
	for i in studyplan:
		test_file.write('cluster: ' + str(i) + '\n')
		for j in studyplan[i]:
			test_file.write(str(j.units) + ' ' + str(j.data) + '\n')
		test_file.write('\n')

# for testing: print tree results
def test_print_tree(tree, test_file):
	# input: study plan tree
	# output: prints the tree results
	test_file.write('\n\n----- STUDY PLAN TREE RESULTS ----------------\n\n')
	for i in tree:
		if len(tree[i].children) > 0:
			if tree[i].priority == True:
				test_file.write('* ')
			test_file.write(str(tree[i].data) + ' -> ')
		else:
			test_file.write(str(tree[i].data) + '\n')
		for j in tree[i].children:
			if j != tree[i].children[-1]:
				test_file.write(str(j.data) + ', ')
			else:
				test_file.write(str(j.data) + '\n')

def test_print_prereqs(tree, test_file):
	# input: study plan tree
	# output: prints courses and their prerequisites
	test_file.write('\n\n----- STUDY PLAN PREREQUISITES ---------------\n\n')
	for i in tree:
		if len(tree[i].parents) > 0:
			if tree[i].priority == True:
				test_file.write('* ')
			test_file.write(str(tree[i].data) + ' -> ')
		else:
			test_file.write(str(tree[i].data) + '\n')
		for j in tree[i].parents:
			if j != tree[i].parents[-1]:
				test_file.write(str(j.data) + ', ')
			else:
				test_file.write(str(j.data) + '\n')

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
		if ('required' in line) or (elective in line):
			read = True
			outfile.write(line)
		elif read is True and r:
			outfile.write(line)
			# val = val + line
			if r[0] not in courses:
				courses.append(r[0])
			try:
				if r[1] not in courses:
					courses.append(r[1])
			except:
				pass
		elif line is '\n':
			read = False

# write suggestions to studyplan.txt
def write_suggestions(studyplan, outfile):
	# input: studyplan, filename of output file
	# output: write course suggestions to output file
	of = open(outfile, 'a')
	for i in studyplan:
		if ('taken' in str(i)) and len(studyplan[i]) > 0:
			of.write('# ' + str(i) + '\n')
		elif type(i) is int:
			of.write('\n# semester: ' + str(i) + '\n')
		for j in studyplan[i]:
			of.write(str(j.data) + '\n')

# ----- main --------------------------
f = open(sys.argv[1], 'r')
fn = 'studyplan.txt'		# filename
of = open(fn, 'w')			# output file
t = open('test_results.txt', 'w')

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
print_courses(courses)

print('\n\nInput courses taken:\n')
taken_courses = input_taken_courses(courses)

of.close()
of = open(fn, 'r')

tree_result = create_tree(of)
update_taken(tree_result, taken_courses)
test_print_tree(tree_result, t)
test_print_prereqs(tree_result, t)

bfs_result = bfs(tree_result['ROOT'])
test_print_bfs(bfs_result, t)

studyplan_result = create_studyplan(bfs_result)
test_print_studyplan(studyplan_result, t)
test_print_sp_result(studyplan_result, t)

of.close()

write_suggestions(studyplan_result, fn)

os.startfile('cgc.py')
