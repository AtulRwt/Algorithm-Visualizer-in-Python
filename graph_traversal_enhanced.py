import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
from collections import deque

class GraphTraversalVisualizer:
    def __init__(self):
        self.G = nx.Graph()
        self.pos = None
        self.fig, self.ax = plt.subplots(figsize=(15, 10))
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
        
        def update(frame):
            self.fig.clear()
            state = states[frame]
            
            # Create subplots for graph and explanation
            gs = self.fig.add_gridspec(1, 2, width_ratios=[2, 1])
            ax_graph = self.fig.add_subplot(gs[0])
            ax_text = self.fig.add_subplot(gs[1])
            
            # Draw the graph
            edge_colors = ['lightgray' for _ in self.G.edges()]
            nx.draw_networkx_edges(self.G, self.pos, edge_color=edge_colors, ax=ax_graph)
            
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
            
            # Display the explanation text
            y_pos = 0.95
            for line in explanation:
                ax_text.text(0.05, y_pos, line, fontsize=10, fontfamily='monospace')
                y_pos -= 0.04
            
            ax_graph.axis('off')
        
        # Create animation
        anim = animation.FuncAnimation(self.fig, update, frames=len(states),
                                     interval=interval, repeat=False)
        plt.tight_layout()
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
            if n_nodes > 0 and n_edges >= n_nodes - 1:
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
    
    # Create and set up the visualizer
    visualizer = GraphTraversalVisualizer()
    G = visualizer.generate_random_graph(n_nodes, n_edges)
    
    print(f"\nGenerated a random connected graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    
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