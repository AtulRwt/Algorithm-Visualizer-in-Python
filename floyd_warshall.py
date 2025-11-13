import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
import numpy as np
import random


class FloydWarshallVisualizer:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.states = []
        self.n = 0

    def generate_graph_matrix(self, n=6, density=0.5, min_w=1, max_w=9, directed=True):
        self.n = n
        inf = float('inf')
        dist = [[inf] * n for _ in range(n)]
        for i in range(n):
            dist[i][i] = 0
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                if random.random() < density:
                    w = random.randint(min_w, max_w)
                    dist[i][j] = w
                    if not directed:
                        dist[j][i] = w
        return dist

    def floyd_warshall_with_states(self, dist):
        self.states = []
        n = len(dist)
        D = [row[:] for row in dist]
        self.states.append({'k': -1, 'i': None, 'j': None, 'D': [row[:] for row in D], 'status': 'Initialize distance matrix'})
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    old = D[i][j]
                    alt = (D[i][k] + D[k][j]) if (D[i][k] != float('inf') and D[k][j] != float('inf')) else float('inf')
                    self.states.append({'k': k, 'i': i, 'j': j, 'D': [row[:] for row in D], 'status': f'Check via k={k}: d[{i},{j}] vs d[{i},{k}]+d[{k},{j}]'})
                    if alt < old:
                        D[i][j] = alt
                        self.states.append({'k': k, 'i': i, 'j': j, 'D': [row[:] for row in D], 'status': f'Update d[{i},{j}] = {alt}'})
        self.states.append({'k': n, 'i': None, 'j': None, 'D': [row[:] for row in D], 'status': 'All-pairs shortest paths computed'})
        return D

    def animate(self, interval=500):
        def update(frame):
            self.fig.clear()
            state = self.states[frame]
            D = state['D']
            n = len(D)
            gs = self.fig.add_gridspec(1, 2, width_ratios=[2, 1])
            ax_mat = self.fig.add_subplot(gs[0])
            ax_text = self.fig.add_subplot(gs[1])
            arr = np.array([[np.inf if D[i][j] == float('inf') else D[i][j] for j in range(n)] for i in range(n)], dtype=float)
            ax_mat.imshow(arr, cmap='Blues')
            for i in range(n):
                for j in range(n):
                    val = '∞' if D[i][j] == float('inf') else int(D[i][j])
                    color = 'black'
                    if state['i'] == i and state['j'] == j:
                        color = 'orange'
                    ax_mat.text(j, i, val, ha='center', va='center', color=color)
            if state['k'] is not None and isinstance(state['k'], int) and 0 <= state['k'] < n:
                k = state['k']
                for j in range(n):
                    ax_mat.add_patch(Rectangle((j-0.5, k-0.5), 1, 1, fill=False, edgecolor='yellow', linewidth=2))
                for i in range(n):
                    ax_mat.add_patch(Rectangle((k-0.5, i-0.5), 1, 1, fill=False, edgecolor='yellow', linewidth=2))
            ax_mat.set_xticks(range(n))
            ax_mat.set_yticks(range(n))
            ax_mat.set_xlabel('j')
            ax_mat.set_ylabel('i')
            ax_mat.set_title(f"Floyd–Warshall (APSP)\nStep {frame + 1}/{len(self.states)}")
            for spine in ax_mat.spines.values():
                spine.set_visible(False)

            ax_text.axis('off')
            k, i, j = state.get('k'), state.get('i'), state.get('j')
            lines = []
            # Header
            lines.append(f"Step {frame + 1} of {len(self.states)}")
            # Action label
            action = 'Start' if k == -1 else ('Finished' if k == len(D) else 'Check cell')
            lines.append(f"Action: {action}")
            if isinstance(k, int) and isinstance(i, int) and isinstance(j, int) and 0 <= k < len(D) and 0 <= i < len(D) and 0 <= j < len(D):
                d_ij = D[i][j]
                d_ik = D[i][k]
                d_kj = D[k][j]
                alt = (d_ik + d_kj) if (d_ik != float('inf') and d_kj != float('inf')) else float('inf')
                d_ij_str = '∞' if d_ij == float('inf') else int(d_ij)
                d_ik_str = '∞' if d_ik == float('inf') else int(d_ik)
                d_kj_str = '∞' if d_kj == float('inf') else int(d_kj)
                alt_str = '∞' if alt == float('inf') else int(alt)
                lines.extend([
                    "",
                    f"Using k={k} as an intermediate",
                    f"i={i}, j={j}",
                    f"Current: d[{i},{j}] = {d_ij_str}",
                    f"Via k: d[{i},{k}] + d[{k},{j}] = {d_ik_str} + {d_kj_str} = {alt_str}",
                    f"Update? {'YES' if alt < d_ij else 'NO'}",
                ])
            y = 0.95
            for line in lines:
                ax_text.text(0.05, y, line, fontsize=10, fontfamily='monospace')
                y -= 0.05
        self.anim = animation.FuncAnimation(self.fig, update, frames=len(self.states), interval=interval, repeat=False)
        plt.tight_layout()
        plt.show()


def get_user_input():
    print("\nFloyd–Warshall (APSP) Visualizer")
    print("===============================")
    print("Press Enter to use defaults or choose manual input.")
    mode = (input("\nMode [D=default, M=manual] [D]: ") or "D").strip().lower()
    if mode.startswith('m'):
        while True:
            try:
                n = int(input("\nNodes [6]: ") or "6")
                if 2 <= n <= 12:
                    break
            except ValueError:
                pass
            print("Invalid. Try again.")
        print("Enter adjacency matrix rows (use 'inf' for no path). Example for 3 nodes: 0 5 inf")
        D = []
        for i in range(n):
            while True:
                row = input(f"row {i}: ").strip()
                if not row:
                    continue
                toks = row.split()
                if len(toks) != n:
                    print(f"Need {n} values")
                    continue
                try:
                    vals = []
                    for t in toks:
                        if t.lower() in ('inf', 'infty', 'infinite', '∞'):
                            vals.append(float('inf'))
                        else:
                            vals.append(int(t))
                    D.append(vals)
                    break
                except ValueError:
                    print("Bad row. Use integers or 'inf'")
        for i in range(n):
            D[i][i] = 0
        interval = int(input("\nSpeed ms/frame [500]: ") or "500")
        return { 'mode': 'manual', 'D': D, 'interval': interval }
    else:
        while True:
            try:
                n = int(input("\nNodes [6]: ") or "6")
                density = float(input("Edge density 0..1 [0.5]: ") or "0.5")
                min_w = int(input("Min weight [1]: ") or "1")
                max_w = int(input("Max weight [9]: ") or "9")
                if 2 <= n <= 12 and 0 <= density <= 1 and max_w >= min_w:
                    break
            except ValueError:
                pass
            print("Invalid. Try again.")
        interval = int(input("\nSpeed ms/frame [500]: ") or "500")
        return { 'mode': 'default', 'n': n, 'density': density, 'min_w': min_w, 'max_w': max_w, 'interval': interval }


def main():
    params = get_user_input()
    vis = FloydWarshallVisualizer()
    if params['mode'] == 'manual':
        dist0 = params['D']
    else:
        dist0 = vis.generate_graph_matrix(n=params['n'], density=params['density'], min_w=params['min_w'], max_w=params['max_w'], directed=True)
    print("Initial distance matrix:")
    for row in dist0:
        print(row)
    vis.floyd_warshall_with_states(dist0)
    vis.animate(params['interval'])


if __name__ == "__main__":
    main()
