import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
import random
import numpy as np


class KnapsackVisualizer:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.states = []
        self.items = []
        self.capacity = 0

    def generate_items(self, n=6, wmin=1, wmax=10, vmin=1, vmax=20, capacity=None):
        self.items = [(random.randint(wmin, wmax), random.randint(vmin, vmax)) for _ in range(n)]
        if capacity is None:
            capacity = max(wmin, int(sum(w for w, _ in self.items) * 0.5))
        self.capacity = capacity
        return self.items, self.capacity

    def knapsack_with_states(self, items, capacity):
        self.states = []
        n = len(items)
        dp = [[0] * (capacity + 1) for _ in range(n + 1)]
        self.states.append({'i': 0, 'w': 0, 'dp': [row[:] for row in dp], 'status': 'Initialize table', 'sel': None})
        for i in range(1, n + 1):
            wt, val = items[i - 1]
            for w in range(capacity + 1):
                best = dp[i - 1][w]
                choice = 'exclude'
                if wt <= w and dp[i - 1][w - wt] + val > best:
                    best = dp[i - 1][w - wt] + val
                    choice = 'include'
                self.states.append({'i': i, 'w': w, 'dp': [row[:] for row in dp], 'status': f'Consider item {i-1} (w={wt}, v={val}) at cap {w}', 'sel': None, 'choice': choice})
                dp[i][w] = best
                self.states.append({'i': i, 'w': w, 'dp': [row[:] for row in dp], 'status': f'Set dp[{i}][{w}]={best} ({choice})', 'sel': None, 'choice': choice})
        sel = []
        w = capacity
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i - 1][w]:
                sel.append(i - 1)
                w -= items[i - 1][0]
        sel = list(reversed(sel))
        self.states.append({'i': None, 'w': None, 'dp': dp, 'status': f'Selected items: {sel}', 'sel': sel})
        return dp, sel

    def animate(self, interval=200):
        def update(frame):
            self.fig.clear()
            state = self.states[frame]
            dp = state['dp']
            n_rows = len(dp)
            n_cols = len(dp[0]) if dp else 0

            gs = self.fig.add_gridspec(1, 2, width_ratios=[2, 1])
            ax_tbl = self.fig.add_subplot(gs[0])
            ax_text = self.fig.add_subplot(gs[1])

            arr = np.array(dp, dtype=float)
            ax_tbl.imshow(arr, cmap='Greens')
            for i in range(n_rows):
                for j in range(n_cols):
                    color = 'black'
                    if state.get('i') == i and state.get('w') == j:
                        color = 'orange'
                    ax_tbl.text(j, i, int(dp[i][j]), ha='center', va='center', color=color)
            if state.get('sel'):
                for i in range(1, len(self.items) + 1):
                    if (i - 1) in state['sel']:
                        ax_tbl.add_patch(Rectangle((-0.5, i - 0.5), n_cols, 1, fill=False, edgecolor='red', linewidth=2))
            ax_tbl.set_xticks(range(n_cols))
            ax_tbl.set_yticks(range(n_rows))
            ax_tbl.set_xlabel('Capacity')
            ax_tbl.set_ylabel('Item index (row)')
            ax_tbl.set_title(f"0/1 Knapsack DP\nStep {frame + 1}/{len(self.states)}")
            for spine in ax_tbl.spines.values():
                spine.set_visible(False)

            ax_text.axis('off')
            lines = [
                "Status:",
                state['status'],
                "",
                f"Items (w,v): {self.items}",
                f"Capacity: {self.capacity}",
            ]
            i = state.get('i')
            w = state.get('w')
            if i is not None and w is not None and i > 0:
                wt, val = self.items[i - 1]
                excl = dp[i - 1][w]
                incl = '-' if wt > w else dp[i - 1][w - wt] + val
                lines.extend([
                    "",
                    "Transition:",
                    f"i={i}, w={w}",
                    f"Option EXCLUDE: dp[{i-1}][{w}] = {excl}",
                    f"Option INCLUDE: {('N/A (wt>'+str(w)+')' if wt > w else f'dp[{i-1}][{w-wt}] + {val} = {incl}')}",
                    f"Choice: {state.get('choice','-')}",
                    f"dp[{i}][{w}] = {dp[i][w]}",
                ])
            if state.get('sel') is not None:
                sel = state['sel']
                if sel:
                    total_val = dp[-1][-1]
                    total_wt = sum(self.items[idx][0] for idx in sel)
                else:
                    total_val = dp[-1][-1]
                    total_wt = 0
                lines.extend([
                    "",
                    "Final Selection:",
                    f"Indices: {sel}",
                    f"Total Weight: {total_wt}",
                    f"Total Value: {total_val}",
                ])
            y = 0.95
            for line in lines:
                ax_text.text(0.05, y, line, fontsize=10, fontfamily='monospace')
                y -= 0.05

        self.anim = animation.FuncAnimation(self.fig, update, frames=len(self.states), interval=interval, repeat=False)
        plt.tight_layout()
        plt.show()


def get_user_input():
    print("\n0/1 Knapsack Visualizer")
    print("=======================")
    while True:
        try:
            n = int(input("\nEnter number of items (default 6): ") or "6")
            wmin = int(input("Enter min item weight (default 1): ") or "1")
            wmax = int(input("Enter max item weight (default 10): ") or "10")
            vmin = int(input("Enter min item value (default 1): ") or "1")
            vmax = int(input("Enter max item value (default 20): ") or "20")
            if 1 <= n <= 15 and wmax >= wmin and vmax >= vmin:
                break
        except ValueError:
            pass
        print("Invalid values, try again.")
    cap = input("\nEnter knapsack capacity (blank for auto): ").strip()
    capacity = None
    if cap:
        try:
            capacity = int(cap)
        except ValueError:
            capacity = None
    interval = int(input("\nEnter animation interval in ms (default 200): ") or "200")
    return n, wmin, wmax, vmin, vmax, capacity, interval


def main():
    n, wmin, wmax, vmin, vmax, capacity, interval = get_user_input()
    vis = KnapsackVisualizer()
    items, cap = vis.generate_items(n=n, wmin=wmin, wmax=wmax, vmin=vmin, vmax=vmax, capacity=capacity)
    dp, sel = vis.knapsack_with_states(items, cap)
    print(f"Items (w,v): {items}\nCapacity: {cap}\nSelected item indices: {sel}")
    vis.animate(interval)


if __name__ == "__main__":
    main()
