# Import data_setup module
import initialize_ACO # Initialize the graph and pheromone matrix
import ant as Ant # Import ant class definition
import numpy as np
import networkx as nx
from IPython import display
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import igraph as ig

ITERATIONS = 30
NUM_ANTS = 30

ALPHA = 0.7 # Pheromone factor
BETA = 0.2 # Distance factor
GAMMA = 0.99 # Evaporation factor

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

  max_pheromone = 7500

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
    starting_city = random.randint(0, len(initialize_ACO.distances) - 1)
    ants_colony_A = [Ant.Ant(initialize_ACO.distances, initialize_ACO.pheromones, ALPHA, BETA, starting_city) for _ in range(NUM_ANTS)]
    convergence = []
    pheromone_list = []
    nest_list = []

    # Calculate tours for each ant for number of iterations
    for iteration in range(ITERATIONS):
    
        # Ant Movement
        for ant in ants_colony_A:
            ant.construct_solution()
            if not(initialize_ACO.cities[ant.startingCity()] in nest_list):
              nest_list.append(initialize_ACO.cities[ant.startingCity()])

        # Global Pheromone Update
        sum_matrix = np.zeros((len(initialize_ACO.distances), len(initialize_ACO.distances[0])))

        # Sum all the matricies from all the ants
        for ant in ants_colony_A:
            sum_matrix = sum_matrix + ant.deposited_pheromone_matrix

        # Divide by number of ants, so we can change number without modifying alpha
        sum_matrix = sum_matrix / NUM_ANTS

        # Evaporation
        updated_pheromones = sum_matrix * GAMMA

        pheromone_list.append(updated_pheromones)

        total_length = 0
        
        #Get average path length to measure convergence
        for ant in ants_colony_A:
            total_length += ant.pathLength()

        convergence.append(total_length/NUM_ANTS)

        # index = 0
        # for a in ants_colony_A:
        #     a.print(index, initialize_ACO.cities)
        #     index += 1

        displayGraph(initialize_ACO.cities, initialize_ACO.distances, updated_pheromones, nest_list)

        # Prepare ants for next iteration, pass updated pheromones
        for ant in ants_colony_A:
            ant.reset(updated_pheromones)

        #if iteration % 5 == 0:
            # Visualization?

    print(convergence) # Print the iterations path length results

    # Check for termination criteria (Early convergence, objective function)
    # if termination_criteria_met():
    #     break


if __name__ == "__main__":
    main()