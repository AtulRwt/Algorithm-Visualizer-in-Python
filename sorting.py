import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import argparse
import sys
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

def merge_sort_visual(arr, states):
    """Merge sort with states for comparisons, copies, and merges."""
    def _merge(arr, temp, left, mid, right, states):
        i, j, k = left, mid + 1, left
        while i <= mid and j <= right:
            states.append((list(arr), 'compare', i, j))
            if arr[i] <= arr[j]:
                temp[k] = arr[i]
                i += 1
            else:
                temp[k] = arr[j]
                j += 1
            k += 1
        while i <= mid:
            temp[k] = arr[i]
            states.append((list(arr), 'copy', k, i))
            i += 1
            k += 1
        while j <= right:
            temp[k] = arr[j]
            states.append((list(arr), 'copy', k, j))
            j += 1
            k += 1
        for p in range(left, right + 1):
            arr[p] = temp[p]
            states.append((list(arr), 'copy_back', p, -1))
        states.append((list(arr), 'merged', left, right))

    def _merge_sort(arr, temp, left, right, states):
        if left < right:
            mid = (left + right) // 2
            _merge_sort(arr, temp, left, mid, states)
            _merge_sort(arr, temp, mid + 1, right, states)
            _merge(arr, temp, left, mid, right, states)

    temp = [0] * len(arr)
    _merge_sort(arr, temp, 0, len(arr) - 1, states)

def radix_sort_visual(arr, states):
    """LSD radix sort for non-negative integers with visualization states."""
    if not arr:
        return
    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        buckets = [[] for _ in range(10)]
        n = len(arr)
        for k in range(n):
            states.append((list(arr), 'digit', k, -1))
        for val in arr:
            index = (val // exp) % 10
            buckets[index].append(val)
        arr[:] = [val for buck in buckets for val in buck]
        states.append((list(arr), 'pass_complete', -1, -1))
        exp *= 10

# Map algorithm names to their functions
algo_functions = {
    'bubble': lambda arr, states: bubble_sort_visual(arr, states),
    'quick': lambda arr, states: quick_sort_visual(arr, 0, len(arr) - 1, states),
    'merge': lambda arr, states: merge_sort_visual(arr, states),
    'radix': lambda arr, states: radix_sort_visual(arr, states),
}

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Generate random numbers and visualize sorting algorithms.")
    parser.add_argument('--mode', choices=['random', 'file'], required=True, help="Input mode: 'random' or 'file'")
    parser.add_argument('--algo', choices=['bubble', 'quick', 'merge', 'radix'], action='append', required=True, help="Sorting algorithm(s) to visualize (e.g., --algo bubble --algo quick)")
    parser.add_argument('--n', type=int, help="Number of elements for random mode")
    parser.add_argument('--min_val', type=int, default=0, help="Min value for random numbers (default: 0)")
    parser.add_argument('--max_val', type=int, default=100, help="Max value for random numbers (default: 100)")
    parser.add_argument('--file', type=str, default="numbers.txt", help="File path for input/output (default: numbers.txt)")
    parser.add_argument('--interval', type=int, default=50, help="Animation frame interval in ms (default: 50)")
    args = parser.parse_args()

    # Load or generate the array
    if args.mode == 'random':
        if args.n is None:
            print("Error: --n is required for random mode.")
            sys.exit(1)
        arr = generate_numbers(args.n, args.min_val, args.max_val, args.file)
    elif args.mode == 'file':
        if args.file is None:
            print("Error: --file is required for file mode.")
            sys.exit(1)
        try:
            with open(args.file, 'r') as f:
                arr = [int(line.strip()) for line in f if line.strip()]
            print("Input array from file:", arr)
        except Exception as e:
            print(f"Error reading file: {e}")
            sys.exit(1)

    # Set up for visualization
    valid_algos, states_list, bars_list, times_list, algo_names = [], [], [], [], []
    num_algos = len(args.algo)
    rows = math.ceil(math.sqrt(num_algos))
    cols = math.ceil(num_algos / rows)
    fig, axs = plt.subplots(rows, cols, figsize=(6 * cols, 5 * rows), squeeze=False)
    axs = axs.flatten()
    max_height = max(arr) * 1.1 if arr else 100

    # Process each algorithm
    subplot_index = 0
    for algo in args.algo:
        arr_copy = list(arr)
        states = []
        start_time = time.time()

        if algo == 'radix' and any(x < 0 for x in arr_copy):
            print(f"Warning: Radix sort assumes non-negative integers. Skipping {algo}.")
            continue

        algo_functions[algo](arr_copy, states)
        end_time = time.time()

        if not states:
            print(f"No elements to sort for {algo}.")
            continue

        valid_algos.append(algo)
        states_list.append(states)
        times_list.append(end_time - start_time)
        algo_names.append(algo.capitalize())
        
        print(f"{algo.capitalize()} steps: {len(states)}, Time: {times_list[-1]*1000:.2f}ms")

        ax = axs[subplot_index]
        ax.set_title(f"{algo.capitalize()} Sort\nTime: {times_list[-1]*1000:.2f}ms")
        ax.set_ylim(0, max_height)
        ax.set_xlim(-0.5, len(arr) - 0.5)
        bars = ax.bar(range(len(arr)), states[0][0], color='lightblue', edgecolor='black', linewidth=0.5)
        bars_list.append(bars)
        subplot_index += 1

    # Hide unused subplots
    for k in range(subplot_index, len(axs)):
        axs[k].axis('off')

    if not states_list:
        print("No valid algorithms to visualize.")
        sys.exit(0)

    # Normalize states to max frames
    max_frames = max(len(states) for states in states_list)
    for i, states in enumerate(states_list):
        if len(states) < max_frames:
            final_state = states[-1]
            final_state_extended = (final_state[0], 'complete', -1, -1)
            states_list[i].extend([final_state_extended] * (max_frames - len(states)))

    print(f"Max frames: {max_frames}")
    animation_duration_ms = max_frames * args.interval
    print(f"Animation duration: ~{animation_duration_ms/1000:.1f}s ({animation_duration_ms:.0f}ms)" if animation_duration_ms >= 1000 else f"Animation duration: ~{animation_duration_ms:.0f}ms")

    def update(frame):
        """Update all subplots for each frame based on their states."""
        for i in range(len(states_list)):
            states = states_list[i]
            bars = bars_list[i]
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
                for k, bar in enumerate(bars):
                    if k < len(state):
                        bar.set_height(state[k])
                        bar.set_color(colors[k])

    # Create animation
    ani = animation.FuncAnimation(fig, update, frames=max_frames, interval=args.interval, repeat=False, blit=False)
    plt.tight_layout()

    # Print performance comparison
    print("\n" + "="*50)
    print("PERFORMANCE COMPARISON:")
    print("="*50)
    algo_time_pairs = sorted(zip(algo_names, times_list), key=lambda x: x[1])
    for rank, (name, time_taken) in enumerate(algo_time_pairs, 1):
        print(f"{rank}. {name} Sort: {time_taken*1000:.2f} ms")
    print(f"\nFastest: {algo_time_pairs[0][0]} Sort ({algo_time_pairs[0][1]*1000:.2f} ms)")
    print(f"Slowest: {algo_time_pairs[-1][0]} Sort ({algo_time_pairs[-1][1]*1000:.2f} ms)")
    print("="*50)

    plt.show()

if __name__ == "__main__":
    main()