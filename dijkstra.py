import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import numpy as np
from queue import PriorityQueue
import time

class DijkstraVisualizer:
    def __init__(self):
        self.G = nx.Graph()
        self.pos = None
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.states = []
        
    def generate_weighted_graph(self, n_nodes=8, n_edges=12, min_weight=1, max_weight=10):
        """Generate a random connected weighted graph."""
        # Create a random connected graph
        while True:
            # First ensure we have a connected path through all nodes
            edges = [(i, i+1) for i in range(n_nodes-1)]
            
            # Add random edges
            possible_edges = [(i, j) for i in range(n_nodes) for j in range(i+1, n_nodes)]
            possible_edges = [e for e in possible_edges if e not in edges]
            additional_edges = random.sample(possible_edges, min(n_edges - (n_nodes-1), len(possible_edges)))
            edges.extend(additional_edges)
            
            self.G.clear()
            # Add edges with random weights
            for edge in edges:
                weight = random.randint(min_weight, max_weight)
                self.G.add_edge(edge[0], edge[1], weight=weight)
            
            if nx.is_connected(self.G):
                break
        
        self.pos = nx.spring_layout(self.G)
        return self.G

    def dijkstra_with_states(self, start_node):
        """Perform Dijkstra's algorithm and record states for visualization."""
        self.states = []
        n_nodes = self.G.number_of_nodes()
        
        # Initialize distances
        distances = {node: float('infinity') for node in self.G.nodes()}
        distances[start_node] = 0
        
        # Initialize predecessors for path reconstruction
        predecessors = {node: None for node in self.G.nodes()}
        
        # Priority queue for nodes to visit
        pq = PriorityQueue()
        pq.put((0, start_node))
        
        # Set of visited nodes
        visited = set()
        
        # Record initial state
        self.states.append({
            'distances': distances.copy(),
            'current': start_node,
            'visited': visited.copy(),
            'edges_in_path': [],
            'status': f'Starting from node {start_node}'
        })
        
        while not pq.empty():
            current_distance, current = pq.get()
            
            if current in visited:
                continue
                
            visited.add(current)
            
            # Record state when visiting a new node
            current_paths = self._get_current_paths(predecessors, visited)
            self.states.append({
                'distances': distances.copy(),
                'current': current,
                'visited': visited.copy(),
                'edges_in_path': current_paths,
                'status': f'Visiting node {current} (distance: {current_distance})'
            })
            
            # Check all neighbors
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
                    'status': f'Checking edge {current}-{neighbor} (weight: {edge_weight})'
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
                        'edges_in_path': self._get_current_paths(predecessors, visited | {neighbor}),
                        'status': f'Updated distance to node {neighbor}: {distance}'
                    })
        
        # Record final state
        final_paths = self._get_current_paths(predecessors, visited)
        self.states.append({
            'distances': distances.copy(),
            'current': None,
            'visited': visited.copy(),
            'edges_in_path': final_paths,
            'status': 'Algorithm completed!'
        })
        
        return distances, predecessors

    def _get_current_paths(self, predecessors, visited_nodes):
        """Get the current shortest paths based on predecessors."""
        edges = []
        for node in visited_nodes:
            pred = predecessors[node]
            if pred is not None:
                edges.append((pred, node))
        return edges

    def animate(self, interval=1000):
        """Create animation of Dijkstra's algorithm."""
        def update(frame):
            self.ax.clear()
            state = self.states[frame]
            
            # Create a second subplot for explanation text
            self.fig.set_size_inches(15, 10)
            gs = self.fig.add_gridspec(1, 2, width_ratios=[2, 1])
            ax_graph = self.fig.add_subplot(gs[0])
            ax_text = self.fig.add_subplot(gs[1])
            
            # Draw all edges in light gray
            edge_colors = ['lightgray' for _ in self.G.edges()]
            edge_weights = nx.get_edge_attributes(self.G, 'weight')
            nx.draw_networkx_edges(self.G, self.pos, edge_color=edge_colors, ax=ax_graph)
            
            # Draw edge labels (weights)
            edge_labels = {(u, v): d['weight'] for (u, v, d) in self.G.edges(data=True)}
            nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=edge_labels)
            
            # Draw shortest path edges in green
            if state['edges_in_path']:
                nx.draw_networkx_edges(self.G, self.pos, edgelist=state['edges_in_path'],
                                     edge_color='g', width=2, ax=ax_graph)
            
            # Draw all nodes in light blue
            nx.draw_networkx_nodes(self.G, self.pos, node_color='lightblue',
                                 node_size=500, ax=ax_graph)
            
            # Draw visited nodes in green
            if state['visited']:
                nx.draw_networkx_nodes(self.G, self.pos, nodelist=list(state['visited']),
                                     node_color='lightgreen', node_size=500, ax=ax_graph)
            
            # Draw current node in red
            if state.get('current') is not None:
                nx.draw_networkx_nodes(self.G, self.pos, nodelist=[state['current']],
                                     node_color='red', node_size=500, ax=ax_graph)
            
            # Draw node being checked in yellow
            if state.get('checking') is not None:
                nx.draw_networkx_nodes(self.G, self.pos, nodelist=[state['checking']],
                                     node_color='yellow', node_size=500, ax=ax_graph)
            
            # Draw recently updated node in orange
            if state.get('updated') is not None:
                nx.draw_networkx_nodes(self.G, self.pos, nodelist=[state['updated']],
                                     node_color='orange', node_size=500, ax=ax_graph)
            
            # Add distance labels to nodes
            distances = state['distances']
            labels = {node: f'{node}\n({distances[node] if distances[node] != float("infinity") else "∞"})'
                     for node in self.G.nodes()}
            nx.draw_networkx_labels(self.G, self.pos, labels, ax=ax_graph)
            
            # Update title
            ax_graph.set_title(f"Dijkstra's Algorithm Visualization\nStep {frame + 1}/{len(self.states)}")
            
            # Add legend to graph
            from matplotlib.patches import Patch
            legend_elements = [
                Patch(facecolor='lightblue', label='Unvisited'),
                Patch(facecolor='lightgreen', label='Visited'),
                Patch(facecolor='red', label='Current Node'),
                Patch(facecolor='yellow', label='Being Checked'),
                Patch(facecolor='orange', label='Distance Updated'),
                Patch(facecolor='lightgray', label='Unused Edge'),
                Patch(facecolor='green', label='Shortest Path')
            ]
            ax_graph.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5))
            
            # Add detailed explanation text
            ax_text.axis('off')
            explanation = [
                "Current Status:",
                "============",
                state['status'],
                "",
                "Algorithm Details:",
                "============",
                f"Current Node: {state.get('current', 'None')}",
            ]
            
            if state.get('checking') is not None:
                explanation.extend([
                    f"Checking Node: {state['checking']}",
                    f"Current Distance: {distances[state['current']]}",
                    f"Edge Weight: {self.G[state['current']][state['checking']]['weight']}",
                    f"Potential New Distance: {distances[state['current']] + self.G[state['current']][state['checking']]['weight']}"
                ])
            
            explanation.extend([
                "",
                "Distance Table:",
                "============"
            ])
            
            # Add current distances
            sorted_nodes = sorted(self.G.nodes())
            for node in sorted_nodes:
                dist = distances[node]
                dist_str = str(dist) if dist != float('infinity') else '∞'
                explanation.append(f"Node {node}: {dist_str}")
            
            # Add progress information
            explanation.extend([
                "",
                "Progress:",
                "============",
                f"Visited Nodes: {sorted(list(state['visited']))}",
                f"Remaining Nodes: {sorted(list(set(self.G.nodes()) - state['visited']))}"
            ])
            
            # Display explanation text
            y_pos = 0.95
            for line in explanation:
                ax_text.text(0.05, y_pos, line, fontsize=10, fontfamily='monospace')
                y_pos -= 0.04
            
            ax_graph.axis('off')
        
        anim = animation.FuncAnimation(self.fig, update, frames=len(self.states),
                                     interval=interval, repeat=False)
        plt.tight_layout()
        plt.show()

