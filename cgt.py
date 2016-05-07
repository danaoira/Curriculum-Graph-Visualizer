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
node_hash = {}

courses = list(set(re_courses.findall(f.read())))
# courses.sort()
# print(courses)
node = (len(courses)+1) * [0]

node[0] = Node('ROOT')
node_hash['ROOT'] = node[0]

# node[i] = courses[i-1]
# print('node[' + str(i) + '] = ' + str(node[i]))
f.seek(0)
n = 1
for line in f:
	r = re_courses.findall(line)
	if r and r[0] not in node_hash:
		node[n] = Node(r[0])
		node[0].add_child(node[n])
		node_hash[r[0]] = node[n]
		n += 1
	try:
		if r and r[1] not in node_hash:
			node[n] = Node(r[1])
			node_hash[r[0]].add_child(node[n])
			node_hash[r[1]] = node[n]
			n += 1
	except:
		pass

# for i in node_hash['ROOT'].children:
# 	print(i.data)

# for i in range(0, len(node)):
# 	print(str(node[i].data) + ' -> ')
# 	for j in node[i].children:
# 		print(j.data, end=', ')


# TEST: to view all node[i] values
# for i in range(len(node)):
# 	print('node[' + str(i) + '] = ' + str(node[i].data))

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
