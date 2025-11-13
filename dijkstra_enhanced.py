import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
from queue import PriorityQueue
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use('TkAgg')

class DijkstraVisualizer:
    def __init__(self):
        # Initialize graph
        self.G = nx.Graph()
        self.pos = None
        self.states = []
        self.root = None
        self.main_frame = None
        self.fig = None
        self.ax = None
        self.canvas = None
        self.text_widget = None

    def initialize_gui(self):
        """Initialize the GUI components after getting user input."""
        # Create the main window
        self.root = tk.Tk()
        self.root.title("Dijkstra's Algorithm Visualization")
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create matplotlib figure
        self.fig = plt.figure(figsize=(10, 6))
        self.ax = self.fig.add_subplot(111)
        
        # Embed matplotlib figure in tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create text frame for explanations
        text_frame = ttk.Frame(self.main_frame)
        text_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
        
        # Create scrolled text widget
        self.text_widget = tk.Text(text_frame, wrap=tk.WORD, width=50)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text_widget.yview)
        self.text_widget.configure(yscrollcommand=scrollbar.set)
        
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def create_weighted_graph(self, n_nodes):
        """Create a graph with user-input weights."""
        self.G.clear()
        print("\nEnter the weights for each edge (0 for no edge):")
        print("Example: For edge 0-1, weight 5, enter '5' when prompted")
        
        # Create adjacency matrix with user input
        adj_matrix = []
        for i in range(n_nodes):
            row = []
            for j in range(n_nodes):
                if i == j:
                    row.append(0)
                elif j > i:
                    while True:
                        try:
                            weight = int(input(f"Enter weight for edge {i}-{j} (0 for no edge): "))
                            if weight >= 0:
                                break
                            print("Weight must be non-negative!")
                        except ValueError:
                            print("Please enter a valid number!")
                    row.append(weight)
                else:
                    row.append(adj_matrix[j][i])  # Mirror the matrix
            adj_matrix.append(row)
            print(f"Current matrix row {i}:", row)
        
        # Create edges from adjacency matrix
        for i in range(n_nodes):
            for j in range(i + 1, n_nodes):
                if adj_matrix[i][j] > 0:
                    self.G.add_edge(i, j, weight=adj_matrix[i][j])
        
        if not nx.is_connected(self.G):
            print("\nWarning: The graph is not connected! Some nodes may be unreachable.")
        
        self.pos = nx.spring_layout(self.G)
        return self.G

    def dijkstra_with_states(self, start_node):
        """Perform Dijkstra's algorithm and record states for visualization."""
        self.states = []
        n_nodes = self.G.number_of_nodes()
        
        distances = {node: float('infinity') for node in self.G.nodes()}
        distances[start_node] = 0
        predecessors = {node: None for node in self.G.nodes()}
        pq = PriorityQueue()
        pq.put((0, start_node))
        visited = set()
        
        # Record initial state
        self.states.append({
            'distances': distances.copy(),
            'current': start_node,
            'visited': visited.copy(),
            'edges_in_path': [],
            'predecessors': predecessors.copy(),
            'status': f'Starting from node {start_node}',
            'checking': None,
            'phase': 'start'
        })
        
        while not pq.empty():
            current_distance, current = pq.get()
            
            if current in visited:
                continue
                
            visited.add(current)
            
            # Record state when visiting a new node
            current_paths = self._get_current_paths(predecessors)
            self.states.append({
                'distances': distances.copy(),
                'current': current,
                'visited': visited.copy(),
                'edges_in_path': current_paths,
                'predecessors': predecessors.copy(),
                'status': f'Processing node {current} (distance: {current_distance})',
                'phase': 'visit'
            })
            
            for neighbor in self.G.neighbors(current):
                if neighbor in visited:
                    continue
                
                edge_weight = self.G[current][neighbor]['weight']
                distance = current_distance + edge_weight
                
                # Record state when checking a neighbor
                self.states.append({
                    'distances': distances.copy(),
                    'current': current,
                    'checking': neighbor,
                    'visited': visited.copy(),
                    'edges_in_path': current_paths,
                    'predecessors': predecessors.copy(),
                    'status': (f'Checking edge {current}-{neighbor} (weight: {edge_weight})\n'
                             f'Current distance to {neighbor}: {distances[neighbor]}\n'
                             f'Potential new distance: {distance}'),
                    'edge_weight': edge_weight,
                    'potential_distance': distance,
                    'phase': 'check'
                })
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current
                    pq.put((distance, neighbor))
                    
                    # Record state when updating a distance
                    self.states.append({
                        'distances': distances.copy(),
                        'current': current,
                        'updated': neighbor,
                        'visited': visited.copy(),
                        'edges_in_path': self._get_current_paths(predecessors),
                        'predecessors': predecessors.copy(),
                        'status': f'Updated distance to node {neighbor}: {distance}',
                        'phase': 'update'
                    })
        
        # Record final state
        self.states.append({
            'distances': distances,
            'current': None,
            'visited': visited,
            'edges_in_path': self._get_current_paths(predecessors),
            'predecessors': predecessors,
            'status': 'Algorithm completed!',
            'phase': 'complete'
        })
        
        return distances, predecessors

    def _get_current_paths(self, predecessors):
        """Get the current shortest paths based on predecessors."""
        edges = []
        for node, pred in predecessors.items():
            if pred is not None:
                edges.append((pred, node))
        return edges

    def update_text(self, state):
        """Update the text widget with current state information."""
        self.text_widget.delete(1.0, tk.END)
        
        # Add algorithm status
        self.text_widget.insert(tk.END, "Dijkstra's Algorithm Status\n")
        self.text_widget.insert(tk.END, "=" * 40 + "\n\n")
        
        # Add adjacency matrix
        self.text_widget.insert(tk.END, "Adjacency Matrix:\n")
        self.text_widget.insert(tk.END, "-" * 20 + "\n")
        n_nodes = len(self.G.nodes())
        # Header row
        self.text_widget.insert(tk.END, "   ")
        for j in range(n_nodes):
            self.text_widget.insert(tk.END, f"{j:3}")
        self.text_widget.insert(tk.END, "\n")
        # Matrix rows
        for i in range(n_nodes):
            self.text_widget.insert(tk.END, f"{i:2}")
            for j in range(n_nodes):
                weight = self.G.get_edge_data(i, j, {'weight': 0})['weight'] if self.G.has_edge(i, j) else 0
                self.text_widget.insert(tk.END, f"{weight:3}")
            self.text_widget.insert(tk.END, "\n")
        self.text_widget.insert(tk.END, "\n")
        
        # Add current status
        self.text_widget.insert(tk.END, "Current Status:\n")
        self.text_widget.insert(tk.END, "-" * 20 + "\n")
        self.text_widget.insert(tk.END, state['status'] + "\n\n")
        
        # Add distance table
        self.text_widget.insert(tk.END, "Distance Table:\n")
        self.text_widget.insert(tk.END, "-" * 20 + "\n")
        distances = state['distances']
        for node in sorted(self.G.nodes()):
            dist = distances[node]
            self.text_widget.insert(tk.END, f"Node {node}: {dist if dist != float('infinity') else '∞'}\n")
        
        # Add path information
        self.text_widget.insert(tk.END, "\nShortest Paths:\n")
        self.text_widget.insert(tk.END, "-" * 20 + "\n")
        for node in sorted(self.G.nodes()):
            path = self._get_path_to_node(node, state['predecessors'])
            if path:
                self.text_widget.insert(tk.END, f"To node {node}: {' -> '.join(map(str, path))}\n")
            else:
                self.text_widget.insert(tk.END, f"To node {node}: No path found\n")
        
        # Add extra information based on the phase
        self.text_widget.insert(tk.END, "\nDetailed Information:\n")
        self.text_widget.insert(tk.END, "-" * 20 + "\n")
        
        if state['phase'] == 'check':
            self.text_widget.insert(tk.END, f"Examining edge weight: {state.get('edge_weight')}\n")
            self.text_widget.insert(tk.END, f"Potential new distance: {state.get('potential_distance')}\n")
        
        # Add progress information
        self.text_widget.insert(tk.END, "\nProgress:\n")
        self.text_widget.insert(tk.END, "-" * 20 + "\n")
        visited = state['visited']
        remaining = set(self.G.nodes()) - visited
        self.text_widget.insert(tk.END, f"Visited nodes: {sorted(list(visited))}\n")
        self.text_widget.insert(tk.END, f"Remaining nodes: {sorted(list(remaining))}\n")

    def _get_path_to_node(self, node, predecessors):
        """Reconstruct path to a node from predecessors."""
        path = []
        current = node
        while current is not None:
            path.append(current)
            current = predecessors[current]
        return list(reversed(path)) if path else []

    def animate(self, interval=1000):
        """Create animation of Dijkstra's algorithm."""
        # Initialize GUI if not already initialized
        if self.root is None:
            self.initialize_gui()
            
        def update(frame):
            self.ax.clear()
            state = self.states[frame]
            
            # Draw all edges in light gray
            edge_colors = ['lightgray' for _ in self.G.edges()]
            nx.draw_networkx_edges(self.G, self.pos, edge_color=edge_colors, ax=self.ax)
            
            # Draw edge labels (weights)
            edge_labels = {(u, v): d['weight'] for (u, v, d) in self.G.edges(data=True)}
            nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=edge_labels)
            
            # Draw shortest path edges in green
            if state['edges_in_path']:
                nx.draw_networkx_edges(self.G, self.pos, edgelist=state['edges_in_path'],
                                     edge_color='g', width=2)
            
            # Draw nodes with different colors
            node_colors = ['lightblue' for _ in self.G.nodes()]
            
            # Color visited nodes
            for node in state['visited']:
                node_colors[node] = 'lightgreen'
            
            # Color current node
            if state.get('current') is not None:
                node_colors[state['current']] = 'red'
            
            # Color node being checked
            if state.get('checking') is not None:
                node_colors[state['checking']] = 'yellow'
            
            # Color updated node
            if state.get('updated') is not None:
                node_colors[state['updated']] = 'orange'
            
            # Draw all nodes
            nx.draw_networkx_nodes(self.G, self.pos, node_color=node_colors,
                                 node_size=500, ax=self.ax)
            
            # Add node labels with distances
            distances = state['distances']
            labels = {node: f'{node}\n({distances[node] if distances[node] != float("infinity") else "∞"})'
                     for node in self.G.nodes()}
            nx.draw_networkx_labels(self.G, self.pos, labels)
            
            # Update title
            self.ax.set_title(f"Dijkstra's Algorithm Visualization\nStep {frame + 1}/{len(self.states)}")
            
            # Add legend
            from matplotlib.patches import Patch
            legend_elements = [
                Patch(facecolor='lightblue', label='Unvisited'),
                Patch(facecolor='lightgreen', label='Visited'),
                Patch(facecolor='red', label='Current Node'),
                Patch(facecolor='yellow', label='Being Checked'),
                Patch(facecolor='orange', label='Distance Updated'),
                Patch(facecolor='green', label='Shortest Path')
            ]
            self.ax.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5))
            
            self.ax.axis('off')
            
            # Update text information
            self.update_text(state)
            
            # Scroll to top of text widget
            self.text_widget.see("1.0")
        
        anim = animation.FuncAnimation(self.fig, update, frames=len(self.states),
                                     interval=interval, repeat=False)
        self.root.mainloop()

