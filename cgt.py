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

# populate study plan tree
def populate_tree(file, tree):
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

# print tree results
def print_tree(tree):
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

def update_completed(tree, taken_list):
	for i in taken_list:
		tree[i].set_taken()

def bfs(root):
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

f = open('studyplan.txt', 'r')
re_courses = re.compile('\w+\s\d+\w*')	# regex for courses
taken_courses = []

node_hash = OrderedDict()
node_hash['ROOT'] = Node("ROOT")

populate_tree(f, node_hash)

update_completed(node_hash, taken_courses)

result = bfs(node_hash['ROOT'])

for i in result:
	print(i.units, i.data, i.priority, i.taken)

# SUGGESTION ALGORITHM
suggestion_hash = OrderedDict()
suggestion_hash['taken'] = []

# print(suggestion_hash)

count = 1
unit_count = 0
prev_count = 0
suggestion_hash[count] = []
for i in result:
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

for i in suggestion_hash:
	print('**', i, '**')
	for j in suggestion_hash[i]:
		print(j.units, j.data)

# i = 1
# unit_count = 0
# for each course in BFS result:
	# if Taken is True:
		# suggestion_hash['taken'].append(course)
	# elif (unit_count + i.units) <= 16:
		# suggestion_hash[i].append(course)
	# else:
		# i++
		# suggestion_hash[i].append()
		# unit_count 