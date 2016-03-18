# testoutput.py - Dana Oira

from graphviz import Digraph

c = Digraph('testoutput', filename='testoutput.gv')

c.attr('node', shape='box')
c.attr('graph', rank='same')
c.body.append('{rank=same; "complete"; "1";}')

# c.body.append('{rank=same; "complete"; "1";}')
c.body.append('rank=same; "a"; "2";')
c.body.append('rank=same; "b"; "3"')
c.body.append('rank=same; "c"; "4"')
c.body.append('rank=same; "d"; "5"')
c.body.append('rank=same; "e"; "6"')

c.edges([('complete', 'a'), ('a', 'b'), ('b', 'c'), ('c', 'd')])
c.edge('d', 'e', '', dir='both')
c.node('1')
c.node('2')
c.node('3')
c.node('4')
c.node('5')
c.node('6')
c.node('7')
c.node('8')

print(c.source)

c.view()