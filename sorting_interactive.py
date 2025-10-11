import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import time
import math

def generate_numbers(n, min_val, max_val, output_file):
    """Generate n random integers and save to output_file (one per line)."""
    numbers = [random.randint(min_val, max_val) for _ in range(n)]
    with open(output_file, 'w') as f:
        for num in numbers:
            f.write(f"{num}\n")
    print(f"Generated {n} numbers between {min_val} and {max_val}, saved to {output_file}")
    print("Generated numbers:", numbers)
    return numbers

def bubble_sort_visual(arr, states):
    """Bubble sort with states for visualization (comparisons and swaps)."""
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - i - 1):
            states.append((list(arr), 'compare', j, j + 1))
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                states.append((list(arr), 'swap', j, j + 1))

def insertion_sort_visual(arr, states):
    """Insertion sort with states for visualization."""
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        states.append((list(arr), 'compare', i, j))
        
        while j >= 0 and arr[j] > key:
            states.append((list(arr), 'compare', j, j + 1))
            arr[j + 1] = arr[j]
            states.append((list(arr), 'swap', j, j + 1))
            j -= 1
        
        arr[j + 1] = key
        if j + 1 != i:
            states.append((list(arr), 'swap', j + 1, i))

def selection_sort_visual(arr, states):
    """Selection sort with states for visualization."""
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            states.append((list(arr), 'compare', j, min_idx))
            if arr[j] < arr[min_idx]:
                min_idx = j
        
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            states.append((list(arr), 'swap', i, min_idx))

def heapify_visual(arr, n, i, states):
    """Heapify function for heap sort with visualization states."""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n:
        states.append((list(arr), 'compare', left, largest))
        if arr[left] > arr[largest]:
            largest = left

    if right < n:
        states.append((list(arr), 'compare', right, largest))
        if arr[right] > arr[largest]:
            largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        states.append((list(arr), 'swap', i, largest))
        heapify_visual(arr, n, largest, states)

def heap_sort_visual(arr, states):
    """Heap sort with states for visualization."""
    n = len(arr)

    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify_visual(arr, n, i, states)

    # Extract elements from heap one by one
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        states.append((list(arr), 'swap', 0, i))
        heapify_visual(arr, i, 0, states)

def partition_visual(arr, low, high, states):
    """Partition for quicksort, tracking pivot, comparisons, and swaps."""
    pivot = arr[high]
    states.append((list(arr), 'pivot', high, -1))
    i = low - 1
    for j in range(low, high):
        states.append((list(arr), 'compare', j, high))
        if arr[j] <= pivot:
            i += 1
            if i != j:
                arr[i], arr[j] = arr[j], arr[i]
                states.append((list(arr), 'swap', i, j))
    if i + 1 != high:
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        states.append((list(arr), 'swap', i + 1, high))
    return i + 1

def quick_sort_visual(arr, low, high, states):
    """Recursive quicksort with visualization states."""
    if low < high:
        pi = partition_visual(arr, low, high, states)
        quick_sort_visual(arr, low, pi - 1, states)
        quick_sort_visual(arr, pi + 1, high, states)

def merge_visual(arr, left, mid, right, states):
    """Merge function for mergesort with visualization states."""
    left_half = arr[left:mid + 1]
    right_half = arr[mid + 1:right + 1]
    i = j = 0
    k = left
    while i < len(left_half) and j < len(right_half):
        states.append((list(arr), 'compare', left + i, mid + 1 + j))
        if left_half[i] <= right_half[j]:
            arr[k] = left_half[i]
            states.append((list(arr), 'copy', k, left + i))
            i += 1
        else:
            arr[k] = right_half[j]
            states.append((list(arr), 'copy', k, mid + 1 + j))
            j += 1
        k += 1

    while i < len(left_half):
        arr[k] = left_half[i]
        states.append((list(arr), 'copy', k, left + i))
        i += 1
        k += 1

    while j < len(right_half):
        arr[k] = right_half[j]
        states.append((list(arr), 'copy', k, mid + 1 + j))
        j += 1
        k += 1

    states.append((list(arr), 'merged', left, right))

def merge_sort_visual(arr, left, right, states):
    """Recursive mergesort with visualization states."""
    if left < right:
        mid = (left + right) // 2
        merge_sort_visual(arr, left, mid, states)
        merge_sort_visual(arr, mid + 1, right, states)
        merge_visual(arr, left, mid, right, states)

def counting_sort_for_radix(arr, exp, states):
    """Counting sort for a specific digit (used by radix sort)."""
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for i in range(n):
        idx = arr[i] // exp
        digit = idx % 10
        count[digit] += 1
        states.append((list(arr), 'digit', i, -1))

    for i in range(1, 10):
        count[i] += count[i - 1]

    i = n - 1
    while i >= 0:
        idx = arr[i] // exp
        digit = idx % 10
        output[count[digit] - 1] = arr[i]
        count[digit] -= 1
        states.append((list(arr), 'copy', i, count[digit]))
        i -= 1

    for i in range(n):
        arr[i] = output[i]
        states.append((list(arr), 'copy_back', i, -1))

def radix_sort_visual(arr, states):
    """Radix sort with visualization states."""
    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        counting_sort_for_radix(arr, exp, states)
        states.append((list(arr), 'pass_complete', -1, -1))
        exp *= 10

