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

def prereqs_met(course):
	for i in course.parents:
		while not (i.studyplan):
			return False
	return True

def in_limit(course_units, unit_count):
	if (unit_count + course_units) <= 16:
		return True
	else:
		return False

def priority(course):
	if course.priority == True:
		return True

# check if courses' prereq is not in current term
def prereqs_dne(course, term):
	for i in course.parents:
		for j in term:
			if i.data is j.data:
				return False
	return True

# suggestion algorithm
def create_studyplan(bfs):
	studyplan = OrderedDict()
	studyplan['taken'] = []
	queue = []

	term = 1
	unit_count = 0
	studyplan[term] = []

	for i in bfs:
		print('--------------------------------------------\nSTART:', i.data, i.units, i.priority, prereqs_met(i), prereqs_dne(i, studyplan[term]), in_limit(i.units, unit_count), unit_count, '>', term, '\n')
		if i.taken:
			studyplan['taken'].append(i)
			i.set_studyplan()
			print('>> taken : ' + str(i.data))
		elif prereqs_met(i) and prereqs_dne(i, studyplan[term]):					# x T T x
			if i.priority and in_limit(i.units, unit_count):						# T T T T
				studyplan[term].append(i)
				i.set_studyplan()
				unit_count = unit_count + i.units
				print('>> A to studyplan : ' + str(i.data))
			elif i.priority and not in_limit(i.units, unit_count):					# T T T F
				term = term + 1
				studyplan[term] = []
				studyplan[term].append(i)
				i.set_studyplan()
				unit_count = i.units
				print('>> AA studyplan : ' + str(i.data))
			else:																	# x T T x
				queue.append(i)
				print('>> B to queue : ' + str(i.data))
		elif (prereqs_met(i) and not prereqs_dne(i, studyplan[term])):				# x T F x
			new_queue = []
			for q in queue:
				# print(q.data, '              !!!!!!!!!!!!!!!!!!!!!!!!!!!')
				if in_limit(q.units, unit_count):									# x T F T
					if prereqs_dne(q, studyplan[term]) or 'L' in q.data[-1]:
						studyplan[term].append(q)
						q.set_studyplan()
						unit_count = unit_count + q.units
						print('>> C to studyplan : ' + str(q.data))
				elif not in_limit(q.units, unit_count):								# x T F F
					unit_count = 0
					print('>> units = 0')
					term = term + 1
					print('>> new term')
					studyplan[term] = []
					new_queue.append(q)
					print('>> D queue : ' + str(q.data))
			queue = new_queue
			if in_limit(i.units, unit_count) and prereqs_dne(i, studyplan[term]):	# x T T T
				studyplan[term].append(i)
				i.set_studyplan()
				unit_count = unit_count + i.units
				print('>> E to studyplan : ' + str(i.data))
			elif unit_count > 14:													# x T T F
				term = term + 1
				studyplan[term] = []
				studyplan[term].append(i)
				i.set_studyplan()
				unit_count = i.units
				print('>> F to studyplan : ' + str(i.data))
			elif i.priority and in_limit(i.units, unit_count):						# T T F T
				term = term + 1
				studyplan[term] = []
				studyplan[term].append(i)
				i.set_studyplan()
				unit_count = i.units
				print('>> FF to studyplan: ' + str(i.data))			
			elif not i.priority and in_limit(i.units, unit_count):
				studyplan[term].append(i)
				i.set_studyplan()
				unit_count = unit_count + i.units
			else:																	# x T T x
				queue.append(i)
				print(unit_count)
				print('>> G : ' + str(i.data))
		elif (not prereqs_met(i) and prereqs_dne(i, studyplan[term])):				# x F T x
			pass
		else:
			print('ELSE: to queue')
			queue.append(i)

		test_print_sp_result(studyplan)
		test_print_sp_queue(queue)
		print('\nEND:', unit_count, '>', term)

	if (queue):
		for q in queue:
			if in_limit(q.units, unit_count):
				if prereqs_dne(q, studyplan[term]) or 'L' in q.data[-1]:
					studyplan[term].append(q)
					q.set_studyplan()
					unit_count = unit_count + q.units
	
	return studyplan



	# look at course
		# if course was taken:
			# add to studyplan
		# elif prereqs_met AND prereqs_dne:
			# if in_limit AND priority:
				# add to term
				# update course as added to studyplan
				# update unit_count
			# else:
				# add to queue
		# elif NOT prereqs_dne:
			# populate term with queue:
				# for i in queue:
					# if in_limit AND prereqs_dne:
						# add to term
						# remove item from queue
						# update unit_count
					# elif not in_limit:
						# term = term + 1
						# break
			# add to term
			# unit_count = i.unit
		# elif NOT in_limit:
			# term = term + 1


		# elif not prereqs_met(i):
		# 	for i in queue:
		# 		if in_limit(i.units, unit_count) and prereqs_dne(i, studyplan[i]):
		# 			pass
		# elif prereqs_met(i) and i.priority and in_limit(i.units, unit_count) and prereqs_dne(i, studyplan[count]):	# T T T T
		# 	studyplan[count].append(i)
		# 	unit_count = unit_count + i.units
		# 	i.set_studyplan()
		# 	print('T T T T: ' + str(i.data))
		# elif prereqs_met(i) and i.priority and prereqs_dne(i, studyplan[count]):		# T T F
		# 	queue.append(i)
		# 	# print('T T F : ' + str(i.data))
		# elif prereqs_met(i) and in_limit(i.units, unit_count):					# T F T
		# 	queue.append(i)
		# 	# print('T F T : ' + str(i.data))
		# elif prereqs_met(i):														# T F F
		# 	queue.append(i)
		# 	# print('T F F : ' + str(i.data))
		# elif priority(i) and in_limit(i.units, unit_count) and prereqs_dne(i, studyplan[count]):		# F T T T
		# 	print('F T T F : ' + str(i.data))
		# 	studyplan[count+1] = []
		# 	studyplan[count+1].append(i)
		# 	unit_count = unit_count + i.units
		# 	print(studyplan[count+1][0].data)
		# 	i.set_studyplan()
		# elif i.priority:															# F T F
		# 	queue.append(i)
		# 	# print('F T F : ' + str(i.data))
		# elif in_limit(i.units, unit_count):										# F F T
		# 	queue.append(i)
		# 	# print('F F T : ' + str(i.data))
		# # print(unit_count)
	
