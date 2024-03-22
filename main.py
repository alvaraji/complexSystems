# Import data_setup module
import initialize_ACO # Initialize the graph and pheromone matrix
import ant as Ant # Import ant class definition

ITERATIONS = 1000
NUM_ANTS = 500

ALPHA = 0.5
BETA = 0.5

def main():


	# Create the first colony
	ants_colony_A = [Ant(initialize_ACO.distances, initialize_ACO.pheromones, ALPHA, BETA) for _ in range(NUM_ANTS)]

	# Calculate tours for each ant for number of iterations
	for iteration in range(ITERATIONS):
    
	    # Ant Movement
	    for ant in ants_colony_A:
	        ant.construct_solution()

	    # Global Pheromone Update
	    for ant in ants_colony_A:
	        ant.update_pheromone()

		# Update evaporation
		# Update objective function

		# Prepare ants for next iteration
		for ant in ants_colony_A:
	        ant.reset()

	    if iteration % 5 == 0:
	    	# Visualization?

    # Check for termination criteria (Early convergence, objective function)
    # if termination_criteria_met():
    #     break


if __name__ == "__main__":
    main()