def get_user_input():
    print("\nSorting Algorithm Visualizer")
    print("==========================")
    
    # Get mode
    while True:
        mode = input("\nChoose mode:\n1. Random numbers\n2. From file\nEnter (1/2): ").strip()
        if mode in ['1', '2']:
            mode = 'random' if mode == '1' else 'file'
            break
        print("Invalid choice! Please enter 1 or 2.")

    # Get algorithm
    print("\nChoose sorting algorithm:")
    print("1. Bubble Sort")
    print("2. Quick Sort")
    print("3. Merge Sort")
    print("4. Radix Sort")
    print("5. Insertion Sort")
    print("6. Selection Sort")
    print("7. Heap Sort")
    while True:
        algo_choice = input("Enter (1-7): ").strip()
        if algo_choice in ['1', '2', '3', '4', '5', '6', '7']:
            algo_map = {
                '1': 'bubble',
                '2': 'quick',
                '3': 'merge',
                '4': 'radix',
                '5': 'insertion',
                '6': 'selection',
                '7': 'heap'
            }
            algo = algo_map[algo_choice]
            break
        print("Invalid choice! Please enter a number between 1 and 7.")

    # Get other parameters based on mode
    if mode == 'random':
        while True:
            try:
                n = int(input("\nEnter number of elements (default 10): ") or "10")
                min_val = int(input("Enter minimum value (default 0): ") or "0")
                max_val = int(input("Enter maximum value (default 100): ") or "100")
                if n > 0 and min_val <= max_val:
                    break
                print("Invalid values! Number of elements must be positive and min_val must be <= max_val.")
            except ValueError:
                print("Please enter valid numbers!")
    else:
        file = input("\nEnter input file name (default 'numbers.txt'): ") or "numbers.txt"
        n = 10  # default value for file mode
        min_val = 0  # default value for file mode
        max_val = 100  # default value for file mode

    interval = input("\nEnter animation interval in ms (default 50): ") or "50"
    try:
        interval = int(interval)
    except ValueError:
        print("Invalid interval! Using default value of 50ms.")
        interval = 50

    # Create a namespace object to store arguments
    class Args:
        pass
    
    args = Args()
    args.mode = mode
    args.algo = algo
    args.n = n
    args.min_val = min_val
    args.max_val = max_val
    args.file = 'numbers.txt'
    args.interval = interval
    
    return args

def main():
    # Get user input
    args = get_user_input()

    # Get numbers based on mode
    if args.mode == 'random':
        numbers = generate_numbers(args.n, args.min_val, args.max_val, args.file)
    else:
        try:
            with open(args.file, 'r') as f:
                numbers = [int(line.strip()) for line in f]
            print(f"Read {len(numbers)} numbers from {args.file}")
        except (FileNotFoundError, ValueError) as e:
            print(f"Error reading file: {e}")
            return

    # Prepare for visualization
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(range(len(numbers)), numbers, color='lightblue')
    ax.set_title(f'{args.algo.capitalize()} Sort Visualization')
    ax.set_xlabel('Index')
    ax.set_ylabel('Value')

    # Create a copy of numbers for sorting
    arr = numbers.copy()
    states = []

    # Sort and time the algorithm
    start_time = time.time()
    if args.algo == 'bubble':
        bubble_sort_visual(arr, states)
    elif args.algo == 'quick':
        quick_sort_visual(arr, 0, len(arr) - 1, states)
    elif args.algo == 'merge':
        merge_sort_visual(arr, 0, len(arr) - 1, states)
    elif args.algo == 'radix':
        radix_sort_visual(arr, states)
    elif args.algo == 'insertion':
        insertion_sort_visual(arr, states)
    elif args.algo == 'selection':
        selection_sort_visual(arr, states)
    elif args.algo == 'heap':
        heap_sort_visual(arr, states)

    time_taken = time.time() - start_time
    print(f"{args.algo.capitalize()} steps: {len(states)}, Time: {time_taken*1000:.2f}ms")

    if len(states) > 0:
        final_state = states[-1]
        final_state_extended = (final_state[0], 'complete', -1, -1)
        states.extend([final_state_extended] * (10))  # Add some frames with the completed state

    def update(frame):
        if frame < len(states):
            state, action, idx1, idx2 = states[frame]
            colors = ['lightblue'] * len(state)
            if action in ['compare', 'digit']:
                if idx1 != -1:
                    colors[idx1] = 'yellow'
                if idx2 != -1 and idx2 < len(colors):
                    colors[idx2] = 'orange'
            elif action in ['swap', 'copy', 'copy_back']:
                if idx1 != -1:
                    colors[idx1] = 'red'
                if idx2 != -1 and idx2 < len(colors):
                    colors[idx2] = 'pink'
            elif action == 'pivot':
                if idx1 != -1:
                    colors[idx1] = 'green'
            elif action == 'merged':
                if idx1 != -1 and idx2 != -1:
                    for k in range(max(0, idx1), min(len(colors), idx2 + 1)):
                        colors[k] = 'lightgreen'
            elif action in ['pass_complete', 'complete']:
                colors = ['lightgreen'] * len(state)
            
            for rect, val, color in zip(bars, state, colors):
                rect.set_height(val)
                rect.set_color(color)

    # Create animation
    ani = animation.FuncAnimation(fig, update, frames=len(states),
                                interval=args.interval, repeat=False, blit=False)
    
    print(f"\nAnimation duration: ~{len(states) * args.interval/1000:.1f}s")
    plt.show()

if __name__ == "__main__":
    main()