def test_print_sp_queue(queue):
	# print('----------------------- QUEUE')
	print('QUEUE:', end=' ')
	for i in queue:
		print(i.data, end=', ')

def test_print_sp_result(studyplan):
	# print('------------------ STUDY PLAN')
	for i in studyplan:
		print(i, end=' -> ')
		for j in studyplan[i]:
			print(j.data, end=', ')
		print()

	# for each node in bfs:
		# if priority is True:
			# if prereqs_met() is True:
				# add_to_studyplan()
			# else:
				# add to queue, high priority
		# else:
			# if prereqs_met() is True:
				# add to queue, normal priority



		# if i.taken is True:
		# 	sp_hash['taken'].append(i)		# add to taken courses list
		# elif (prev_count != 0) and ((prev_count + i.units) <= 16):
		# 	sp_hash[count-1].append(i)		# add to previous term in study plan
		# elif (unit_count + i.units) <= 16:
		# 	sp_hash[count].append(i)		# add to 
		# 	unit_count = unit_count + i.units
		# else:
		# 	count = count + 1
		# 	sp_hash[count] = []
		# 	sp_hash[count].append(i)
		# 	prev_count = unit_count
		# 	unit_count = i.units
	# return sp_hash

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

# print list of courses
def print_courses(courses):
	for i, item in enumerate(sorted(courses), start=1):
		if i % 7 == 0:
			print()
		else:
			print('{:10s}'.format(item), end=' ')

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

def test_print_prereqs(tree):
	# input: study plan tree
	# output: prints courses and their prerequisites
	print('\n----- STUDY PLAN PREREQUISITES ---------------\n')
	for i in tree:
		if len(tree[i].parents) > 0:
			if tree[i].priority == True:
				print('*', end=' ')
			print(str(tree[i].data) + ' -> ', end='')
		else:
			print(tree[i].data)
		for j in tree[i].parents:
			if j != tree[i].parents[-1]:
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
			of.write('\n# semester: ' + str(i) + '\n')
		for j in studyplan[i]:
			of.write(str(j.data) + '\n')

# ----- main --------------------------
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
print_courses(courses)

print('\n\nInput courses taken:\n')
taken_courses = input_taken_courses(courses)

of.close()
of = open(fn, 'r')

tree_result = create_tree(of)
update_taken(tree_result, taken_courses)
# test_print_tree(tree_result)
# test_print_prereqs(tree_result)

bfs_result = bfs(tree_result['ROOT'])
# test_print_bfs(bfs_result)

studyplan_result = create_studyplan(bfs_result)
# test_print_studyplan(studyplan_result)

of.close()

write_suggestions(studyplan_result, fn)

os.startfile('cgc.py')

# TO DO
# add translation for course suggestions via cgc.py
# add the rest of the elective tracks and their courses
# add prerequisite relations to elective courses
# if have time: handle user input for taken courses that do not have prerequisites met