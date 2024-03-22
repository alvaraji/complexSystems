# Import data_setup module
import initialize_ACO # Initialize the graph and pheromone matrix
import ant

ITERATIONS = 1000

def main():

	# Calculate tours for each ant for number of iterations
	for iteration in range(ITERATIONS):
    
    # Ant Movement
    for ant in ants:
        ant.construct_solution()

    # Global Pheromone Update
    for ant in ants:
        ant.update_pheromone()

    # Check for termination criteria (Early convergence)
    # if termination_criteria_met():
    #     break


if __name__ == "__main__":
    main()