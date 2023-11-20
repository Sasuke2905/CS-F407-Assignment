import numpy as np
import matplotlib.pyplot as plt
import math
import random

def calculate_total_distance(tour, distance_matrix):
    total_distance = 0
    for i in range(len(tour) - 1):
        total_distance += distance_matrix[tour[i]][tour[i + 1]]
    total_distance += distance_matrix[tour[-1]][tour[0]]  # Return to the starting city
    return total_distance

def generate_neighbor(tour):
    # Randomly swap two cities in the tour to generate a neighbor
    neighbor = tour.copy()
    idx1, idx2 = random.sample(range(len(tour)), 2)
    neighbor[idx1], neighbor[idx2] = neighbor[idx2], neighbor[idx1]
    return neighbor

def simulated_annealing(distance_matrix, initial_temperature=1000, cooling_rate=0.995, num_iterations=5000):
    num_cities = len(distance_matrix)
    
    # Generate an initial tour (random permutation of cities)
    current_tour = list(range(num_cities))
    random.shuffle(current_tour)
    
    # Initialize the best tour and its distance
    best_tour = current_tour.copy()
    best_distance = calculate_total_distance(best_tour, distance_matrix)
    
    # Initialize temperature
    temperature = initial_temperature
    
    # Simulated Annealing main loop
    for iteration in range(num_iterations):
        # Generate a neighboring solution
        neighbor_tour = generate_neighbor(current_tour)
        
        # Calculate the distances for current and neighbor tours
        current_distance = calculate_total_distance(current_tour, distance_matrix)
        neighbor_distance = calculate_total_distance(neighbor_tour, distance_matrix)
        
        # Decide whether to accept the neighbor
        if neighbor_distance < current_distance or random.random() < math.exp((current_distance - neighbor_distance) / temperature):
            current_tour = neighbor_tour.copy()
        
        # Update the best tour if needed
        if neighbor_distance < best_distance:
            best_tour = neighbor_tour.copy()
            best_distance = neighbor_distance
        
        # Cool down the temperature
        temperature *= cooling_rate
    
    return best_tour, best_distance

def plot_tour(tour, cities):
    x = [cities[i][0] for i in tour]
    y = [cities[i][1] for i in tour]
    
    # Connect the last city to the starting city
    x.append(x[0])
    y.append(y[0])
    
    plt.plot(x, y, marker='o', linestyle='-')
    plt.scatter(x, y, color='red')
    plt.title('TSP Tour - Simulated Annealing')
    plt.xlabel('X-coordinate')
    plt.ylabel('Y-coordinate')
    plt.show()

if __name__ == "__main__":
    np.random.seed(52)
    
    # Example coordinates of cities
    cities = np.random.rand(7, 2) * 100
    # Example distance matrix
    distance_matrix = np.linalg.norm(cities[:, np.newaxis, :] - cities, axis=-1)
    
    # Solve TSP using Simulated Annealing
    optimal_tour, optimal_distance = simulated_annealing(distance_matrix)
    
    # Print the result
    print(f"The optimal TSP tour is: {optimal_tour}")
    print(f"The optimal distance is: {optimal_distance}")
    
    # Plot the optimal tour
    plot_tour(optimal_tour, cities)
