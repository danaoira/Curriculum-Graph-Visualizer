# finalcgv.py - Curriculum Graph Visualizer

from graphviz import Digraph

c = Digraph('test_ie', filename='test_ie.gv')
c.attr('graph', fontname="Helvetica")
c.attr('node', fontname="Helvetica")
# c.attr('fontname="Arial"')

# legend
c0 = Digraph('cluster_0')
c0.body.append('label = "LEGEND"')
c0.body.append('color=lightgrey')
c0.node_attr.update(style='filled', color='white')
c0.edge_attr.update(color='white')
c0.node('Semester 6', color='plum')
c0.node('Semester 7', color='crimson')
c0.node('Semester 3', color='peachpuff')
c0.node('Semester 4', color='darkseagreen')
c0.node('Semester 5', color='lightblue')
c0.node('Completed', color='grey')
c0.node('Semester 1', color='pink')
c0.node('Semester 2', color='lightsalmon')
c0.node('Semester 8', color='chocolate')
c0.edge('Semester 6', 'Semester 7')
c0.edge('Semester 7', 'Semester 8')
c0.edge('Semester 7', 'Semester 8')
c0.edge('Semester 3', 'Semester 4')
c0.edge('Semester 4', 'Semester 5')
c0.edge('Completed', 'Semester 1')
c0.edge('Semester 1', 'Semester 2')

# science and math electives
c1 = Digraph('cluster_1')
c1.body.append('label = "Science and Math Electives"')
c1.body.append('color = aliceblue')
c1.body.append('style = filled')
c1.edge('MATH 150B', 'MATH 250A')
c1.edge('PHYS 225', 'PHYS 225L', '', arrowhead='dot', arrowtail='dot', dir='both')
c1.edge('PHYS 225', 'PHYS 226')
c1.edge('PHYS 226', 'PHYS 226L', '', arrowhead='dot', arrowtail='dot', dir='both')
c1.node('MATH 150A')
c1.node('MATH 250A')
c1.node('MATH 338')

# IE track
c2 = Digraph('cluster_2')
c2.body.append('label = "Internet & Enterprise Computing (IE) Track"')
c2.body.append('labelloc = "b"')
c2.body.append('color = aliceblue')
c2.body.append('style = filled')
c2.node('CPSC 431')
c2.node('CPSC 473')
c2.node('CPSC 476')
# c2.node('Free Elective 1')
# c2.node('Free Elective 2')

# SC track
c3 = Digraph('cluster_3')
c3.body.append('label = "Scientific Computing (SC) Track"')
c3.body.append('labelloc = "b"')
c3.body.append('color = aliceblue')
c3.body.append('style = filled')
c3.node('MATH 340')
c3.node('MATH 370')
c3.node('Free Elective 1')
c3.node('Free Elective 2')
c3.node('Free Elective 3')

# Multimedia and Digital Games (MG) Track
c4 = Digraph('cluster_4')
c4.body.append('label = "Multimedia and Digital Games (MG) Track"')
c4.body.append('labelloc = "b"')
c4.body.append('color = aliceblue')
c4.body.append('style = filled')
c4.edge('CPSC 386', 'CPSC 486')
c4.node('CPSC 484', 'CPSC 486')
c4.edge('CPSC 486', 'CPSC 489')
c4.node('Free Elective 1')

# Software Engineer (SE) Track
c5 = Digraph('cluster_5')
c5.body.append('label = "Software Engineer (SE) Track"')
c5.body.append('labelloc = "b"')
c5.body.append('color = aliceblue')
c5.node('CPSC 462')
c5.node('CPSC 464')
c5.node('CPSC 463')
c5.node('CPSC 466')
c5.node('Free Elective 1')
c5.node('Free Elective 2')

# Custom Track (CT) Bioinformatics Focus
c6 = Digraph('cluster_5')
c6.body.append('label = "Custom Track (CT) Bioinformatics Focus"')
c6.body.append('labelloc = "b"')
c6.body.append('color = aliceblue')
c6.node('CPSC 483')
c6.node('CPSC 485')
c6.node('Free Elective 1')
c6.node('Free Elective 2')
c6.node('Free Elective 3')

