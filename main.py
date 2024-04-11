# Import data_setup module
import initialize_ACO # Initialize the graph and pheromone matrix
import ant as Ant # Import ant class definition
import numpy as np
import networkx as nx
from IPython import display
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import igraph as ig
import statistics


ITERATIONS = 500
NUM_ANTS = 100

ALPHA = 3 # Pheromone factor
BETA = 1 # Distance factor
GAMMA = 0.98 # Evaporation factor
STARTINGCITY = 1 # Used when doing single city start

def displayGraph(cities, distances, pheromone_matrix, nestList):
  # Construct a graph with a number of vertices equal to the cities
  n_vertices = len(cities)
  edges = []
  pheromones = []
  for i in range(len(distances)):
      for j in range(len(distances[0])):
          if distances[i][j] > 0:
            edges.append((i, j))
            pheromones.append(pheromone_matrix[i][j])

  nest = np.full((len(cities)), False, dtype=bool)

  for i in range(len(cities)):
    if cities[i] in nestList:
      nest[i] = True     

  max_pheromone = np.max(pheromones)

  g = ig.Graph(n_vertices, edges)

  # Set attributes for the graph, nodes, and edges
  g["title"] = "Romanian Road Map"
  g.vs["name"] = cities
  g.vs["isNest"] = nest

  # Customize edge colors based on pheromone levels
  cmap_colors = [((241/256), (241/256), (241/256)), ((105/256), (190/256), (40/256))]  # gray to green gradient

  cmap = LinearSegmentedColormap.from_list('pheromone_gradient', cmap_colors)

  edge_colors = []

  for i in range(len(edges)):
    phero_num = int((pheromones[i]/max_pheromone)*256)
    edge_colors.append(cmap(phero_num))

  # Plot in matplotlib
  # Note that attributes can be set globally (e.g. vertex_size), or set individually using arrays (e.g. vertex_color)
  fig, ax = plt.subplots(figsize=(16,8))
  ig.plot(
      g,
      target=ax,
      vertex_size=75,
      vertex_color=["steelblue" if nest else "salmon" for nest in g.vs["isNest"]],
      vertex_frame_width=4.0,
      vertex_frame_color="white",
      vertex_label=g.vs["name"],
      vertex_label_size=7.0,
      edge_width=[2],
      edge_color=edge_colors
  )

  display.clear_output(wait=True)
  display.display(plt.show())

def main():


     # Create the first colony
    starting_city = np.random.randint(0, len(initialize_ACO.distances) - 1)
    ants_colony_A = [Ant.Ant(initialize_ACO.distances, initialize_ACO.pheromones[0], ALPHA, BETA, STARTINGCITY) for _ in range(NUM_ANTS)]
    convergence = []
    pheromone_list = []
    nest_list = []
    sum_matrix = []
    path_lengths = []

    # Calculate tours for each ant for number of iterations
    for iteration in range(ITERATIONS):
    
        # Ant Movement
        for ant in ants_colony_A:
            ant.construct_solution()
            if not(initialize_ACO.cities[ant.starting_city] in nest_list):
              nest_list.append(initialize_ACO.cities[ant.starting_city])

        # City Pheromone Update
        for _ in initialize_ACO.distances:
            sum_matrix.append(np.zeros((len(initialize_ACO.distances), len(initialize_ACO.distances[0]))))

        # Sum all the matricies from all the ants for their city
        i = 0
        path_lengths = []
        for ant in ants_colony_A:

            # Take the top shortest 10 paths produced for reinforcement
            path_lengths.append((i, ant.pathLength()))
            path_lengths.sort(key=lambda x: x[1])
            i+=1
        
        for k in range(10):
            sum_matrix[ants_colony_A[path_lengths[k][0]].starting_city] = sum_matrix[ants_colony_A[path_lengths[k][0]].starting_city] + ants_colony_A[path_lengths[k][0]].deposited_pheromone_matrix

        # Divide by number of ants, so we can change ant count without modifying alpha
        for k in range(len(sum_matrix)):
            #sum_matrix[k] = sum_matrix[k] / NUM_ANTS
            sum_matrix[k] = sum_matrix[k] * GAMMA # Evaporation

        total_length = 0
        
        #Get average path length to measure convergence
        for ant in ants_colony_A:
            total_length += ant.pathLength()

        convergence.append(total_length/NUM_ANTS)

        # Print the best path initially
        if iteration == 0:
            ants_colony_A[path_lengths[0][0]].print(path_lengths[0][0], initialize_ACO.cities)

        if iteration == 5 or iteration == 450:
            ants_colony_A[5].printVariables()
            ants_colony_A[5].print(5, initialize_ACO.cities)

        # index = 0
        # for a in ants_colony_A:
        #     a.print(index, initialize_ACO.cities)
        #     index += 1

        # Prepare ants for next iteration, pass updated pheromones
        if iteration != ITERATIONS:
            for ant in ants_colony_A:
                ant.reset(sum_matrix[ant.starting_city], STARTINGCITY)

        #if iteration % 5 == 0:
            # Visualization?

    displayGraph(initialize_ACO.cities, initialize_ACO.distances, sum_matrix[STARTINGCITY], nest_list)

    ants_colony_A[path_lengths[0][0]].print(path_lengths[0][0], initialize_ACO.cities)

    # Print the first 5 and the last 5 elements, averaged to see if there's any improvement
    print(statistics.mean(convergence[:5]))
    print(statistics.mean(convergence[-5:]))

    # Check for termination criteria (Early convergence, objective function)
    # if termination_criteria_met():
    #     break


if __name__ == "__main__":
    main()