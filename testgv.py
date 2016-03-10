# testoutput.py - Dana Oira

from graphviz import Digraph

c = Digraph('cgv', filename='testoutput.gv')

c.edge('A', 'B')

print(c.source)

c.view()