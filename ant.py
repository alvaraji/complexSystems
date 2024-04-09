import random
import numpy as np

class Ant:
    def __init__(self, graph, pheromone_matrix, alpha, beta):

        self.graph = graph                                  
        self.pheromone_matrix = pheromone_matrix
        self.deposited_pheromone_matrix = np.zeros((len(self.graph), len(self.graph[0]))) # Initalize zero array for saving pheromone deposits

        self.alpha = alpha  # Alpha parameter for balancing pheromone vs. heuristic information
        self.beta = beta    # Beta parameter for balancing pheromone vs. heuristic information
        
        self.starting_city = random.randint(0, len(graph) - 1)  # Come up with starting city
        self.current_city = self.starting_city                  # Set it as current_city
        self.path = [self.starting_city]                        # Initialize the path array
        self.visited = set()                                    # Set to keep track of visited cities
        self.visited.add(self.starting_city)                    # Add starting city

    # Decision function to select the ants next city
    def select_next_city(self):

        probabilities = []
        choices_index = []
        index = 0

        for choice in self.graph[self.current_city]:
            
            # Best choice will be random weighted choice from eval function

            if choice != 0: # If there is a road to take. There should always be at least one road.

                probabilities.append(self.eval(index)) # Array to calculate probabilities
                choices_index.append(index) # Save the indexes of the possible choices

            index += 1

        # Normalize
        total_prob = sum(probabilities)
        probabilities = [prob / total_prob for prob in probabilities]

        # Pick a path at random, weighted with probabilities
        self.current_city = random.choices(choices_index, weights=probabilities)[0]

        return self.current_city

    # Come up with the ant's weighted random walk
    def construct_solution(self):

        next_city = self.starting_city

        # Ant will keep selecting cities until all are visited, and the ant returns home.
        while (len(self.visited) < len(self.graph)) or (next_city != self.starting_city):

            last_city = next_city
            
            # The any will randomly choose the next city based on weighted probabilities
            next_city = self.select_next_city()

            # Deposit pheromone
            self.deposited_pheromone_matrix[last_city][next_city] += 1
            self.deposited_pheromone_matrix[next_city][last_city] += 1

            # Record and continue
            self.visited.add(next_city)
            self.path.append(next_city)

    def reset(self, new_pheromone_matrix):

        # Pick a new random starting point
        self.current_city = random.randint(0, len(self.graph) - 1)
        self.starting_city = self.current_city

        # Pass the updated pheromone matrix
        self.pheromone_matrix = new_pheromone_matrix

        # Reset path
        self.path = [self.starting_city]
        self.visited = set()

    # Calculate the probability of a given edge from current city
    def eval(self, index):

        # Get pheromone level and distance for current index
        pheromone_level = self.pheromone_matrix[self.current_city][index]
        distance = self.graph[self.current_city][index]

        # Calculate the probability of making this choice
        probability = (pheromone_level ** self.alpha) * ((1/distance) ** self.beta)

        return probability # Not yet normalized


    # For printing/debugging purposes
    def print(self, number, cities):

        print("Ant number: %d\n" % number)
        print("\tpath:\n[", end='')
        for p in self.path:
            print(cities[p], end='')
            if p != len(self.path):
                print(" --> ", end='')

        print("]")

    # This will look into distance matrix and output how far the ant walked
    def pathLength(self):

        total_distance = 0
        k = 0

        while k < len(self.path)-1:
            total_distance += self.graph[self.path[k]][self.path[k+1]]
            k += 1

        return total_distance

    def startingCity(self):
        return self.starting_city
    

