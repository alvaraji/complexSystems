import numpy as np
import math

INITIAL_PHEROMONE = 0.1

ENV = "test" #Sets enviornment from test to 'production', prod creates random graphs (choices: 'prod' and 'test')
NUM_CITIES = 20 #Sets the number of cities t randomly scatter
MIN_EDGE_SIZE = 75 #SETS MINIMUM EDGE LENGTH POSSIBLE
MAX_EDGE_SIZE = 250 #SETS MAXIMUM EDGE LENGTH POSSIBLE
EDGE_TO_CITY_RATIO = 1.15 #SETS HOW MANY EDGES SHOULD THERE BE RELATIVE TO HOW MANY CITIES

if ENV == "prod":
  cities = []
  distances = []
  pheromones = []

  #create list for cities and distances
  for i in range(NUM_CITIES):
    cities.append(str(i))
    distances.append([0] * NUM_CITIES)
    pheromones.append([0] * NUM_CITIES)

  #populate distances according to the number of edges desired
  for j in range(math.ceil(NUM_CITIES*EDGE_TO_CITY_RATIO)):
    #Pick two random cities
    city1 = np.random.randint(0, (NUM_CITIES - 1))
    city2 = np.random.randint(0, (NUM_CITIES - 1))
    
    #keep picking until there is no edge between chosen cities
    #AND until city 1 is not also city 2
    while ((distances[city1][city2] != 0) or (city1 == city2)):
      city1 = np.random.randint(0, (NUM_CITIES - 1))
      city2 = np.random.randint(0, (NUM_CITIES - 1))

    #Pick a random edge length
    edge_length = np.random.randint(MIN_EDGE_SIZE, MAX_EDGE_SIZE)

    #add edge to distances graph
    distances[city1][city2] = edge_length
    distances[city2][city1] = edge_length

    #add initial pheromones to existing city edge
    pheromones[city1][city2] = INITIAL_PHEROMONE
    pheromones[city2][city1] = INITIAL_PHEROMONE
  
  #if a city is completely disconnected, connect it to another city
  for k in range(NUM_CITIES):
    if (np.max(distances[k]) == 0):
      city_connect = np.random.randint(0, (NUM_CITIES - 1))

      #keep trying until you get a valid edge
      while ((distances[k][city_connect] != 0) or (k == city_connect)):
        city_connect = np.random.randint(0, (NUM_CITIES - 1))

      #Pick a random edge length
      edge_length = np.random.randint(MIN_EDGE_SIZE, MAX_EDGE_SIZE)

      #add edge to distances graph
      distances[k][city_connect] = edge_length
      distances[city_connect][k] = edge_length

      #add initial pheromones to existing city edge
      pheromones[k][city_connect] = INITIAL_PHEROMONE
      pheromones[city_connect][k] = INITIAL_PHEROMONE      


elif ENV == "test":
  # Define the cities and their distances for the ACO algorithm
  cities = [
      'Arad',           #1
      'Bucharest',      #2
      'Craiova',        #3
      'Drobeta',        #4
      'Eforie',         #5
      'Fagaras',        #6
      'Giurgiu',        #7
      'Hirsova',        #8
      'Iasi',           #9
      'Lugoj',          #10
      'Mehadia',        #11
      'Neamt',          #12
      'Oradea',         #13
      'Pitesti',        #14
      'Rimnicu Vilcea', #15
      'Sibiu',          #16
      'Timisoara',      #17
      'Urziceni',       #18
      'Vaslui',         #19
      'Zerind'          #20
  ]

  # Define the graph of distances. In the future, we can use straight line distance in the context of airlines.

  # Romainian Road Map
  distances = [
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 140, 118, 0, 0, 75],      # 0 Arad
      [0, 0, 0, 0, 0, 211, 90, 0, 0, 0, 0, 0, 0, 101, 0, 0, 0, 85, 0, 0],     # 1 Bucharest
      [0, 0, 0, 120, 0, 0, 0, 0, 0, 0, 0, 0, 0, 138, 146, 0, 0, 0, 0, 0],     # 2 Craiova
      [0, 0, 120, 0, 0, 0, 0, 0, 0, 0, 75, 0, 0, 0, 0, 0, 0, 0, 0, 0],        # 3 Drobeta
      [0, 0, 0, 0, 0, 0, 0, 86, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],          # 4 Eforie
      [0, 211, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 99, 0, 0, 0, 0],        # 5 Fagaras
      [0, 90, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],          # 6 Giurgiu
      [0, 0, 0, 0, 86, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 98, 0, 0],         # 7 Hirsova
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 87, 0, 0, 0, 0, 0, 0, 92, 0],         # 8 Iasi
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 70, 0, 0, 0, 0, 0, 111, 0, 0, 0],        # 9 Lugoj
      [0, 0, 0, 75, 0, 0, 0, 0, 0, 70, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],         # 10 Mehadia
      [0, 0, 0, 0, 0, 0, 0, 0, 87, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],          # 11 Neamt
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 151, 0, 0, 0, 71],        # 12 Oradea
      [0, 101, 138, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 97, 0, 0, 0, 0, 0],      # 13 Pitesti
      [0, 0, 146, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 97, 0, 80, 0, 0, 0, 0],       # 14 Rimnicu Vilcea
      [140, 0, 0, 0, 0, 99, 0, 0, 0, 0, 0, 0, 151, 0, 80, 0, 0, 0, 0, 0],     # 15 Sibiu
      [118, 0, 0, 0, 0, 0, 0, 0, 0, 111, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],       # 16 Timisoara
      [0, 85, 0, 0, 0, 0, 0, 98, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 142, 0],       # 17 Urziceni
      [0, 0, 0, 0, 0, 0, 0, 0, 92, 0, 0, 0, 0, 0, 0, 0, 0, 142, 0, 0],        # 18 Vaslui
      [75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 71, 0, 0, 0, 0, 0, 0, 0]          # 19 Zerind
  ]
  # Initialize the peromone array as a copy of the distances array, with INITIAL_PHEROMONE in place of the distance.

  pheromones = []

  for k in distances:
      pheromones.append([[INITIAL_PHEROMONE if distance != 0 else 0 for distance in row] for row in distances])
else:
  raise Exception("Error! Environment varaible \'" + ENV + "\' not recognized")
