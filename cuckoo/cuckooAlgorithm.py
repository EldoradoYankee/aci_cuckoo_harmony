import random
import networkx as nx
import numpy as np
import math
import datetime
import pandas as pd
import matplotlib.pyplot as plt


class Cuckoo:
    def __init__(self, path, G, eps=0.9):
        self.path = path
        self.G = G
        self.nodes = list(G.nodes)
        self.eps = eps
        self.fitness = self.calculate_fitness()

    """
    Function to Compute fitness value.
    """

    def calculate_fitness(self):
        fitness = 0.0

        for i in range(1, len(self.path)):
            total_distance = 0
            curr_node = self.path[i - 1]
            next_node = self.path[i]
            if self.G.has_edge(curr_node, next_node):
                fitness += self.G[curr_node][next_node]['weight']
            else:
                fitness += 0
        fitness = np.power(abs(fitness + self.eps), 2)
        return fitness

    def generate_new_path(self):
        """
        This function generates a random solution (a random path) in the graph
        """
        nodes = list(self.G.nodes)
        start = nodes[0]
        end = nodes[-1]
        samples = list(nx.all_simple_paths(self.G, start, end))
        for i in range(len(samples)):
            if len(samples[i]) != len(nodes):
                extra_nodes = [node for node in nodes if node not in samples[i]]
                random.shuffle(extra_nodes)
                samples[i] = samples[i] + extra_nodes

        sample_node = random.choice(samples)
        return sample_node


class CuckooSearch:
    def __init__(self, G, num_cuckoos, max_iterations, beta):
        self.G = G
        self.nodes = list(G.nodes)
        self.num_cuckoos = num_cuckoos
        self.max_iterations = max_iterations
        self.beta = beta
        self.cuckoos = [Cuckoo(random.sample(self.nodes, len(self.nodes)), self.G) for _ in range(self.num_cuckoos)]
        self.test_results = []
        self.test_cases = 0

    """
    Function to buld new nests at new location and abandon old ones using Levi flights.
    """

    def levy_flight(self):
        sigma = (math.gamma(1 + self.beta) * np.sin(np.pi * self.beta / 2) / (
                    math.gamma((1 + self.beta) / 2) * self.beta * 2 ** ((self.beta - 1) / 2))) ** (1 / self.beta)
        u = np.random.normal(0, sigma, 1)
        v = np.random.normal(0, 1, 1)
        step = u / (abs(v) ** (1 / self.beta))
        return step

    def optimize(self):
        for i in range(self.max_iterations):
            for j in range(self.num_cuckoos):
                cuckoo = self.cuckoos[j]
                step = self.levy_flight()
                new_path = cuckoo.generate_new_path()
                new_cuckoo = Cuckoo(new_path, self.G)
                if new_cuckoo.fitness > cuckoo.fitness:
                    self.cuckoos[j] = new_cuckoo
                    self.test_cases += 1

            self.cuckoos = sorted(self.cuckoos, key=lambda x: x.fitness, reverse=True)
            best_path = self.cuckoos[0].path
            best_fitness = self.cuckoos[0].fitness

            self.test_results.append([i, best_fitness, self.test_cases])

        last_node = list(self.G.nodes)[-1]
        last_node_index = best_path.index(last_node) + 1

        return best_path[:last_node_index], best_fitness

def randomEdges(graph, edgeNumber, vrpSize, weightMin, weightMax):
    # Generate additional random edges with weights
    edges = []
    for _ in range(edgeNumber):
        x = random.randint(0, vrpSize)
        y = random.randint(0, vrpSize)
        if x != y and not graph.has_edge(x, y):
            weight = random.randint(weightMin, weightMax)
            edges.append((x, y, {'weight': weight}))
    return edges

# Keep removing edges until no node has degree 1
def remove_degree_one_nodes(graph):
    degree_one_nodes = [node for node, degree in dict(graph.degree()).items() if degree == 1]
    while degree_one_nodes:
        for node in degree_one_nodes:
            neighbors = list(graph.neighbors(node))
            if neighbors:
                graph.remove_edge(node, neighbors[0])
        degree_one_nodes = [node for node, degree in dict(graph.degree()).items() if degree == 1]

def remove_degree_zero_nodes(graph):
    # Identify nodes with degree 0
    degree_zero_nodes = [node for node, degree in dict(graph.degree()).items() if degree == 0]
    # Remove nodes with degree 0
    graph.remove_nodes_from(degree_zero_nodes)

if __name__ == "__main__":
    '''
    Graph Creation
    '''
    vrpSize = 100 # Number of nodes
    Gn = nx.Graph()


    # Ensure all nodes are connected using a Minimum Spanning Tree (MST)
    complete_graph = nx.complete_graph(vrpSize + 1)
    for (u, v) in complete_graph.edges():
        complete_graph[u][v]['weight'] = random.randint(1, 10)
    mst = nx.minimum_spanning_tree(complete_graph)
    Gn.add_edges_from(mst.edges(data=True))


    # Add additional random edges
    additional_edges = randomEdges(Gn, 20, vrpSize, 1, 10)
    Gn.add_edges_from(additional_edges)

    # Remove vertices with degree 1
    remove_degree_one_nodes(Gn)
    # Remove vertices with degree 0
    remove_degree_zero_nodes(Gn)

    # Automatically generate positions for all nodes
    pos = nx.spring_layout(Gn)  # You can also use nx.circular_layout(Gn) or other layouts


    # Draw the graph
    plt.figure(figsize=(80, 60))
    nx.draw(Gn, pos, with_labels=True, node_color='lightblue', node_size=1000, font_weight='bold')
    nx.draw_networkx_edge_labels(
        Gn, pos, edge_labels={(u, v): d for u, v, d in Gn.edges(data='weight')}
    )

    # Highlight the depot
    nx.draw_networkx_nodes(Gn, pos, nodelist=[0], node_color='orange', node_size=1200, label='Depot')

    plt.title("Random VRP Graph with Depot (Node 0)")
    plt.axis('off')
    plt.show()

    #csa = CuckooSearch(Gn, num_cuckoos=30, max_iterations=1000, beta=0.27)

    #start = datetime.datetime.now()
    #best_path, best_fitness = csa.optimize()
    #end = datetime.datetime.now()

    #csa_time = end - start

    #csa_test_data = pd.DataFrame(csa.test_results, columns=["iterations", "fitness_value", "test_cases"])

    #print("Optimal path: ", best_path)
    #print("Optimal path cost: ", best_fitness)
    #print("CSA total Exec time => ", csa_time.total_seconds())
    #csa_test_data.to_csv("csa_test_data_results.csv")