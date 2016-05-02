# cgt.py - Curriculum Graph Tree - Dana Toribio

import os
import re
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

	def set_units(self):
		if 'CPSC' in self:
			self.units = 3
		elif 'MATH' in self:
			self.units = 4

z = Node("ROOT")

for line in f:
	# check for RegEx matches
	if re_courses.findall(line):
	# do depth first search
	# if re[0] not in tree from DFS
		# create re[0] node
		# set re[0] as child to ROOT
		# if * in line -> priority = True
		# set_units()
	# if re[1] not in tree
		# create re[1] node
		# set re[1] as child of re[0]
		# if * in line -> priority = True
