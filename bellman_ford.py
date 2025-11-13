import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random


class BellmanFordVisualizer:
    def __init__(self):
        self.G = nx.DiGraph()
        self.pos = None
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.states = []
        self.negative_cycle_edges = []

    def generate_directed_weighted_graph(self, n_nodes=6, n_edges=10, min_weight=-5, max_weight=10):
        self.G.clear()
        edges = set()
        possible = [(i, j) for i in range(n_nodes) for j in range(n_nodes) if i != j]
        random.shuffle(possible)
        for (u, v) in possible:
            if len(edges) >= n_edges:
                break
            w = random.randint(min_weight, max_weight)
            edges.add((u, v, w))
        for u, v, w in edges:
            self.G.add_edge(u, v, weight=w)
        if self.G.number_of_edges() == 0:
            # ensure at least one edge
            self.G.add_edge(0, 1, weight=random.randint(min_weight, max_weight))
        self.pos = nx.spring_layout(self.G)
        return self.G

    def bellman_ford_with_states(self, start=0):
        self.states = []
        self.negative_cycle_edges = []
        nodes = list(self.G.nodes())
        n = len(nodes)
        dist = {u: float('inf') for u in nodes}
        dist[start] = 0
        pred = {u: None for u in nodes}

        # Initial state
        self.states.append({'dist': dist.copy(), 'iter': 0, 'checking': None, 'updated': None, 'status': f'Start at node {start}'})

        edges = [(u, v, d['weight']) for u, v, d in self.G.edges(data=True)]
        # Relax edges V-1 times
        for i in range(1, n):
            changed = False
            for u, v, w in edges:
                self.states.append({'dist': dist.copy(), 'iter': i, 'checking': (u, v), 'updated': None, 'status': f'Iter {i}: relax edge {u}->{v} (w={w})'})
                if dist[u] != float('inf') and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    pred[v] = u
                    changed = True
                    self.states.append({'dist': dist.copy(), 'iter': i, 'checking': (u, v), 'updated': v, 'status': f'Updated dist[{v}] = {dist[v]}'})
            if not changed:
                self.states.append({'dist': dist.copy(), 'iter': i, 'checking': None, 'updated': None, 'status': 'No updates in this round; early stop'})
                break

        # Check for negative cycles
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                self.negative_cycle_edges.append((u, v))
                self.states.append({'dist': dist.copy(), 'iter': 'neg', 'checking': (u, v), 'updated': None, 'status': f'Negative cycle detected via {u}->{v}'})

        # Final state
        if not self.negative_cycle_edges:
            self.states.append({'dist': dist.copy(), 'iter': 'done', 'checking': None, 'updated': None, 'status': 'Algorithm completed'})

        return dist, pred

    def animate(self, interval=800):
        def update(frame):
            self.fig.clear()
            state = self.states[frame]
            gs = self.fig.add_gridspec(1, 2, width_ratios=[2, 1])
            ax_graph = self.fig.add_subplot(gs[0])
            ax_text = self.fig.add_subplot(gs[1])

            # Graph panel
            nx.draw_networkx_edges(self.G, self.pos, edge_color='lightgray', arrows=True, ax=ax_graph)
            if self.negative_cycle_edges:
                nx.draw_networkx_edges(self.G, self.pos, edgelist=self.negative_cycle_edges, edge_color='red', width=3, arrows=True, ax=ax_graph)
            if state['checking'] is not None:
                nx.draw_networkx_edges(self.G, self.pos, edgelist=[state['checking']], edge_color='yellow', width=3, arrows=True, ax=ax_graph)
            if state['updated'] is not None:
                nx.draw_networkx_nodes(self.G, self.pos, nodelist=[state['updated']], node_color='orange', node_size=600, ax=ax_graph)
            nx.draw_networkx_nodes(self.G, self.pos, node_color='lightblue', node_size=500, ax=ax_graph)
            labels = {(u, v): d['weight'] for u, v, d in self.G.edges(data=True)}
            nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=labels, ax=ax_graph)
            # Node labels: show distance
            dists = state['dist']
            node_labels = {u: f"{u}\n({('∞' if dists[u] == float('inf') else int(dists[u]))})" for u in self.G.nodes()}
            nx.draw_networkx_labels(self.G, self.pos, labels=node_labels, ax=ax_graph)
            ax_graph.set_title(f"Bellman–Ford Shortest Paths\nStep {frame + 1}/{len(self.states)}")
            ax_graph.axis('off')

            # Text panel
            ax_text.axis('off')
            lines = [
                "Status:",
                f"{state['status']}",
            ]
            if state['checking'] is not None:
                u, v = state['checking']
                w = self.G[u][v]['weight']
                du = dists[u]
                dv = dists[v]
                du_str = '∞' if du == float('inf') else int(du)
                dv_str = '∞' if dv == float('inf') else int(dv)
                alt = (du + w) if du != float('inf') else float('inf')
                alt_str = '∞' if alt == float('inf') else int(alt)
                updated = state['updated'] is not None
                lines.extend([
                    "",
                    "Relaxation:",
                    f"Edge {u}->{v} (w={w})",
                    f"Check: d[{u}] + w < d[{v}] ?",
                    f"{du_str} + {w} = {alt_str}  vs  {dv_str}",
                    f"Update d[{v}] = {alt_str} : {'YES' if updated else 'NO'}",
                ])
            if self.negative_cycle_edges:
                lines.extend([
                    "",
                    "Negative cycle edges detected:",
                    f"{self.negative_cycle_edges}"
                ])
            lines.extend([
                "",
                "Current distances:",
            ])
            for node in sorted(self.G.nodes()):
                val = dists[node]
                val_str = '∞' if val == float('inf') else int(val)
                lines.append(f"d[{node}] = {val_str}")

            y = 0.95
            for line in lines:
                ax_text.text(0.05, y, line, fontsize=10, fontfamily='monospace')
                y -= 0.05

        self.anim = animation.FuncAnimation(self.fig, update, frames=len(self.states), interval=interval, repeat=False)
        plt.tight_layout()
        plt.show()


def get_user_input():
    print("\nBellman–Ford Visualizer")
    print("=======================")
    while True:
        try:
            n_nodes = int(input("\nEnter number of nodes (default 6): ") or "6")
            n_edges = int(input("Enter number of directed edges (default 10): ") or "10")
            min_w = int(input("Enter min weight (can be negative, default -5): ") or "-5")
            max_w = int(input("Enter max weight (default 10): ") or "10")
            start = int(input(f"Enter start node (0-{n_nodes-1}, default 0): ") or "0")
            if 0 <= start < n_nodes and n_nodes > 1 and n_edges >= n_nodes - 1 and max_w >= min_w:
                break
        except ValueError:
            pass
        print("Invalid values, try again.")
    interval = int(input("\nEnter animation interval in ms (default 800): ") or "800")
    return n_nodes, n_edges, min_w, max_w, start, interval


def main():
    n_nodes, n_edges, min_w, max_w, start, interval = get_user_input()
    vis = BellmanFordVisualizer()
    G = vis.generate_directed_weighted_graph(n_nodes, n_edges, min_w, max_w)
    print(f"Generated directed weighted graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    vis.bellman_ford_with_states(start)
    vis.animate(interval)


if __name__ == "__main__":
    main()
