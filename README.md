# Algorithm Visualizer Collection

This repository contains a collection of algorithm visualizations implemented in Python. Each visualization helps in understanding how different algorithms work through interactive animations.

## Prerequisites

Before running the visualizations, make sure you have Python installed and the following libraries:
```bash
pip install matplotlib networkx numpy
```

## Available Visualizations

### 1. Sorting Algorithms
File: `sorting_interactive.py`

Features:
- Multiple sorting algorithms
- Real-time visualization
- Customizable array size and range

Available algorithms:
- Bubble Sort
- Quick Sort
- Merge Sort
- Radix Sort
- Insertion Sort
- Selection Sort
- Heap Sort

To run:
```bash
python sorting_interactive.py
```

Follow the prompts to:
1. Choose sorting algorithm
2. Set array size
3. Define value range
4. Adjust animation speed

### 2. Graph Traversal Algorithms
File: `graph_traversal.py`

Features:
- BFS (Breadth-First Search)
- DFS (Depth-First Search)
- Interactive graph generation
- Step-by-step visualization

To run:
```bash
python graph_traversal.py
```

Follow the prompts to:
1. Choose traversal algorithm (BFS/DFS)
2. Set number of nodes and edges
3. Select start node
4. Adjust animation speed

### 3. Binary Search
File: `binary_search.py`

Features:
- Visualization of binary search process
- Works on sorted arrays
- Shows search space reduction

To run:
```bash
python binary_search.py
```

Follow the prompts to:
1. Set array size
2. Define value range
3. Enter target value to search
4. Adjust animation speed

### 4. Dijkstra's Shortest Path
File: `dijkstra.py`

Features:
- Weighted graph visualization
- Shortest path finding
- Real-time distance updates
- Path construction visualization

To run:
```bash
python dijkstra.py
```

Follow the prompts to:
1. Set number of nodes and edges
2. Define weight range
3. Choose start node
4. Adjust animation speed

## Color Codes

### Sorting Visualizer
- Light Blue: Unsorted elements
- Yellow: Elements being compared
- Red: Elements being swapped
- Light Green: Sorted elements

### Graph Traversal
- Light Blue: Unvisited nodes
- Red: Current node
- Yellow: Nodes in queue/stack
- Green: Visited nodes
- Green edges: Path taken

### Binary Search
- Light Blue: Unexamined elements
- Light Gray: Current search space
- Red: Middle element
- Green: Target found

### Dijkstra's Algorithm
- Light Blue: Unvisited nodes
- Light Green: Visited nodes
- Red: Current node
- Yellow: Node being checked
- Orange: Node with updated distance
- Green edges: Shortest paths

## Customization

Each visualization allows you to customize:
- Input size (number of elements/nodes)
- Value ranges
- Animation speed
- Starting positions (where applicable)

## Example Commands

Here are some example commands with typical parameters:

### Sorting (20 numbers, range 1-100):
```bash
python sorting_interactive.py
# Choose algorithm: 1 (Bubble Sort)
# Array size: 20
# Min value: 1
# Max value: 100
# Interval: 50
```

### Graph Traversal (10 nodes, 15 edges):
```bash
python graph_traversal.py
# Choose algorithm: 1 (BFS)
# Nodes: 10
# Edges: 15
# Start node: 0
# Interval: 1000
```

### Binary Search (20 numbers):
```bash
python binary_search.py
# Array size: 20
# Min value: 1
# Max value: 100
# Target: 50
# Interval: 1000
```

### Dijkstra (8 nodes, weights 1-10):
```bash
python dijkstra.py
# Nodes: 8
# Edges: 12
# Min weight: 1
# Max weight: 10
# Start node: 0
# Interval: 1000
```

## Notes

- All visualizations use matplotlib for rendering
- Animations can be paused/resumed using matplotlib's interactive controls
- Window can be resized for better visibility
- Close the visualization window to end the program
- Use smaller intervals (e.g., 50ms) for faster animations
- Use larger intervals (e.g., 1000ms) to better observe the steps