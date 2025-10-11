import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import time
from collections import deque

class GraphVisualizer:
    def __init__(self):
        self.G = nx.Graph()
        self.pos = None
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.states = []
        
    def generate_random_graph(self, n_nodes=10, n_edges=15):
        """Generate a random connected graph."""
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
            self.G.add_edges_from(edges)
            
            if nx.is_connected(self.G):
                break
        
        self.pos = nx.spring_layout(self.G)
        return self.G

    def bfs_with_states(self, start_node):
        """Perform BFS and record states for visualization."""
        self.states = []
        visited = set()
        queue = deque([start_node])
        visited.add(start_node)
        
        # Record initial state
        self.states.append({
            'visited': set(),
            'current': start_node,
            'queue': list(queue),
            'edges_in_path': []
        })
        
        edges_in_path = []
        
        while queue:
            current = queue.popleft()
            
            # Record state at start of processing this node
            self.states.append({
                'visited': visited.copy(),
                'current': current,
                'queue': list(queue),
                'edges_in_path': edges_in_path.copy()
            })
            
            for neighbor in self.G.neighbors(current):
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)
                    edges_in_path.append((current, neighbor))
                    
                    # Record state after adding each neighbor
                    self.states.append({
                        'visited': visited.copy(),
                        'current': neighbor,
                        'queue': list(queue),
                        'edges_in_path': edges_in_path.copy()
                    })
        
        return self.states

    def dfs_with_states(self, start_node):
        """Perform DFS and record states for visualization."""
        self.states = []
        visited = set()
        stack = [start_node]
        
        # Record initial state
        self.states.append({
            'visited': set(),
            'current': start_node,
            'stack': list(stack),
            'edges_in_path': []
        })
        
        edges_in_path = []
        
        while stack:
            current = stack.pop()
            
            if current not in visited:
                visited.add(current)
                
                # Record state at start of processing this node
                self.states.append({
                    'visited': visited.copy(),
                    'current': current,
                    'stack': list(stack),
                    'edges_in_path': edges_in_path.copy()
                })
                
                # Add neighbors in reverse order to process them in the correct order
                neighbors = list(self.G.neighbors(current))
                for neighbor in reversed(neighbors):
                    if neighbor not in visited:
                        stack.append(neighbor)
                        edges_in_path.append((current, neighbor))
                        
                        # Record state after adding each neighbor
                        self.states.append({
                            'visited': visited.copy(),
                            'current': neighbor,
                            'stack': list(stack),
                            'edges_in_path': edges_in_path.copy()
                        })
        
        return self.states

    def animate(self, algorithm='bfs', start_node=0, interval=1000):
        """Create animation of the graph traversal."""
        if algorithm.lower() == 'bfs':
            states = self.bfs_with_states(start_node)
            title = 'Breadth-First Search Visualization'
        else:
            states = self.dfs_with_states(start_node)
            title = 'Depth-First Search Visualization'
            
        def update(frame):
            self.ax.clear()
            state = states[frame]
            
            # Draw the graph structure (all edges in light gray)
            nx.draw_networkx_edges(self.G, self.pos, edge_color='lightgray', ax=self.ax)
            
            # Draw visited edges in the path
            edge_list = state['edges_in_path']
            if edge_list:
                nx.draw_networkx_edges(self.G, self.pos, edgelist=edge_list, 
                                     edge_color='g', width=2, ax=self.ax)
            
            # Draw all nodes in light blue
            nx.draw_networkx_nodes(self.G, self.pos, node_color='lightblue', 
                                 node_size=500, ax=self.ax)
            
            # Draw visited nodes in green
            visited_nodes = list(state['visited'])
            if visited_nodes:
                nx.draw_networkx_nodes(self.G, self.pos, nodelist=visited_nodes,
                                     node_color='lightgreen', node_size=500, ax=self.ax)
            
            # Draw current node in red
            if state['current'] is not None:
                nx.draw_networkx_nodes(self.G, self.pos, nodelist=[state['current']],
                                     node_color='red', node_size=500, ax=self.ax)
            
            # Draw queue/stack nodes in yellow
            queue_or_stack = state['queue'] if algorithm.lower() == 'bfs' else state['stack']
            if queue_or_stack:
                nx.draw_networkx_nodes(self.G, self.pos, nodelist=queue_or_stack,
                                     node_color='yellow', node_size=500, ax=self.ax)
            
            # Add labels to all nodes
            nx.draw_networkx_labels(self.G, self.pos)
            
            # Update title with traversal information
            status_text = f"Current Node: {state['current']}\n"
            status_text += f"{'Queue' if algorithm.lower() == 'bfs' else 'Stack'}: {queue_or_stack}\n"
            status_text += f"Visited: {sorted(list(state['visited']))}"
            
            self.ax.set_title(f"{title}\n{status_text}")
            self.ax.axis('off')
        
        anim = animation.FuncAnimation(self.fig, update, frames=len(states),
                                     interval=interval, repeat=False)
        plt.show()

def get_user_input():
    print("\nGraph Traversal Visualizer")
    print("=========================")
    
    # Get algorithm choice
    while True:
        print("\nChoose traversal algorithm:")
        print("1. Breadth-First Search (BFS)")
        print("2. Depth-First Search (DFS)")
        algo_choice = input("Enter (1/2): ").strip()
        if algo_choice in ['1', '2']:
            algorithm = 'bfs' if algo_choice == '1' else 'dfs'
            break
        print("Invalid choice! Please enter 1 or 2.")
    
    # Get graph parameters
    while True:
        try:
            n_nodes = int(input("\nEnter number of nodes (default 10): ") or "10")
            n_edges = int(input("Enter number of edges (default 15): ") or "15")
            if n_nodes > 0 and n_edges >= n_nodes - 1:  # Minimum edges for connected graph
                break
            print("Invalid values! Number of edges must be at least (nodes - 1) for a connected graph.")
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
    
    return algorithm, n_nodes, n_edges, start_node, interval

def main():
    # Get user input
    algorithm, n_nodes, n_edges, start_node, interval = get_user_input()
    
    # Create and set up the graph visualizer
    visualizer = GraphVisualizer()
    G = visualizer.generate_random_graph(n_nodes, n_edges)
    
    print(f"\nGenerated a random connected graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    print(f"Starting {algorithm.upper()} traversal from node {start_node}")
    
    # Run the visualization
    visualizer.animate(algorithm, start_node, interval)

if __name__ == "__main__":
    main()