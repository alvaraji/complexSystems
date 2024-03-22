import numpy as np

INITIAL_PHEROMONE = 0.1

# Define the cities and their distances for the ACO algorithm
cities = [
    'Arad', 
    'Bucharest', 
    'Craiova', 
    'Drobeta', 
    'Eforie', 
    'Fagaras', 
    'Giurgiu', 
    'Hirsova', 
    'Iasi', 
    'Lugoj', 
    'Mehadia', 
    'Neamt', 
    'Oradea', 
    'Pitesti', 
    'Rimnicu Vilcea', 
    'Sibiu', 
    'Timisoara', 
    'Urziceni', 
    'Vaslui', 
    'Zerind'
]

# Define the graph of distances. In the future, we can use straight line distance in the context of airlines.

# Romainian Road Map
distances = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 140, 118, 0, 0, 75],      # Arad
    [0, 0, 0, 0, 0, 211, 90, 0, 0, 0, 0, 0, 0, 101, 0, 0, 0, 85, 0, 0],     # Bucharest
    [0, 0, 0, 120, 0, 0, 0, 0, 0, 0, 0, 0, 0, 138, 146, 0, 0, 0, 0, 0],     # Craiova
    [0, 0, 0, 120, 0, 0, 0, 0, 0, 75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],        # Drobeta
    [0, 0, 0, 0, 0, 0, 0, 86, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],          # Eforie
    [0, 211, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 99, 0, 0, 0, 0],        # Fagaras
    [0, 90, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],          # Giurgiu
    [0, 0, 0, 0, 86, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 98, 0, 0],         # Hirsova
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 87, 0, 0, 0, 0, 0, 0, 92, 0],         # Iasi
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 70, 0, 0, 0, 0, 0, 111, 0, 0, 0],        # Lugoj
    [0, 0, 0, 75, 0, 0, 0, 0, 0, 70, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],         # Mehadia
    [0, 0, 0, 0, 0, 0, 0, 0, 87, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],          # Neamt
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 151, 0, 0, 0, 71],        # Oradea
    [0, 101, 138, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 97, 0, 0, 0, 0, 0],      # Pitesti
    [0, 0, 146, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 97, 0, 80, 0, 0, 0, 0],       # Rimnicu Vilcea
    [140, 0, 0, 0, 0, 99, 0, 0, 0, 0, 0, 0, 151, 0, 80, 0, 0, 0, 0, 0],     # Sibiu
    [118, 0, 0, 0, 0, 0, 0, 0, 0, 111, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],       # Timisoara
    [0, 85, 0, 0, 0, 0, 0, 98, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 142, 0],       # Urziceni
    [0, 0, 0, 0, 0, 0, 0, 0, 92, 0, 0, 0, 0, 0, 0, 0, 0, 142, 0, 0],        # Vaslui
    [75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 71, 0, 0, 0, 0, 0, 0, 0]          # Zerind
]

# Initialize the peromone array as a copy of the distances array, with INITIAL_PHEROMONE in place of the distance.
pheromones = [[INITIAL_PHEROMONE if distance != 0 else 0 for distance in row] for row in distances]