import graphviz
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