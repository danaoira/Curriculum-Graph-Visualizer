# cgt.py - Curriculum Graph Tree - Dana Toribio

from collections import deque
from collections import OrderedDict
import os
import re
import sys

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

re_courses = re.compile('\w+\s\d+\w*')	# regex for courses
f = open('studyplan.txt', 'r')
taken_courses = []

tree_result = create_tree(f)
test_print_tree(tree_result)
update_taken(tree_result, taken_courses)

bfs_result = bfs(tree_result['ROOT'])
test_print_bfs(bfs_result)

studyplan_result = create_studyplan(bfs_result)
test_print_studyplan(studyplan_result)