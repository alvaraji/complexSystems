import random

class Ant:
    def __init__(self, graph, pheromone_matrix, alpha, beta):
        self.graph = graph
        self.pheromone_matrix = pheromone_matrix
        self.alpha = alpha  # Alpha parameter for balancing pheromone vs. heuristic information
        self.beta = beta    # Beta parameter for balancing pheromone vs. heuristic information
        
        self.starting_city = random.randint(0, len(graph) - 1)  # Come up with starting city
        self.current_city = self.starting_city                  # Set it as current_city
        self.path = [self.starting_city]                        # Initialize the path array
        self.visited = set()                                    # Set to keep track of visited cities
        self.visited.add(self.starting_city)                    # Add starting city

    def select_next_city(self):
        # Implement the ant's decision rule to select the next city
        # This can be based on pheromone levels and heuristic information
        # Example: use a probabilistic decision based on pheromone and heuristic values
        # Update self.current_city and add it to self.visited

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

        self.current_city = random.choices(choices_index, weights=probabilities)[0] # Pick a path at random weighted with probabilities

        return self.current_city


    def construct_solution(self):

        next_city = 0

        # Construct a solution by iteratively selecting next cities until all cities are visited, and returned home.
        while (len(self.visited) < len(self.graph)) or (next_city != self.starting_city):
            next_city = self.select_next_city()
            self.visited.add(next_city)
            self.path.append(next_city)

    def reset(self, updated_pheromone_matrix):

        # Pick a new random starting point
        self.current_city = random.randint(0, len(self.graph) - 1)
        self.starting_city = self.current_city

        # Pass the updated pheromone matrix
        self.pheromone_matrix = updated_pheromone_matrix

        # Reset path
        self.path = [self.starting_city]
        self.visited = set()

    def eval(self, index):

        # Get pheromone level and distance for current index
        pheromone_level = self.pheromone_matrix[self.current_city][index]
        distance = self.graph[self.current_city][index]

        # Calculate the probability of making this choice
        probability = (pheromone_level ** self.alpha) * ((1/distance) ** self.beta)

        return probability # Not yet normalized

    def print(self, number, cities):

        print("Ant number: %d\n" % number)
        print("\tpath:\n[", end='')
        for p in self.path:
            print(cities[p], end='')
            if p != len(self.path):
                print(" --> ", end='')

        print("]")
