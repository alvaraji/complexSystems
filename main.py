# Import data_setup module
import initialize_ACO # Initialize the graph and pheromone matrix
import ant as Ant # Import ant class definition
import numpy as np
import statistics

ITERATIONS = 500
NUM_ANTS = 100

ALPHA = 3 # Pheromone factor
BETA = 2 # Distance factor
GAMMA = 0.9 # Evaporation factor
STARTINGCITY = 1 # Used when doing single city start

def main():


    # Create the first colony
    ants_colony_A = [Ant.Ant(initialize_ACO.distances, initialize_ACO.pheromones[0], ALPHA, BETA, STARTINGCITY) for _ in range(NUM_ANTS)]
    convergence = []
    sum_matrix = []

    # Calculate tours for each ant for number of iterations
    for iteration in range(ITERATIONS):

    
        # Ant Movement
        for ant in ants_colony_A:
            ant.construct_solution()


        # sum_matrix = []
        # City Pheromone Update
        for _ in initialize_ACO.distances:
            sum_matrix.append(np.zeros((len(initialize_ACO.distances), len(initialize_ACO.distances[0]))))

        # Sum all the matricies from all the ants for their city
        for ant in ants_colony_A:
            sum_matrix[ant.starting_city] = sum_matrix[ant.starting_city] + ant.deposited_pheromone_matrix

        # Divide by number of ants, so we can change ant count without modifying alpha
        for k in range(len(sum_matrix)):
            #sum_matrix[k] = sum_matrix[k] / NUM_ANTS
            sum_matrix[k] = sum_matrix[k] * GAMMA # Evaporation

        total_length = 0
        
        #Get average path length to measure convergence
        for ant in ants_colony_A:
            total_length += ant.pathLength()

        convergence.append(total_length/NUM_ANTS)

        # index = 0
        # for a in ants_colony_A:
        #     a.print(index, initialize_ACO.cities)
        #     index += 1

        if iteration == 5 or iteration == 150:
            ants_colony_A[5].printVariables()
            ants_colony_A[5].print(5, initialize_ACO.cities)

        # Prepare ants for next iteration, pass updated pheromones
        for ant in ants_colony_A:
            ant.reset(sum_matrix[ant.starting_city], STARTINGCITY)

        # if iteration % 5 == 0:
        #     print("...")
        #     print(sum_matrix[1])
        #     print(ants_colony_A[1].path)
            

    print(convergence) # Print the iterations path length results

    # Print the first 5 and the last 5 elements, averaged to see if there's any improvement
    print(statistics.mean(convergence[:5]))
    print(statistics.mean(convergence[-5:]))

    # Check for termination criteria (Early convergence, objective function)
    # if termination_criteria_met():
    #     break


if __name__ == "__main__":
    main()