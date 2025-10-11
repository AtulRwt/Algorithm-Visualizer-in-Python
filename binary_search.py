import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time

class BinarySearchVisualizer:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.states = []

    def binary_search_with_states(self, arr, target):
        """Perform binary search and record states for visualization."""
        self.states = []
        left, right = 0, len(arr) - 1
        
        # Record initial state
        self.states.append({
            'array': arr.copy(),
            'left': left,
            'right': right,
            'mid': None,
            'target': target,
            'status': 'Initial array',
            'found': False
        })
        
        while left <= right:
            mid = (left + right) // 2
            
            # Record comparison state
            self.states.append({
                'array': arr.copy(),
                'left': left,
                'right': right,
                'mid': mid,
                'target': target,
                'status': f'Comparing {arr[mid]} with target {target}',
                'found': False
            })
            
            if arr[mid] == target:
                # Record found state
                self.states.append({
                    'array': arr.copy(),
                    'left': left,
                    'right': right,
                    'mid': mid,
                    'target': target,
                    'status': f'Found target {target} at index {mid}!',
                    'found': True
                })
                return mid
            
            elif arr[mid] < target:
                left = mid + 1
                status = f'{arr[mid]} < {target}, searching right half'
            else:
                right = mid - 1
                status = f'{arr[mid]} > {target}, searching left half'
            
            # Record state after updating search space
            self.states.append({
                'array': arr.copy(),
                'left': left,
                'right': right,
                'mid': mid,
                'target': target,
                'status': status,
                'found': False
            })
        
        # Record not found state
        self.states.append({
            'array': arr.copy(),
            'left': None,
            'right': None,
            'mid': None,
            'target': target,
            'status': f'Target {target} not found in array',
            'found': False
        })
        return -1

    def animate(self, interval=1000):
        """Create animation of the binary search process."""
        def update(frame):
            self.ax.clear()
            state = self.states[frame]
            arr = state['array']
            n = len(arr)
            
            # Create bar colors (default to light blue)
            colors = ['lightblue'] * n
            
            # Color the current search space in light gray
            if state['left'] is not None and state['right'] is not None:
                for i in range(state['left'], state['right'] + 1):
                    colors[i] = 'lightgray'
            
            # Color the middle element in red
            if state['mid'] is not None:
                colors[state['mid']] = 'red'
            
            # If target is found, color it green
            if state['found'] and state['mid'] is not None:
                colors[state['mid']] = 'lightgreen'
            
            # Create bars
            bars = self.ax.bar(range(n), arr, color=colors)
            
            # Add value labels on top of each bar
            for i, v in enumerate(arr):
                self.ax.text(i, v, str(v), ha='center', va='bottom')
            
            # Customize the plot
            self.ax.set_title(f'Binary Search Visualization\nStep {frame + 1}/{len(self.states)}\n{state["status"]}')
            self.ax.set_xlabel('Index')
            self.ax.set_ylabel('Value')
            
            # Add a legend
            from matplotlib.patches import Patch
            legend_elements = [
                Patch(facecolor='lightblue', label='Unexamined'),
                Patch(facecolor='lightgray', label='Current Search Space'),
                Patch(facecolor='red', label='Middle Element'),
                Patch(facecolor='lightgreen', label='Target Found')
            ]
            self.ax.legend(handles=legend_elements, loc='upper right')
            
            # Ensure the y-axis starts from 0
            self.ax.set_ylim(0, max(arr) * 1.2)

        anim = animation.FuncAnimation(self.fig, update, frames=len(self.states),
                                     interval=interval, repeat=False)
        plt.show()

def generate_sorted_array(n=20, min_val=1, max_val=100):
    """Generate a sorted array of n unique random numbers."""
    arr = np.random.choice(range(min_val, max_val + 1), size=n, replace=False)
    return np.sort(arr)

def get_user_input():
    print("\nBinary Search Visualizer")
    print("=======================")
    
    # Get array size
    while True:
        try:
            n = int(input("\nEnter array size (default 20): ") or "20")
            min_val = int(input("Enter minimum value (default 1): ") or "1")
            max_val = int(input("Enter maximum value (default 100): ") or "100")
            if n > 0 and min_val < max_val:
                break
            print("Invalid values! Array size must be positive and min_val must be less than max_val.")
        except ValueError:
            print("Please enter valid numbers!")
    
    # Generate sorted array
    arr = generate_sorted_array(n, min_val, max_val)
    print("\nGenerated sorted array:", arr)
    
    # Get target value
    while True:
        try:
            target = int(input("\nEnter target value to search for: "))
            break
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
    
    return arr, target, interval

def main():
    # Get user input
    arr, target, interval = get_user_input()
    
    # Create visualizer and run binary search
    visualizer = BinarySearchVisualizer()
    result = visualizer.binary_search_with_states(arr, target)
    
    # Display the animation
    print(f"\nStarting binary search for {target}...")
    if result != -1:
        print(f"Target {target} found at index {result}")
    else:
        print(f"Target {target} not found in array")
    
    visualizer.animate(interval)

if __name__ == "__main__":
    main()