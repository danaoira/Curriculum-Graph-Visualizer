# cgt.py - Curriculum Graph Tree - Dana Toribio

import collections
import os
import re
import sys

class Node:
	n = 0
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

re_courses = re.compile('\w+\s\d+\w*')	# regex for courses

node_hash = collections.OrderedDict()
node_hash['ROOT'] = Node("ROOT")

f = open('studyplan.txt', 'r')

# populate study plan tree
for line in f:
	r = re_courses.findall(line)
	if r and r[0] not in node_hash:
		node_hash[r[0]] = Node(r[0])					# create Node obj
		node_hash['ROOT'].add_child(node_hash[r[0]])	# set as child to ROOT
		if '*' in line:
			node_hash[r[0]].set_priority()				# set priority
	try:
		if r and r[1] not in node_hash:
			node_hash[r[1]] = Node(r[1])
			node_hash[r[0]].add_child(node_hash[r[1]])
			if '*' in line:
				node_hash[r[1]].set_priority()
	except:
		pass

for i in node_hash:
	if len(node_hash[i].children) > 0:
		if node_hash[i].priority == True:
			print('*', end=' ')
		print(str(node_hash[i].data) + ' -> ', end='')
	else:
		print(node_hash[i].data)
	for j in node_hash[i].children:
		if j != node_hash[i].children[-1]:
			print(j.data, end=', ')
		else:
			print(j.data)

# BREADTH FIRST SEARCH

# def bfs(root_node):
# 	return null