# Custom Track (CT) Cybersecurity Focus
c7 = Digraph('cluster_5')
c7.body.append('label = "Custom Track (CT) Cybersecurity Focus"')
c7.body.append('labelloc = "b"')
c7.body.append('color = aliceblue')
c7.node('CPSC 353')
c7.node('CPSC 439')
c7.node('CPSC 452')
c7.node('CPSC 454')
c7.node('CPSC 456')

# coloring for completed courses
c.attr('node', style='filled', color='grey')
c.node('MATH 150A')
c.node('MATH 270A')
c.node('CPSC 120')

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
c.node('MATH 250A')
c.node('CPSC 240')
c.node('CPSC 254')
c.node('CPSC 223')
c.node('CPSC 311')

# semester 4 suggestion
c.attr('node', style='filled', color='darkseagreen')
c.node('PHYS 225')
c.node('PHYS 225L')
c.node('CPSC 301')
c.node('CPSC 332')
c.node('CPSC 315')

# semester 5 suggestion
c.attr('node', style='filled', color='lightblue')
c.node('PHYS 226')
c.node('PHYS 226L')
c.node('CPSC 335')
c.node('CPSC 351')
c.node('CPSC 323')
c.node('CPSC 362')

# semester 6 suggestion
c.attr('node', style='filled', color='plum')
c.node('CPSC 481')
c.node('CPSC 471')
c.node('CPSC 440')
c.node('CPSC 431')

# semester 7 suggestion
c.attr('node', style='filled', color='lightblue')
c.node('CPSC 473')
c.node('CPSC 476')

# major prerequisite tree
c.edge('CPSC 120', 'CPSC 121', color='red')
c.edge('CPSC 121', 'CPSC 131', color='red')
c.edge('CPSC 131', 'CPSC 223')
c.edge('CPSC 131', 'CPSC 240')
c.edge('CPSC 131', 'CPSC 254', color='red')
c.edge('CPSC 131', 'CPSC 311')
c.edge('CPSC 131', 'CPSC 332')
c.edge('CPSC 240', 'CPSC 440')
c.edge('CPSC 254', 'CPSC 301', color='red')
c.edge('CPSC 254', 'CPSC 351')
c.edge('CPSC 301', 'CPSC 323')
c.edge('CPSC 301', 'CPSC 335', color='red')
c.edge('CPSC 301', 'CPSC 362')
c.edge('CPSC 311', 'CPSC 315')
c.edge('CPSC 311', 'CPSC 362')
c.edge('CPSC 335', 'CPSC 481', color='red')
c.edge('CPSC 351', 'CPSC 471')
c.edge('ENGL 101', 'CPSC 311')
c.edge('MATH 150A', 'MATH 150B', color='red')
c.edge('MATH 150B', 'MATH 338', color='red')
c.edge('MATH 270A', 'CPSC 240')
c.edge('MATH 270A', 'MATH 270B', color='red')
c.edge('MATH 270B', 'CPSC 335', color='red')
c.edge('MATH 338', 'CPSC 335', color='red')

# IE track
c.edge('CPSC 332', 'CPSC 431')
c.edge('CPSC 332', 'CPSC 473')
c.edge('CPSC 223', 'CPSC 476')
c.edge('CPSC 351', 'CPSC 476')

# SC track

# MG track
# c.edge('CPSC 131', 'CPSC 386')
# c.edge('CPSC 150B', 'CPSC 484')
# c.edge('MATH 270B', 'CPSC 484')

# SE track

# Bioinformatics track

# Cybersecurity track

# science/math electives

c.subgraph(c1)
c.subgraph(c2)
# c.subgraph(c3)
# c.subgraph(c4)
# c.subgraph(c5)
# c.subgraph(c6)
# c.subgraph(c7)
c.subgraph(c0)

print(c.source)
input()
c.view()