import networkx as nx
import matplotlib.pyplot as plt
import random

# Seed for reproducibility
random.seed(47)

# Create a graph
G = nx.Graph()

# Number of customers (excluding depot)
num_customers = 5
nodes = list(range(num_customers + 1))  # Node 0 is depot
G.add_nodes_from(nodes)

# Generate random positions for each node (Depot at center)
pos = {0: (0, 0)}  # Depot
for i in range(1, num_customers + 1):
    pos[i] = (random.uniform(-1.5, 1.5), random.uniform(-1.5, 1.5))

# Add edges from depot to each customer with random weights
edges = []
for i in range(1, num_customers + 1):
    weight = random.randint(5, 20)
    edges.append((0, i, weight))

# Optionally, connect some customer nodes to each other
for i in range(1, num_customers + 1):
    for j in range(i + 1, num_customers + 1):
        if random.random() < 0.4:  # 40% chance of connecting customer nodes
            weight = random.randint(5, 20)
            edges.append((i, j, weight))

# Add edges to the graph
G.add_weighted_edges_from(edges)

# Draw the graph
plt.figure(figsize=(8, 6))
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1000, font_weight='bold')
nx.draw_networkx_edge_labels(
    G, pos, edge_labels={(u, v): d for u, v, d in G.edges(data='weight')}
)

# Highlight the depot
nx.draw_networkx_nodes(G, pos, nodelist=[0], node_color='orange', node_size=1200, label='Depot')

plt.title("Random VRP Graph with Depot (Node 0)")
plt.axis('off')
plt.show()