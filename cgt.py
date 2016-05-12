# cgt.py - Curriculum Graph Tree - Dana Toribio

from collections import deque
from collections import OrderedDict
import os
import re
import sys

class Node:
	def __init__(self, data):
		self.data = data
		self.priority = False
		self.units = 0
		self.children = []

	def add_child(self, obj):
		self.children.append(obj)

	def set_priority(self):
		self.priority = True

	def get_child(self):
		return self.children

	def set_units(self):
		if 'CPSC' in self:
			self.units = 3
		elif 'MATH' in self:
			self.units = 4

# populate study plan tree
def populate_tree(file, tree):
	for line in file:
		r = re_courses.findall(line)
		if r and r[0] not in tree:
			tree[r[0]] = Node(r[0])				# create Node obj
			tree['ROOT'].add_child(tree[r[0]])	# set as child to ROOT
			if '*' in line:
				tree[r[0]].set_priority()		# set priority
		try:
			if r and r[1] not in tree:
				tree[r[1]] = Node(r[1])
			tree[r[0]].add_child(tree[r[1]])
			if '*' in line:
				tree[r[1]].set_priority()

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

def bfs(root):
	visited = []
	queue = deque([root])
	while queue:
		vertex = queue.popleft()
		if vertex not in visited:
			visited.append(vertex)
			for i in vertex.children:
				queue.append(i)
	return visited

re_courses = re.compile('\w+\s\d+\w*')	# regex for courses

node_hash = OrderedDict()
node_hash['ROOT'] = Node("ROOT")

f = open('studyplan.txt', 'r')

populate_tree(f, node_hash)
# print_tree(node_hash)

result = bfs(node_hash['ROOT'])

for i in result:
	print(i.data)

# BREADTH FIRST SEARCH

# def bfs(root_node):
# 	return null