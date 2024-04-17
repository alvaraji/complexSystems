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
#STARTINGCITY = 1 # Used when doing single city start // Not needed anymore

def displayGraph(cities, distances, pheromone_matrix, nestList):
  # Construct a graph with a number of vertices equal to the cities
  n_vertices = len(cities)
  edges = []
  pheromones = []
  dominantColony = []

  for i in range(len(distances)):
      for j in range(len(distances[0])):
          if distances[i][j] > 0:
            #get the pheromone array for the edge
            edgePheromones = pheromone_matrix[i][j]
            #extract the largest quantity of pheromones
            largestDeposit = np.max(edgePheromones)
            #append the edge to the list of edges
            edges.append((i, j))
            #append the largest quantity of pheromone to the list of pheromones
            pheromones.append(largestDeposit)

            #look for which colony had the largest deposit for coloring purposes
            winningCol = -1
            for k in range(len(edgePheromones)):
              if edgePheromones[k] == largestDeposit:
                winningCol = k%2 #limited to 2 colors
                break
            
            #if all the elements in the array are the same and there's more than one colony, consider it a tie
            if (np.all(edgePheromones == edgePheromones[winningCol]) and (len(edgePheromones) > 1)):
              winningCol = -1
            
            #append the winning colony to the dominant colony list
            #for purposes of this experiment only two colors will be shown
            dominantColony.append(winningCol)


  nestCol = np.full((len(cities)), -1, dtype=int)

  for i in range(len(cities)):
    for j in range(len(nestList)):
      if cities[i] == nestList[j]:
        nestCol[i] = j%2 #limited to 2 colors


  g = ig.Graph(n_vertices, edges)

  max_pheromone = np.max(pheromones)

  # Set attributes for the graph, nodes, and edges
  g["title"] = "Road Map"
  g.vs["name"] = cities
  g.vs["isNest"] = nestCol

  # Customize edge colors based on pheromone levels
  cmap_colors1 = [((241/256), (241/256), (241/256)), ((250/256), (128/256), (114/256))]  # gray to red gradient
  cmap_colors2 = [((241/256), (241/256), (241/256)), ((70/256), (130/256), (180/256))]  # gray to blue gradient
  cmap_colors3 = [((241/256), (241/256), (241/256)), ((147/256), (112/256), (219/256))] # gray to purple gradient

  cmap1 = LinearSegmentedColormap.from_list('pheromone_gradient', cmap_colors1)
  cmap2 = LinearSegmentedColormap.from_list('pheromone_gradient', cmap_colors2)
  cmap3 = LinearSegmentedColormap.from_list('pheromone_gradient', cmap_colors3)

  #get the edge color depending on which colony "controls" the edge
  edge_colors = []

  for i in range(len(edges)):
    phero_num = int((pheromones[i]/max_pheromone)*256)

    #if even colony controls the route then color it red
    if dominantColony[i] == 0:
      edge_colors.append(cmap1(phero_num))
    #if not color it blue
    elif dominantColony[i] == 1:
      edge_colors.append(cmap2(phero_num))
    #if there is a tie color it purple
    else:
      #edge_colors.append(cmap3(phero_num))
      edge_colors.append((147/256), (112/256), (219/256))

  # Plot in matplotlib
  # Note that attributes can be set globally (e.g. vertex_size), or set individually using arrays (e.g. vertex_color)
  fig, ax = plt.subplots(figsize=(16,8))
  ig.plot(
      g,
      target=ax,
      vertex_size=75,
      vertex_color=["steelblue" if nest == 1 else "salmon" if nest >= 0 else "silver" for nest in g.vs["isNest"]],
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
     # Create the first colonies

    colonies = []
    nest_list = []

    for nest in range(initialize_ACO.NUM_NESTS):
      #pick a random starting city
      starting_city = np.random.randint(0, len(initialize_ACO.distances) - 1)

      #keep picking until an unoccupied city is chose
      while (initialize_ACO.cities[starting_city] in nest_list):
        starting_city = np.random.randint(0, len(initialize_ACO.distances) - 1)

      nest_list.append(initialize_ACO.cities[starting_city])

      #create the colony
      if (initialize_ACO.ENV == "test"):
        current_ants_colony = [Ant.Ant(initialize_ACO.distances, initialize_ACO.pheromones[0], ALPHA, BETA, starting_city, nest) for _ in range(NUM_ANTS)]
      else:
        current_ants_colony = [Ant.Ant(initialize_ACO.distances, initialize_ACO.pheromones, ALPHA, BETA, starting_city, nest) for _ in range(NUM_ANTS)]
      #add the colony to the array of colonies
      colonies.append(current_ants_colony)

    convergence = [[] for nest in range(initialize_ACO.NUM_NESTS)]
    print(convergence)
    sum_matrix = []
    path_lengths = []

    # Calculate tours for each ant for number of iterations
    for iteration in range(ITERATIONS):

      for colony in colonies:

          #randomizing ant order
          np.random.shuffle(colony)

          colNumber = colony[0].colonyNumber
          nestCity = colony[0].starting_city

          # Ant Movement
          for ant in colony:
              ant.construct_solution()


          # City Pheromone Update
          #for _ in initialize_ACO.distances:
          if (initialize_ACO.ENV == "test"):
            sum_matrix = initialize_ACO.pheromones[0] 
          else:
            sum_matrix = initialize_ACO.pheromones 

          # Sum all the matricies from all the ants for their city
          i = 0
          path_lengths = []
          for ant in colony:

              # Take the top shortest 10 paths produced for reinforcement
              path_lengths.append((i, ant.pathLength()))
              path_lengths.sort(key=lambda x: x[1])
              i+=1

          for k in range(10):
            for q in range(len(sum_matrix)):
              for p in range(len(sum_matrix)):
                sum_matrix[q][p][colNumber] = sum_matrix[p][q][colNumber] + colony[path_lengths[k][0]].deposited_pheromone_matrix[q][p]

          # Divide by number of ants, so we can change ant count without modifying alpha
          for k in range(len(sum_matrix)):
              for t in range(len(sum_matrix)):
                sum_matrix[k][t][colNumber] = sum_matrix[k][t][colNumber] * GAMMA # Evaporation

          #

          total_length = 0

          #Get average path length to measure convergence
          for ant in colony:
              total_length += ant.pathLength()

          convergence[colNumber].append(total_length/NUM_ANTS)

          # Print the best path initially
          if iteration == 0:
              colony[path_lengths[0][0]].print(path_lengths[0][0], initialize_ACO.cities)

          if iteration == 5 or iteration == 450:
              colony[5].printVariables()
              colony[5].print(5, initialize_ACO.cities)

          # index = 0
          # for a in ants_colony_A:
          #     a.print(index, initialize_ACO.cities)
          #     index += 1

          # Prepare ants for next iteration, pass updated pheromones
          if iteration != ITERATIONS:
              for ant in colony:
                  ant.reset(sum_matrix, nestCity)

          #if iteration % 5 == 0:
              # Visualization?

    displayGraph(initialize_ACO.cities, initialize_ACO.distances, sum_matrix, nest_list)

    #colony[path_lengths[0][0]].print(path_lengths[0][0], initialize_ACO.cities)

    # Print the first 5 and the last 5 elements, averaged to see if there's any improvement
    for i in range(initialize_ACO.NUM_NESTS):
      if i%2 == 0:
        print("red colony (#" + str(i+1) + "): ")
      else:
        print("blue colony (#" + str(i+1) + "): ")
      print(statistics.mean(convergence[i][:5]))
      print(statistics.mean(convergence[i][-5:]))
      print("-------------")

    # Check for termination criteria (Early convergence, objective function)
    # if termination_criteria_met():
    #     break


if __name__ == "__main__":
    main()