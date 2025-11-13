import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
from collections import deque
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')

class GraphTraversalVisualizer:
    def __init__(self):
        self.G = nx.Graph()
        self.pos = None
        self.states = []
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Graph Traversal Visualization")
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create matplotlib figure
        self.fig = plt.figure(figsize=(15, 10))
        
        # Embed matplotlib figure in tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create text frame with scrollbar
        self.text_frame = ttk.Frame(self.main_frame)
        self.text_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
        
        # Create scrolled text widget
        self.text_widget = tk.Text(self.text_frame, wrap=tk.WORD, width=50)
        self.scrollbar = ttk.Scrollbar(self.text_frame, orient=tk.VERTICAL, command=self.text_widget.yview)
        self.text_widget.configure(yscrollcommand=self.scrollbar.set)
        
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_user_graph(self, n_nodes):
        """Create a graph with user-input connections."""
        self.G.clear()
        print("\nEnter connections between nodes (1 for connection, 0 for no connection):")
        print("Example: For connection between nodes 0 and 1, enter '1' when prompted")
        
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
                            conn = int(input(f"Connect nodes {i}-{j}? (1/0): "))
                            if conn in [0, 1]:
                                break
                            print("Please enter 0 or 1!")
                        except ValueError:
                            print("Please enter a valid number!")
                    row.append(conn)
                else:
                    row.append(adj_matrix[j][i])  # Mirror the matrix
            adj_matrix.append(row)
            print(f"Current connections for node {i}:", row)
        
        # Create edges from adjacency matrix
        for i in range(n_nodes):
            for j in range(i + 1, n_nodes):
                if adj_matrix[i][j] == 1:
                    self.G.add_edge(i, j)
        
        if not nx.is_connected(self.G):
            print("\nWarning: The graph is not connected! Some nodes may be unreachable.")
        
        self.pos = nx.spring_layout(self.G)
        return self.G

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
            'edges_in_path': [],
            'status': 'Starting BFS from node {start_node}',
            'level': 0,
            'action': 'start'
        })
        
        edges_in_path = []
        level = 0
        nodes_in_level = {0: [start_node]}
        
        while queue:
            current = queue.popleft()
            current_level = next(level for level, nodes in nodes_in_level.items() if current in nodes)
            
            # Record state at start of processing this node
            self.states.append({
                'visited': visited.copy(),
                'current': current,
                'queue': list(queue),
                'edges_in_path': edges_in_path.copy(),
                'status': f'Processing node {current} at level {current_level}',
                'level': current_level,
                'action': 'process'
            })
            
            unvisited_neighbors = []
            for neighbor in self.G.neighbors(current):
                if neighbor not in visited:
                    unvisited_neighbors.append(neighbor)
                    
            # Record state before processing neighbors
            if unvisited_neighbors:
                self.states.append({
                    'visited': visited.copy(),
                    'current': current,
                    'queue': list(queue),
                    'edges_in_path': edges_in_path.copy(),
                    'unvisited_neighbors': unvisited_neighbors,
                    'status': f'Found unvisited neighbors: {unvisited_neighbors}',
                    'level': current_level,
                    'action': 'check_neighbors'
                })
            
            for neighbor in unvisited_neighbors:
                queue.append(neighbor)
                visited.add(neighbor)
                edges_in_path.append((current, neighbor))
                
                # Update level information
                if current_level + 1 not in nodes_in_level:
                    nodes_in_level[current_level + 1] = []
                nodes_in_level[current_level + 1].append(neighbor)
                
                # Record state after adding each neighbor
                self.states.append({
                    'visited': visited.copy(),
                    'current': current,
                    'next_node': neighbor,
                    'queue': list(queue),
                    'edges_in_path': edges_in_path.copy(),
                    'status': f'Added node {neighbor} to queue (Level {current_level + 1})',
                    'level': current_level,
                    'action': 'add_neighbor'
                })
        
        # Record final state
        self.states.append({
            'visited': visited,
            'current': None,
            'queue': [],
            'edges_in_path': edges_in_path,
            'status': 'BFS completed!',
            'level': max(nodes_in_level.keys()),
            'action': 'complete',
            'level_info': nodes_in_level
        })
        
        return self.states

    def dfs_with_states(self, start_node):
        """Perform DFS and record states for visualization."""
        self.states = []
        visited = set()
        stack = [start_node]
        path = []  # Track the current path
        
        # Record initial state
        self.states.append({
            'visited': set(),
            'current': start_node,
            'stack': list(stack),
            'edges_in_path': [],
            'status': f'Starting DFS from node {start_node}',
            'path': [],
            'action': 'start',
            'depth': 0
        })
        
        edges_in_path = []
        max_depth = 0
        current_depth = {start_node: 0}
        
        while stack:
            current = stack[-1]  # Peek at the top of the stack
            
            if current not in visited:
                visited.add(current)
                path.append(current)
                depth = len(path) - 1
                current_depth[current] = depth
                max_depth = max(max_depth, depth)
                
                # Record state when visiting a new node
                self.states.append({
                    'visited': visited.copy(),
                    'current': current,
                    'stack': list(stack),
                    'edges_in_path': edges_in_path.copy(),
                    'status': f'Visiting node {current} at depth {depth}',
                    'path': path.copy(),
                    'action': 'visit',
                    'depth': depth
                })
                
                # Find unvisited neighbors
                neighbors = list(self.G.neighbors(current))
                unvisited_neighbors = [n for n in neighbors if n not in visited]
                
                if unvisited_neighbors:
                    # Record state before processing neighbors
                    self.states.append({
                        'visited': visited.copy(),
                        'current': current,
                        'stack': list(stack),
                        'edges_in_path': edges_in_path.copy(),
                        'unvisited_neighbors': unvisited_neighbors,
                        'status': f'Found unvisited neighbors: {unvisited_neighbors}',
                        'path': path.copy(),
                        'action': 'check_neighbors',
                        'depth': depth
                    })
                    
                    # Add neighbors to stack in reverse order
                    for neighbor in reversed(unvisited_neighbors):
                        stack.append(neighbor)
                        edges_in_path.append((current, neighbor))
                        
                        # Record state after adding each neighbor
                        self.states.append({
                            'visited': visited.copy(),
                            'current': current,
                            'next_node': neighbor,
                            'stack': list(stack),
                            'edges_in_path': edges_in_path.copy(),
                            'status': f'Added node {neighbor} to stack',
                            'path': path.copy(),
                            'action': 'add_neighbor',
                            'depth': depth
                        })
                else:
                    # Dead end - record backtracking state
                    self.states.append({
                        'visited': visited.copy(),
                        'current': current,
                        'stack': list(stack),
                        'edges_in_path': edges_in_path.copy(),
                        'status': f'Dead end at node {current}, will backtrack',
                        'path': path.copy(),
                        'action': 'backtrack',
                        'depth': depth
                    })
            
            stack.pop()
            if path and path[-1] == current:
                path.pop()
        
        # Record final state
        self.states.append({
            'visited': visited,
            'current': None,
            'stack': [],
            'edges_in_path': edges_in_path,
            'status': 'DFS completed!',
            'path': [],
            'action': 'complete',
            'depth': 0,
            'max_depth': max_depth,
            'depth_info': current_depth
        })
        
        return self.states

    def animate(self, algorithm='bfs', start_node=0, interval=1000):
        """Create animation of the graph traversal."""
        if algorithm.lower() == 'bfs':
            states = self.bfs_with_states(start_node)
            title = 'Breadth-First Search (BFS)'
            data_structure = 'Queue'
        else:
            states = self.dfs_with_states(start_node)
            title = 'Depth-First Search (DFS)'
            data_structure = 'Stack'
            
        # Set window title
        self.root.title(f"Graph Traversal Visualization - {title}")
        
        # Configure the text widget
        self.text_widget.config(font=('Courier', 10))
        
        def update(frame):
            self.fig.clear()
            state = states[frame]
            
            # Create subplots for graph, matrix and explanation
            gs = self.fig.add_gridspec(2, 2, height_ratios=[2, 1], width_ratios=[2, 1])
            ax_graph = self.fig.add_subplot(gs[0, 0])  # Graph in top-left
            ax_text = self.fig.add_subplot(gs[:, 1])   # Text spans right side
            ax_matrix = self.fig.add_subplot(gs[1, 0]) # Matrix in bottom-left
            
            # Draw the graph
            edge_colors = ['lightgray' for _ in self.G.edges()]
            nx.draw_networkx_edges(self.G, self.pos, edge_color=edge_colors, ax=ax_graph)
            
            # Draw adjacency matrix
            ax_matrix.clear()
            ax_matrix.set_title("Adjacency Matrix")
            n_nodes = len(list(self.G.nodes()))  # Get actual nodes
            nodes_list = sorted(list(self.G.nodes()))  # Get sorted list of nodes
            node_to_index = {node: i for i, node in enumerate(nodes_list)}  # Map nodes to indices
            
            # Create matrix with correct dimensions
            matrix = [[0 for _ in range(n_nodes)] for _ in range(n_nodes)]
            
            # Fill matrix using node mapping
            for edge in self.G.edges():
                i, j = edge
                idx1, idx2 = node_to_index[i], node_to_index[j]
                matrix[idx1][idx2] = 1
                matrix[idx2][idx1] = 1  # Undirected graph
            
            # Plot matrix
            im = ax_matrix.imshow(matrix, cmap='Blues')
            
            # Add matrix labels
            for i in range(n_nodes):
                for j in range(n_nodes):
                    text = ax_matrix.text(j, i, matrix[i][j],
                                        ha="center", va="center",
                                        color="black" if matrix[i][j] == 0 else "white")
            
            # Add row and column labels
            ax_matrix.set_xticks(range(n_nodes))
            ax_matrix.set_yticks(range(n_nodes))
            ax_matrix.set_xticklabels(nodes_list)
            ax_matrix.set_yticklabels(nodes_list)
            ax_matrix.set_xlabel("To Node")
            ax_matrix.set_ylabel("From Node")
            
            # Draw path edges in green
            if state['edges_in_path']:
                nx.draw_networkx_edges(self.G, self.pos, edgelist=state['edges_in_path'],
                                     edge_color='g', width=2, ax=ax_graph)
            
            # Draw nodes with different colors based on their state
            node_colors = ['lightblue' for _ in self.G.nodes()]  # Default color
            
            # Color visited nodes
            for node in state['visited']:
                node_colors[node] = 'lightgreen'
            
            # Color current node
            if state.get('current') is not None:
                node_colors[state['current']] = 'red'
            
            # Color next node to be visited
            if state.get('next_node') is not None:
                node_colors[state['next_node']] = 'yellow'
            
            # Draw all nodes
            nx.draw_networkx_nodes(self.G, self.pos, node_color=node_colors,
                                 node_size=500, ax=ax_graph)
            
            # Add node labels
            nx.draw_networkx_labels(self.G, self.pos, ax=ax_graph)
            
            # Set title
            ax_graph.set_title(f"{title} Visualization\nStep {frame + 1}/{len(states)}")
            
            # Add legend
            from matplotlib.patches import Patch
            legend_elements = [
                Patch(facecolor='lightblue', label='Undiscovered'),
                Patch(facecolor='lightgreen', label='Visited'),
                Patch(facecolor='red', label='Current Node'),
                Patch(facecolor='yellow', label='Next Node'),
                Patch(facecolor='green', label='Path Taken')
            ]
            ax_graph.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5))
            
            # Prepare detailed explanation text
            ax_text.axis('off')
            explanation = [
                f"{title} - Step Explanation",
                "=" * 30,
                "",
                "Current Status:",
                "-" * 15,
                state['status'],
                "",
                "Progress:",
                "-" * 15,
                f"Visited: {sorted(list(state['visited']))}",
                f"Remaining: {sorted(list(set(self.G.nodes()) - state['visited']))}",
                "",
                f"{data_structure} Contents:",
                "-" * 15
            ]
            
            # Add data structure-specific information
            if algorithm.lower() == 'bfs':
                queue = state.get('queue', [])
                if queue:
                    explanation.append("Front -> " + " -> ".join(map(str, queue)) + " <- Back")
                    explanation.append("(FIFO: First In, First Out)")
                else:
                    explanation.append("(Empty)")
                
                # Add level information if available
                if state.get('level') is not None:
                    explanation.extend([
                        "",
                        "Level Information:",
                        "-" * 15,
                        f"Current Level: {state['level']}"
                    ])
                    if state.get('level_info'):
                        for level, nodes in state['level_info'].items():
                            explanation.append(f"Level {level}: {nodes}")
            else:
                stack = state.get('stack', [])
                if stack:
                    explanation.append("Top -> " + " -> ".join(map(str, stack)) + " <- Bottom")
                    explanation.append("(LIFO: Last In, First Out)")
                else:
                    explanation.append("(Empty)")
                
                # Add depth information
                if state.get('depth') is not None:
                    explanation.extend([
                        "",
                        "Depth Information:",
                        "-" * 15,
                        f"Current Depth: {state['depth']}"
                    ])
                    if state.get('path'):
                        explanation.append(f"Current Path: {' -> '.join(map(str, state['path']))}")
            
            # Add algorithm-specific explanation
            explanation.extend([
                "",
                "Algorithm Details:",
                "-" * 15
            ])
            
            if algorithm.lower() == 'bfs':
                explanation.extend([
                    "- Explores nodes level by level",
                    "- Guarantees shortest path in unweighted graph",
                    "- Uses Queue (FIFO) for next nodes",
                    "- Complete level must be explored",
                    "  before moving to next level"
                ])
            else:
                explanation.extend([
                    "- Explores as deeply as possible",
                    "- Good for maze-solving problems",
                    "- Uses Stack (LIFO) for next nodes",
                    "- Backtracking occurs when no",
                    "  unvisited neighbors remain"
                ])
            
            # Update the text widget
            self.text_widget.delete(1.0, tk.END)
            for line in explanation:
                self.text_widget.insert(tk.END, line + '\n')
            self.text_widget.see(1.0)  # Scroll to top
            
            ax_graph.axis('off')
        
        # Create animation
        anim = animation.FuncAnimation(self.fig, update, frames=len(states),
                                     interval=interval, repeat=False)
        plt.tight_layout()
        
        # Start the tkinter main loop
        self.root.mainloop()

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
    
    # Get graph creation mode
    while True:
        print("\nChoose graph creation mode:")
        print("1. Random graph")
        print("2. Create your own graph")
        mode_choice = input("Enter (1/2): ").strip()
        if mode_choice in ['1', '2']:
            mode = 'random' if mode_choice == '1' else 'user'
            break
        print("Invalid choice! Please enter 1 or 2.")
    
    # Get graph parameters
    while True:
        try:
            if mode == 'random':
                n_nodes = int(input("\nEnter number of nodes (default 10): ") or "10")
                n_edges = int(input("Enter number of edges (default 15): ") or "15")
                if n_nodes > 0 and n_edges >= n_nodes - 1:
                    break
                print("Invalid values! Number of edges must be at least (nodes - 1) for a connected graph.")
            else:
                n_nodes = int(input("\nEnter number of nodes (2-10): "))
                if 2 <= n_nodes <= 10:
                    n_edges = None  # Not needed for user input mode
                    break
                print("Please enter a number between 2 and 10.")
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
    
    return algorithm, mode, n_nodes, n_edges, start_node, interval

def main():
    # Get user input
    algorithm, mode, n_nodes, n_edges, start_node, interval = get_user_input()
    
    # Create and set up the visualizer
    visualizer = GraphTraversalVisualizer()
    
    if mode == 'random':
        G = visualizer.generate_random_graph(n_nodes, n_edges)
        print(f"\nGenerated a random connected graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    else:
        print("\nNow you'll create your own graph structure.")
        print("Enter 1 if two nodes should be connected, 0 if not.")
        G = visualizer.create_user_graph(n_nodes)
        print(f"\nCreated graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    
    if algorithm.lower() == 'bfs':
        print("\nBFS Characteristics:")
        print("- Explores nodes level by level")
        print("- Guarantees shortest path in unweighted graphs")
        print("- Uses a Queue (First In, First Out)")
    else:
        print("\nDFS Characteristics:")
        print("- Explores as deeply as possible before backtracking")
        print("- Good for maze solving and topological sorting")
        print("- Uses a Stack (Last In, First Out)")
    
    print(f"\nStarting {algorithm.upper()} traversal from node {start_node}")
    
    # Run the visualization
    visualizer.animate(algorithm, start_node, interval)

if __name__ == "__main__":
    main()