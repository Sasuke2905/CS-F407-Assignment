import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from simulates_annealing import simulated_annealing
from tabu_search import taboo_search

class TSPSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TSP Solver GUI")

        self.num_cities = 10  # Number of cities for generating random coordinates

        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')

        # Create tabs for each algorithm
        self.tab_simulated_annealing = ttk.Frame(self.notebook)
        self.tab_taboo_search = ttk.Frame(self.notebook)

        # Add tabs to the notebook
        self.notebook.add(self.tab_simulated_annealing, text='Simulated Annealing')
        self.notebook.add(self.tab_taboo_search, text='Tabu Search')

        # Set up content for each tab
        self.setup_simulated_annealing_tab()
        self.setup_taboo_search_tab()

    def setup_simulated_annealing_tab(self):
        self.frame_simulated_annealing = ttk.Frame(self.tab_simulated_annealing)
        self.frame_simulated_annealing.pack()

        self.button_run_simulated_annealing = ttk.Button(self.frame_simulated_annealing,
                                                          text='Run Simulated Annealing',
                                                          command=self.run_simulated_annealing)
        self.button_run_simulated_annealing.pack(pady=10)

    def setup_taboo_search_tab(self):
        self.frame_taboo_search = ttk.Frame(self.tab_taboo_search)
        self.frame_taboo_search.pack()

        self.button_run_taboo_search = ttk.Button(self.frame_taboo_search,
                                                  text='Run Tabu Search',
                                                  command=self.run_taboo_search)
        self.button_run_taboo_search.pack(pady=10)

    def generate_random_cities(self):
        return np.random.rand(self.num_cities, 2) * 100

    def run_simulated_annealing(self):
        try:
            cities = self.generate_random_cities()
            distance_matrix = np.linalg.norm(cities[:, np.newaxis, :] - cities, axis=-1)
            optimal_tour, optimal_distance = simulated_annealing(distance_matrix)

            self.plot_tour(optimal_tour, cities, 'Simulated Annealing')
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run_taboo_search(self):
        try:
            cities = self.generate_random_cities()
            distance_matrix = np.linalg.norm(cities[:, np.newaxis, :] - cities, axis=-1)
            optimal_tour, optimal_distance = taboo_search(distance_matrix)

            self.plot_tour(optimal_tour, cities, 'Tabu Search')
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def plot_tour(self, tour, cities, algorithm_name):
        fig, ax = plt.subplots()
        x = [cities[i][0] for i in tour]
        y = [cities[i][1] for i in tour]
        x.append(x[0])
        y.append(y[0])
        ax.plot(x, y, marker='o', linestyle='-')
        ax.scatter(x, y, color='red')
        ax.set_title(f'TSP Tour - {algorithm_name}')
        ax.set_xlabel('X-coordinate')
        ax.set_ylabel('Y-coordinate')

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(expand=True, fill='both')
        canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = TSPSolverApp(root)
    root.mainloop()
