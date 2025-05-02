import networkx as nx
from harmony.harmonyAlgorithm import harmony_search_serial
from harmony.ObjectiveFunction import ObjectiveFunctionInterface

class GraphObjectiveFunction(ObjectiveFunctionInterface):
    def __init__(self, graph):
        self.graph = graph
        self.num_nodes = len(graph.nodes)

    def fitness(self, vector):
        # Example: Minimize the total weight of a path
        total_weight = 0
        for i in range(len(vector) - 1):
            if self.graph.has_edge(vector[i], vector[i + 1]):
                total_weight += self.graph[vector[i]][vector[i + 1]].get('weight', 1)
            else:
                return float('inf')  # Penalize invalid paths
        return total_weight

    def get_fitness(self, vector):
        # Use the fitness method to calculate the fitness value
        return self.fitness(vector)

    def get_value(self, i, j=None):
        # Return a random node from the graph
        return list(self.graph.nodes)[i]

    def get_num_parameters(self):
        # Number of parameters is the number of nodes in the graph
        return self.num_nodes

    def maximize(self):
        # Set to False for minimization problems
        return False

    def use_random_seed(self):
        # Return False if you don't need a random seed
        return False

    def get_hms(self):
        # Return the harmony memory size
        return 10

    def get_max_imp(self):
        # Return the maximum number of improvisations
        return 1000

    def get_hmcr(self):
        # Return the Harmony Memory Considering Rate (e.g., 0.9)
        return 0.9

    def get_par(self):
        # Return the Pitch Adjustment Rate (e.g., 0.3)
        return 0.3

    def is_variable(self, i):
        # All parameters (nodes) are adjustable
        return True

    def is_discrete(self, i):
        # All parameters (nodes) are discrete
        return True

    def get_index(self, i, value):
        # Return the index of the given value in the list of graph nodes
        return list(self.graph.nodes).index(value)

    def get_mpai(self):
        # Return the Maximum Pitch Adjustment Index (e.g., num_nodes - 1)
        return self.num_nodes - 1

    def get_num_discrete_values(self, i):
        # Return the total number of nodes in the graph
        return self.num_nodes

    # Do the harmony search for one graph
    def doHarmonySearchForOneGraph(graph, hsa_test_data):
        # Initialize the objective function with the graph
        objective_function = GraphObjectiveFunction(graph)

        # Run Harmony Search
        iteration = 10
        results = harmony_search_serial(objective_function, iteration,None)

        # Extract relevant data from HarmonySearchResults
        new_row = {
            "index": len(hsa_test_data) + 1,
            "Best Harmony (Path) ": results.best_harmony,
            "Best Fitness (Cost) ": results.best_fitness,
        }
        hsa_test_data.loc[len(hsa_test_data)] = new_row

        # Save the results to a CSV file
        hsa_test_data.to_csv("hsa_test_data_results.csv", index=False)

if __name__ == "__main__":
    Gn = nx.complete_graph(5)
    nx.set_edge_attributes(Gn, values=1, name='weight')  # Assign weights to edges

    # Initialize the objective function with the graph
    objective_function = GraphObjectiveFunction(Gn)

    # Run Harmony Search
    results = harmony_search_serial(objective_function, 10, None)

    print("Best Harmony (Path):", results[0])
    print("Best Fitness (Cost):", results[1])