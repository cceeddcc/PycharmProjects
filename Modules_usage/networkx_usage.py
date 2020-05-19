"""
NetworkX is a Python package for the creation, manipulation,
and study of the structure, dynamics, and functions
of complex networks.

navigator
# Theme : ...
# Package : ...
# Module : ...
# Class : ...
# Method : ...
# : comments / examples

"""
import matplotlib.pyplot as plt
import networkx as nx
help(nx)

# Class : nx.Graph()
"""
Base class for undirected graphs.
"""
G = nx.Graph()

# Class : nx.DiGraph()
"""
Base class for directed graphs.
"""
G = nx.DiGraph()

# Class : nx.MultiGraph()
"""
"""
G = nx.MultiGraph()

# Class : nx.MultiDiGraph()
"""
"""
G = nx.MultiDiGraph()



# Method : nx.Graph.add_node()
"""
Add a single node `node_for_adding` and update node attributes
"""
G.add_node(1)
G.add_node(2)
G.add_node("A",role="trader")

# Method : nx.Graph.add_nodes_from()
G.add_nodes_from([(1,2),(3,4)])
B.add_nodes_from(["A","B","C","D","E"],bipartite=0)
B.add_nodes_from([1,2,3,4], bipartite=1)

# Method :nx.Graph.add_edge()
G.add_edge(1,2)
G.add_edge("A", "B", weight=6, relation="family")

# Method : nx.Graph.add_edges_from()
G.add_edges_from([(3,4),(5,6)])


# Method : nx.Graph.edges()
G.edges() # list of all edges
G.edges(data=True) # list of all edges with attributes
G.edges(data="relation") # list of all edges with attribute "relation"

# Method : nx.Graph.nodes()
G.nodes() # list of all nodes
G.nodes(data=True) # list of all nodes with attributes


# Bipartite Graphs

B=nx.Graph()
B.add_nodes_from(["A","B","C","D","E"],bipartite=0)
B.add_nodes_from([1,2,3,4], bipartite=1)
B.add_edges_from([("A",1),("B",1),("C",1),("C",3),("D",2),("E",3)])



from networkx.algorithms import bipartite

bipartite.is_bipartite(B) # check if B is bipartite
B.add_edge("A","B") # break the rule
bipartite.is_bipartite(B)

B.remove_edge("A","B") # remove edge

# check set of nodes is bipartite
X = set([1,2,3,4])
bipartite.is_bipartite_node_set(B,X)

X = set(["A","B","C","D","E"])
bipartite.is_bipartite_node_set(B,X)

bipartite.sets(B)

# Projected Graphs
B = nx.Graph()
B.add_edges_from([("A",1),("B",1),("C",1),
                  ("D",1),("H",1),("B",2),
                  ("C",2),("D",2),("E",2),
                  ("G",2),("E",3),("F",3),
                  ("H",3),("J",3),("E",4),
                  ("I",4),("J",4)])
X = set(["A","B","C","D","E","F","G","H","I","J"])
P = bipartite.projected_graph(B,X)
nx.draw(P)

X = set([1,2,3,4])
P = bipartite.projected_graph(B,X)
nx.draw(P, with_labels= 1)

# Weighted Projected Graphs
X = set([1,2,3,4])
P = bipartite.weighted_projected_graph(B,X)
nx.draw(P, with_labels= 1)


# generate network data
import pandas as pd
import numpy as np
import random
import statsmodels.api as sm

n1 = []
n2 = []
outcome = []
for i in range(100) :
    (a, b) = np.random.choice([1, 2, 3, 4, 5, 6, 7], 2, replace=False)
    n1.append(a)
    n2.append(b)
    outcome.append(random.choice([-1,0,1]))
net_df = pd.DataFrame({"n1":n1,
                       "n2":n2,
                       "outcome":outcome})
net_df.to_string("C:/Users/S/Desktop/edgelist.txt",index=False, header=False)
net_df.to_csv("C:/Users/S/Desktop/edgelist.csv",index=False)
help(net_df.to_string)

# read Edgelist
G4 = nx.read_edgelist('C:/Users/S/Desktop/edgelist.txt', data=[('outcome', int)])
G4.edges(data=True)
chess = nx.read_edgelist('C:/Users/S/Desktop/edgelist.txt', data=[('outcome', int)],
                         create_using=nx.MultiDiGraph())
chess.edges(data=True)




G_df = pd.read_csv("C:/Users/S/Desktop/edgelist.csv", names=['n1', 'n2', 'outcome'], skiprows=1)
G_df
G5 = nx.from_pandas_edgelist(G_df, 'n1', 'n2', edge_attr='outcome')
G5.edges(data=True)

