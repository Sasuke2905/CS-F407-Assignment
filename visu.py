import heapq
import itertools
import matplotlib.pyplot as plt
import numpy as np

class Node:
    def __init__(self, city, parent=None, cost=0, heuristic=0):
        self.city = city
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic
    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

def calculate_heuristic(current_city, remaining_cities):
    min_cost = float('inf')
    for perm in itertools.permutations(remaining_cities):
        cost = 0
        prev_city = current_city
        for city in perm:
            cost += distance_matrix[prev_city][city]
            prev_city = city
        cost += distance_matrix[prev_city][current_city]
        min_cost = min(min_cost, cost)

    return min_cost


def astar_tsp(start_city):
    initial_node = Node(start_city)
    priority_queue = [initial_node]
    visited = set()

    while priority_queue:
        current_node = heapq.heappop(priority_queue)

        if current_node.city not in visited:
            visited.add(current_node.city)

            if len(visited) == num_cities:
                tour = []
                while current_node:
                    tour.append(current_node.city)
                    current_node = current_node.parent
                return tour[::-1]  # Reverse the tour to start from the initial city

            for next_city in range(num_cities):
                if next_city not in visited:
                    new_cost = current_node.cost + distance_matrix[current_node.city][next_city]
                    new_heuristic = calculate_heuristic(next_city, visited)
                    new_node = Node(next_city, current_node, new_cost, new_heuristic)
                    heapq.heappush(priority_queue, new_node)

    return float('inf')


def plot_tour(tour):
    x = [cities[i][0] for i in tour]
    y = [cities[i][1] for i in tour]
    # Connect the last city to the starting city
    x.append(x[0])
    y.append(y[0])
    plt.plot(x, y, marker='o', linestyle='-')
    plt.scatter(x, y, color='red')
    plt.title('TSP Tour')
    plt.xlabel('X-coordinate')
    plt.ylabel('Y-coordinate')
    plt.show()

if __name__ == "__main__":
    np.random.seed(48)
    # Example coordinates of cities
    cities = np.random.rand(2, 25) * 100
    # Example distance matrix
    distance_matrix = np.linalg.norm(cities[:, np.newaxis, :] - cities, axis=-1)
    num_cities = len(distance_matrix)
    start_city = 0
    optimal_cost = astar_tsp(start_city)
    if optimal_cost != float('inf'):
        print(f"The optimal cost of the TSP tour is: {optimal_cost}")
        optimal_tour = astar_tsp(start_city)
        plot_tour(optimal_tour)
    else:
        print("No valid tour found.")
