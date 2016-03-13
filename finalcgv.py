# finalcgv.py - Curriculum Graph Visualizer

from graphviz import Digraph

c = Digraph('finalcgv', filename='finalcgv.gv')
#c.node_attr.update(color='', style='filled')

# legend
c0 = Digraph('cluster_0')
c0.body.append('color=lightgrey')
c0.node_attr.update(style='filled', color='white')
c0.edge_attr.update(color='white')
c0.attr('node', color='grey')
c0.node('Completed')
c0.attr('node', color='pink')
c0.node('Semester 1')
c0.attr('node', color='lightsalmon')
c0.node('Semester 2')
c0.attr('node', color='peachpuff')
c0.node('Semester 3')
c0.attr('node', color='darkseagreen')
c0.node('Semester 4')
c0.attr('node', color='lightblue')
c0.node('Semester 5')
c0.attr('node', color='plum')
c0.node('Semester 6')
c0.attr('node', color='plum')
c0.node('Semester 7')
c0.attr('node', color='plum')
c0.node('Semester 8')
c0.edge('Completed', 'Semester 1', len='0.1')
c0.edge('Semester 1', 'Semester 2', len='0.1')
c0.edge('Semester 2', 'Semester 3', len='0.1')
c0.edge('Semester 3', 'Semester 4', len='0.1')
c0.edge('Semester 4', 'Semester 5', len='0.1')
c0.edge('Semester 5', 'Semester 6')
c0.edge('Semester 6', 'Semester 7')
c0.edge('Semester 7', 'Semester 8')
# c0.edges([('Completed', 'Semester 1'), ('Semester 1', 'Semester 2'), ('Semester 2', 'Semester 3'), ('Semester 3', 'Semester 4'), ('Completed', 'Semester 5'), ('Semester 5', 'Semester 6'), ('Semester 6', 'Semester 7'), ('Semester 7', 'Semester 8')])
c0.body.append('label = "LEGEND"')

# science and math electives
c1 = Digraph('cluster_1')
c1.body.append('color=lightgrey')
c1.edge('PHYS 225', 'PHYS 225L')
c1.edge('PHYS 225', 'PHYS 226')
c1.edge('PHYS 226', 'PHYS 226L')
c1.node('MATH 250A')
c1.body.append('label = "Science and Math Electives"')

# scientific computing track
c2 = Digraph('cluster_1')
c2.body.append('color=lightgrey')
c2.edge('MATH 250A', 'MATH 250B')
c2.edge('PHYS 225', 'PHYS 225L')
c2.body.append('label = "Scientific Computing Track"')

# coloring for completed courses
c.attr('node', style='filled', color='grey')
c.node('MATH 150A')
c.node('MATH 270A')
c.node('CPSC 120')
c.node('ENGL 101')

# semester 1 suggestion
c.attr('node', style='filled', color='pink')
c.node('MATH 150B')
c.node('MATH 270B')
c.node('CPSC 121')

# semester 2 suggestion
c.attr('node', style='filled', color='lightsalmon')
c.node('CPSC 131')
c.node('MATH 338')

# semester 3 suggestion
c.attr('node', style='filled', color='peachpuff')
c.node('CPSC 240')
c.node('CPSC 254')
c.node('CPSC 223')
c.node('CPSC 332')
c.node('CPSC 311')

# semester 4 suggestion
c.attr('node', style='filled', color='darkseagreen')
c.node('CPSC 440')
c.node('CPSC 301')
c.node('CPSC 351')
c.node('CPSC 315')

# semester 5 suggestion
c.attr('node', style='filled', color='lightblue')
c.node('CPSC 335')
c.node('CPSC 323')
c.node('CPSC 471')
c.node('CPSC 362')

# semester 6 suggestion
c.attr('node', style='filled', color='plum')
c.node('CPSC 481')

# other
c.attr('node', style='filled', color='lightblue')

# major prerequisite tree
c.edge('CPSC 120', 'CPSC 121')
c.edge('CPSC 121', 'CPSC 131')
c.edge('CPSC 131', 'CPSC 223')
c.edge('CPSC 131', 'CPSC 240')
c.edge('CPSC 131', 'CPSC 254')
c.edge('CPSC 131', 'CPSC 311')
c.edge('CPSC 131', 'CPSC 332')
c.edge('CPSC 240', 'CPSC 440')
c.edge('CPSC 254', 'CPSC 301')
c.edge('CPSC 254', 'CPSC 351')
c.edge('CPSC 301', 'CPSC 323')
c.edge('CPSC 301', 'CPSC 335')
c.edge('CPSC 301', 'CPSC 362')
c.edge('CPSC 311', 'CPSC 315')
c.edge('CPSC 311', 'CPSC 362')
c.edge('CPSC 335', 'CPSC 481')
c.edge('CPSC 351', 'CPSC 471')
c.edge('ENGL 101', 'CPSC 311')
c.edge('MATH 150A', 'MATH 150B')
c.edge('MATH 150B', 'MATH 338')
c.edge('MATH 270A', 'CPSC 240')
c.edge('MATH 270A', 'MATH 270B')
c.edge('MATH 270B', 'CPSC 335')
c.edge('MATH 338', 'CPSC 335')

#c.subgraph(c1)
#c.subgraph(c2)
#c.subgraph(c0)

# a = 'label = "COMPLETED COURSES\nCPSC 121, MATH 150A, MATH 270A, ENGL 101"'

# c.body.append(b)
c.view()