def get_user_input():
    print("\nDijkstra's Algorithm Visualizer")
    print("==============================")
    
    while True:
        try:
            n_nodes = int(input("\nEnter number of nodes (2-10): "))
            if 2 <= n_nodes <= 10:
                break
            print("Please enter a number between 2 and 10.")
        except ValueError:
            print("Please enter a valid number!")
    
    return n_nodes

def main():
    print("\nWelcome to Dijkstra's Algorithm Visualizer")
    print("====================================")
    
    # Get user input for number of nodes
    n_nodes = get_user_input()
    
    # Create and set up the visualizer
    visualizer = DijkstraVisualizer()
    
    # Create graph with user input weights
    print("\nNow you'll enter the weights for the graph edges.")
    print("Use 0 for no connection between nodes.")
    print("Example: Weight 5 between nodes 0 and 1 means the distance is 5.\n")
    
    G = visualizer.create_weighted_graph(n_nodes)
    
    # Get start node
    while True:
        try:
            start_node = int(input(f"\nEnter start node (0-{n_nodes-1}, default 0): ") or "0")
            if 0 <= start_node < n_nodes:
                break
            print(f"Invalid start node! Please enter a number between 0 and {n_nodes-1}.")
        except ValueError:
            print("Please enter a valid number!")
    
    # Get animation speed
    while True:
        try:
            interval = int(input("\nEnter animation interval in ms (default 1000): ") or "1000")
            if interval > 0:
                break
            print("Invalid interval! Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number!")
    
    print(f"\nCreated a graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    print(f"\nStarting Dijkstra's algorithm from node {start_node}")
    
    # Run Dijkstra's algorithm and create visualization
    distances, predecessors = visualizer.dijkstra_with_states(start_node)
    
    # Display final distances
    print("\nFinal shortest distances from node", start_node)
    for node in sorted(distances.keys()):
        dist = distances[node]
        print(f"To node {node}: {dist if dist != float('infinity') else '∞'}")
    
    # Run the visualization
    visualizer.animate(interval)

if __name__ == "__main__":
    main()
