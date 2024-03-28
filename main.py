# Import data_setup module
import initialize_ACO # Initialize the graph and pheromone matrix
import ant as Ant # Import ant class definition
import numpy as np

ITERATIONS = 30
NUM_ANTS = 30

ALPHA = 0.7 # Pheromone factor
BETA = 0.2 # Distance factor
GAMMA = 0.99 # Evaporation factor

def main():


    # Create the first colony
    ants_colony_A = [Ant.Ant(initialize_ACO.distances, initialize_ACO.pheromones, ALPHA, BETA) for _ in range(NUM_ANTS)]
    convergence = []

    # Calculate tours for each ant for number of iterations
    for iteration in range(ITERATIONS):
    
        # Ant Movement
        for ant in ants_colony_A:
            ant.construct_solution()

        # Global Pheromone Update
        sum_matrix = np.zeros((len(initialize_ACO.distances), len(initialize_ACO.distances[0])))

        # Sum all the matricies from all the ants
        for ant in ants_colony_A:
            sum_matrix = sum_matrix + ant.deposited_pheromone_matrix

        # Divide by number of ants, so we can change number without modifying alpha
        sum_matrix = sum_matrix / NUM_ANTS

        # Evaporation
        updated_pheromones = sum_matrix * GAMMA

        total_length = 0
        
        #Get average path length to measure convergence
        for ant in ants_colony_A:
            total_length += ant.pathLength()

        convergence.append(total_length/NUM_ANTS)

        # index = 0
        # for a in ants_colony_A:
        #     a.print(index, initialize_ACO.cities)
        #     index += 1

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