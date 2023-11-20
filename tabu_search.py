import numpy as np
import matplotlib.pyplot as plt
import random

def calculate_total_distance(tour, distance_matrix):
    total_distance = 0
    for i in range(len(tour) - 1):
        total_distance += distance_matrix[tour[i]][tour[i + 1]]
    total_distance += distance_matrix[tour[-1]][tour[0]]  # Return to the starting city
    return total_distance

def generate_initial_solution(num_cities):
    initial_solution = list(range(num_cities))
    random.shuffle(initial_solution)
    return initial_solution

def generate_neighbor(solution):
    # Swap two random cities to generate a neighbor
    neighbor = solution.copy()
    idx1, idx2 = random.sample(range(len(solution)), 2)
    neighbor[idx1], neighbor[idx2] = neighbor[idx2], neighbor[idx1]
    return neighbor

def is_tabu_move(move, tabu_list):
    return tuple(move) in tabu_list

def update_tabu_list(tabu_list, max_tabu_size, move):
    if len(tabu_list) >= max_tabu_size:
        tabu_list.pop(0)
    tabu_list.append(tuple(move))

def taboo_search(distance_matrix, max_iterations=100, max_tabu_size=10):
    num_cities = len(distance_matrix)
    
    # Generate an initial solution
    current_solution = generate_initial_solution(num_cities)
    
    # Initialize the best solution and its distance
    best_solution = current_solution.copy()
    best_distance = calculate_total_distance(best_solution, distance_matrix)
    
    # Initialize tabu list
    tabu_list = []
    
    # Taboo Search main loop
    for iteration in range(max_iterations):
        # Generate a neighbor solution
        neighbor_solution = generate_neighbor(current_solution)
        
        # Calculate the distances for current and neighbor solutions
        current_distance = calculate_total_distance(current_solution, distance_matrix)
        neighbor_distance = calculate_total_distance(neighbor_solution, distance_matrix)
        
        # Check if the move is tabu or leads to a better solution
        if neighbor_distance < current_distance or not is_tabu_move((current_solution[0], current_solution[-1]), tabu_list):
            current_solution = neighbor_solution.copy()
        
        # Update the best solution if needed
        if neighbor_distance < best_distance:
            best_solution = neighbor_solution.copy()
            best_distance = neighbor_distance
        
        # Update tabu list
        update_tabu_list(tabu_list, max_tabu_size, (current_solution[0], current_solution[-1]))
    
    return best_solution, best_distance

def plot_tour(tour, cities):
    x = [cities[i][0] for i in tour]
    y = [cities[i][1] for i in tour]
    
    # Connect the last city to the starting city
    x.append(x[0])
    y.append(y[0])
    
    plt.plot(x, y, marker='o', linestyle='-')
    plt.scatter(x, y, color='red')
    plt.title('TSP Tour - Tabu Search')
    plt.xlabel('X-coordinate')
    plt.ylabel('Y-coordinate')
    plt.show()

if __name__ == "__main__":
    np.random.seed(47)
    
    # Example coordinates of cities
    cities = np.random.rand(9, 2) * 100
    
    # Example distance matrix (replace with your own)
    distance_matrix = np.linalg.norm(cities[:, np.newaxis, :] - cities, axis=-1)
    
    # Solve TSP using Tabu Search
    optimal_tour, optimal_distance = taboo_search(distance_matrix)
    
    # Print the result
    print(f"The optimal TSP tour is: {optimal_tour}")
    print(f"The optimal distance is: {optimal_distance}")
    
    # Plot the optimal tour
    plot_tour(optimal_tour, cities)
