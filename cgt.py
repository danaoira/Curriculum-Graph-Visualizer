# cgt.py - Curriculum Graph Tree - Dana Toribio

import os
import re
import sys

class Node:
	n = 0
	def __init__(self, data):
		Node.n += 1
		self.n = Node.n
		self.data = data
		self.priority = False
		self.units = 0
		self.children = []

	# def create_node(self, )

	def add_child(self, obj):
		self.children.append(obj)

	def priority(self):
		self.priority = True

	def get_child(self):
		return self.children

	def set_units(self):
		if 'CPSC' in self:
			self.units = 3
		elif 'MATH' in self:
			self.units = 4

z = Node("ROOT")

re_courses = re.compile('\w+\s\d+\w*')	# regex for courses

f = open('studyplan.txt', 'r')
nodes = list(set(re_courses.findall(f.read())))
nodes.sort()
print(nodes)
node = len(nodes) * [0]

node_hash = {}

for i in range(len(nodes)):
	node[i] = nodes[i]
	print('node[' + str(i) + '] = ' + str(node[i]))

# for line in f:
	# check for RegEx matches
	# if re_courses.findall(line):	
	# if re[0] not in tree from DFS
		# if  re_courses.findall(line)[0] not in node_hash:
			# node_hash[re_courses.findall(line)[0]] = 
		# create re[0] node
		# set re[0] as child to ROOT
		# if * in line -> priority = True
		# set_units()
	# if re[1] not in tree
		# create re[1] node
		# set re[1] as child of re[0]
		# if * in line -> priority = True
