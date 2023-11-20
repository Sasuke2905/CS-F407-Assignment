import heapq
import itertools


class Node:
    def __init__(self, city, parent=None, cost=0, heuristic=0):
        self.city = city
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


def calculate_heuristic(current_city, remaining_cities):
    # In TSP, a common heuristic is the minimum spanning tree (MST) cost of the remaining cities.
    # This is a relaxed lower bound on the actual cost.
    min_cost = float('inf')
    for perm in itertools.permutations(remaining_cities):
        cost = 0
        prev_city = current_city
        for city in perm:
            cost += distance_matrix[prev_city][city]
            prev_city = city
        cost += distance_matrix[prev_city][current_city]  # Return to starting city
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
                # Return to the starting city to complete the tour
                return current_node.cost + distance_matrix[current_node.city][start_city]

            for next_city in range(num_cities):
                if next_city not in visited:
                    new_cost = current_node.cost + distance_matrix[current_node.city][next_city]
                    new_heuristic = calculate_heuristic(next_city, visited)
                    new_node = Node(next_city, current_node, new_cost, new_heuristic)
                    heapq.heappush(priority_queue, new_node)

    return float('inf')


if __name__ == "__main__":
    # Example distance matrix (replace with your own)
    distance_matrix = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]

    num_cities = len(distance_matrix)

    start_city = 0  # Starting city index
    optimal_cost = astar_tsp(start_city)

    if optimal_cost != float('inf'):
        print(f"The optimal cost of the TSP tour is: {optimal_cost}")
    else:
        print("No valid tour found.")