G5.degree() # return (node : number of edges(degree))

# edgelist to dataframe
df = pd.DataFrame(G5.edges(data=True),columns=["white","black","outcome"])
df


# 데이터 핸들링 스킬
df['outcome'] = df['outcome'].map(lambda x: x['outcome'])
df
won_as_white = df[df['outcome']==1].groupby('white').sum()["outcome"]
won_as_black = -df[df['outcome']==-1].groupby('black').sum()["outcome"]
win_count = won_as_white.add(won_as_black, fill_value=0)
win_count.head()
win_count.nlargest(5)





# clustering coefficient
G = nx.Graph()
G.add_edges_from([("A","K"),("A","B"),("A","C"),("B","C"),("B","K"),
                  ("C","E"),("C","F"),("D","E"),("E","F"),("E","H"),
                  ("F","G"),("I","J")])

nx.clustering(G,"F")
nx.clustering(G,"A")









################################################################################################################
# Method :
print(nx.info(G))

# Method :
nx.draw(G)


G = nx.Graph()
G.add_edges_from([(1,2),(2,3),(3,1)])
nx.draw(G)

nx.write_edgelist(G,path="C:/Users/S/Desktop/edgelist.txt")

G = nx.read_edgelist(path="C:/Users/S/Desktop/edgelist.txt",
                     create_using=nx.Graph(),
                     nodetype=int)

nx.draw(G)

G.nodes
G.edges
print(G.nodes)
print(G.edges)
nx.draw(G, with_labels=1) # label 표시

z = nx.complete_graph(10) # 모든 노드 연결됨
z.nodes()
z.edges()
z.order()
z.size()
nx.draw(z, with_labels=1) # label 표시


G = nx.gnp_random_graph(20,0.5) # 50% 확률로 randomly edges
G.nodes()
G.edges()
G.order()
G.size()
nx.draw(G, with_labels=1) # label 표시


## modellin road network of india

import networkx as nx
import matplotlib.pyplot as plt
import random
G = nx.Graph() # undirected graph
# G = nx.DiGraph() # directed graph

city_set = ["Delhi", "Bangalore", "Hyderabad", "Ahmedabad",
            "Chennai", "Kolkata", "Surat", "Pune", "Jaipur"]

for each in city_set:
    G.add_node(each)

nx.draw(G,with_labels=1)

costs = []
values=100
while (values<=2000):
    costs.append(values)
    values+=100

print(costs)

while(G.number_of_edges()<16):
    c1=random.choice(list(G.nodes))
    c2=random.choice(list(G.nodes))
    if c1!=c2 and G.has_edge(c1,c2) == 0 :
        w=random.choice(costs)
        G.add_edge(c1,c2,weight=w)

print(nx.info(G))
G.edges(data=True)

# change layout
# pos = nx.spectral_layout(G)
# pos = nx.spring_layout(G)
pos = nx.circular_layout(G)
nx.draw(G, with_labels=1,pos=pos)

# draw edges labels
nx.draw(G, with_labels=1,pos=pos)
nx.draw_networkx_edge_labels(G,pos=pos)


print(nx.is_connected(G)) # there exist path between every two pair of nodes
for u in G.nodes():
    for v in G.nodes():
        print(u,v,nx.has_path(G,u,v))
nx.has_path()

# shortest path
"""Returns the shortest weighted path from source to target in G.

    Uses Dijkstra's Method to compute the shortest weighted path
    between two nodes in a graph."""

u="Delhi"
v="Kolkata"
print(nx.dijkstra_path(G,u,v))
print(nx.dijkstra_path_length(G,u,v))



import matplotlib.pyplot as plt
import networkx as nx

G = nx.cycle_graph(24)
pos = nx.spring_layout(G, iterations=200)
nx.draw(G, pos, node_color=range(24), node_size=1000, cmap=plt.cm.Blues)
plt.show()


# Author: Aric Hagberg (hagberg@lanl.gov)
import matplotlib.pyplot as plt
import networkx as nx

G = nx.house_graph()
# explicitly set positions
pos = {0: (0, 0),
       1: (1, 0),
       2: (0, 1),
       3: (1, 1),
       4: (0.5, 2.0)}

nx.draw_networkx_nodes(G, pos, node_size=2000, nodelist=[4])
nx.draw_networkx_nodes(G, pos, node_size=3000, nodelist=[0, 1, 2, 3], node_color='b')
nx.draw_networkx_edges(G, pos, alpha=0.5, width=6)
plt.axis('off')
plt.show()