def get_user_input():
    print("\nDijkstra's Algorithm Visualizer")
    print("==============================")
    
    # Get graph parameters
    while True:
        try:
            n_nodes = int(input("\nEnter number of nodes (default 8): ") or "8")
            n_edges = int(input("Enter number of edges (default 12): ") or "12")
            min_weight = int(input("Enter minimum edge weight (default 1): ") or "1")
            max_weight = int(input("Enter maximum edge weight (default 10): ") or "10")
            
            if (n_nodes > 0 and n_edges >= n_nodes - 1 and 
                min_weight > 0 and max_weight >= min_weight):
                break
            print("Invalid values! Please ensure:")
            print("- Number of nodes is positive")
            print("- Number of edges is at least (nodes - 1)")
            print("- Weights are positive")
            print("- Max weight is >= min weight")
        except ValueError:
            print("Please enter valid numbers!")
    
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
    
    return n_nodes, n_edges, min_weight, max_weight, start_node, interval

def main():
    # Get user input
    n_nodes, n_edges, min_weight, max_weight, start_node, interval = get_user_input()
    
    # Create and set up the visualizer
    visualizer = DijkstraVisualizer()
    G = visualizer.generate_weighted_graph(n_nodes, n_edges, min_weight, max_weight)
    
    print(f"\nGenerated a random weighted graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    print(f"Edge weights range from {min_weight} to {max_weight}")
    print(f"Starting Dijkstra's algorithm from node {start_node}")
    
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