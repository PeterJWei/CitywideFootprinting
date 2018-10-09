import plotly
plotly.tools.set_credentials_file(username='PeterJWei1993', api_key='yAEMz9PQoadbn4pmKKQ7')

import plotly.plotly as py


import plotly.graph_objs as go

import networkx as nx

import csv

# nodes = []
# with open('streetCorners.csv', mode='r') as csv_file:
# 	csv_reader = csv.reader(csv_file, delimiter=',')
# 	lines = 0
# 	x = 0.0
# 	y = 0.0
# 	for row in csv_reader:
# 		lines += 1
# 		nodes.append([float(row[0]),float(row[1])])
# 		x += float(row[0])
# 		y += float(row[1])
# 	x = x/lines
# 	y = y/lines


# G=nx.random_geometric_graph(200,0.125)
# print(G)
# pos=nx.get_node_attributes(G,'pos')
# print(pos)

i = 1
G = nx.Graph()
G.add_node(1, pos=[-73.962171,40.810581])
G.add_node(2, pos=[-73.961240,40.811896])
G.add_node(3, pos=[-73.962118,40.812259])
G.add_node(4, pos=[-73.963072,40.810969])
G.add_node(5, pos=[-73.963957,40.811342])
G.add_node(6, pos=[-73.962996,40.812625])
G.add_node(7, pos=[-73.963500,40.810395])
G.add_node(8, pos=[-73.964355,40.810755])
G.add_node(9, pos=[-73.964901,40.808443])
G.add_node(10, pos=[-73.965780,40.808825])
G.add_node(11, pos=[-73.962223,40.813701])
G.add_node(12, pos=[-73.960696,40.814215])
G.add_node(13, pos=[-73.959815,40.813838])
G.add_node(14, pos=[-73.958278,40.810635])
G.add_node(15, pos=[-73.959243,40.809351])
G.add_node(16, pos=[-73.964011,40.808063])
G.add_edge(1,2)
G.add_edge(3,2)
G.add_edge(3,4)
G.add_edge(4,1)
G.add_edge(4,5)
G.add_edge(5,6)
G.add_edge(6,3)
G.add_edge(4,7)
G.add_edge(5,8)
G.add_edge(7,8)
G.add_edge(7,9)
G.add_edge(8,10)
G.add_edge(11,6)
G.add_edge(3,12)
G.add_edge(2,13)
G.add_edge(2,14)
G.add_edge(1,15)
G.add_edge(1,16)

# for node in nodes:
# 	G.add_node(i, pos=node)
# 	i += 1
#G.add_node(1, pos=[0.0,1.0])
#G.add_node(2, pos=[0.0,2.0])
#G.add_edge(1,2)
pos=nx.get_node_attributes(G,'pos')
print(pos)
x = 0.0
y = 0.0
for p in pos:
	px = pos[p][0]
	py = pos[p][1]
	x += px
	y += py
x = x/len(pos)
y = y/len(pos)
dmin=10000000
ncenter=0
for n in pos:
    x1,y1=pos[n]
    d=(x1-x)**2+(y1-y)**2
    if d<dmin:
        ncenter=n
        dmin=d

p=nx.single_source_shortest_path_length(G,ncenter)

edge_trace = go.Scatter(
    x=[],
    y=[],
    line=dict(width=0.5,color='#888'),
    hoverinfo='none',
    mode='lines')

for edge in G.edges():
    x0, y0 = G.node[edge[0]]['pos']
    x1, y1 = G.node[edge[1]]['pos']
    edge_trace['x'] += tuple([x0, x1, None])
    edge_trace['y'] += tuple([y0, y1, None])

node_trace = go.Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        # colorscale options
        #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
        #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
        #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
        colorscale='YlGnBu',
        reversescale=True,
        color=[],
        size=10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=2)))

for node in G.nodes():
    x, y = G.node[node]['pos']
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([y])


for node, adjacencies in enumerate(G.adjacency()):
    node_trace['marker']['color']+=tuple([len(adjacencies[1])])
    node_info = '# of connections: '+str(len(adjacencies[1]))
    node_trace['text']+=tuple([node_info])



fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='<br>Transport Network',
                titlefont=dict(size=32),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    showarrow=True,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False,scaleanchor="x",scaleratio=1)))

plotly.offline.plot(fig, filename='networkx')