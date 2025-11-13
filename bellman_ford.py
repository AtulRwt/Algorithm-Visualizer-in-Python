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

    def set_graph_from_edges(self, n_nodes, edges):
        self.G.clear()
        self.G.add_nodes_from(range(n_nodes))
        for u, v, w in edges:
            if 0 <= u < n_nodes and 0 <= v < n_nodes and u != v:
                self.G.add_edge(u, v, weight=int(w))
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
            step_header = f"Step {frame + 1} of {len(self.states)}"
            # Determine action label
            action = 'Step'
            if state['iter'] == 'neg':
                action = 'Check negative cycle'
            elif state['iter'] == 'done':
                action = 'Finished'
            elif state['checking'] is not None and state['updated'] is not None:
                action = 'Update distance'
            elif state['checking'] is not None:
                action = 'Relax edge'
            lines = [
                step_header,
                f"Action: {action}",
                "",
                state['status'],
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
                    "Negative cycle edges:",
                    f"{self.negative_cycle_edges}"
                ])
            dist_line = []
            for node in sorted(self.G.nodes()):
                val = dists[node]
                val_str = '∞' if val == float('inf') else int(val)
                dist_line.append(f"d[{node}]={val_str}")
            lines.extend([
                "",
                "Distances:",
                ", ".join(dist_line)
            ])

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
    print("Press Enter to use defaults or choose manual input.")
    mode = (input("\nMode [D=default, M=manual] [D]: ") or "D").strip().lower()
    if mode.startswith('m'):
        while True:
            try:
                n_nodes = int(input("\nNodes [6]: ") or "6")
                start = int(input(f"Start node [0..{n_nodes-1}] [0]: ") or "0")
                if 0 <= start < n_nodes:
                    break
            except ValueError:
                pass
            print("Invalid. Try again.")
        print("Enter directed edges as: u v w  (blank line to finish). Nodes are 0..N-1")
        edges = []
        while True:
            line = input("> ").strip()
            if not line:
                break
            try:
                u, v, w = map(int, line.split())
                edges.append((u, v, w))
            except Exception:
                print("Bad line. Use: u v w")
        interval = int(input("\nSpeed ms/frame [800]: ") or "800")
        return { 'mode': 'manual', 'n_nodes': n_nodes, 'start': start, 'edges': edges, 'interval': interval }
    else:
        while True:
            try:
                n_nodes = int(input("\nNodes [6]: ") or "6")
                n_edges = int(input("Directed edges [10]: ") or "10")
                min_w = int(input("Min weight [-5]: ") or "-5")
                max_w = int(input("Max weight [10]: ") or "10")
                start = int(input(f"Start node [0..{n_nodes-1}] [0]: ") or "0")
                if 0 <= start < n_nodes and n_nodes > 1 and n_edges >= n_nodes - 1 and max_w >= min_w:
                    break
            except ValueError:
                pass
            print("Invalid. Try again.")
        interval = int(input("\nSpeed ms/frame [800]: ") or "800")
        return { 'mode': 'default', 'n_nodes': n_nodes, 'n_edges': n_edges, 'min_w': min_w, 'max_w': max_w, 'start': start, 'interval': interval }


def main():
    params = get_user_input()
    vis = BellmanFordVisualizer()
    if params['mode'] == 'manual':
        G = vis.set_graph_from_edges(params['n_nodes'], params['edges'])
        start = params['start']
    else:
        G = vis.generate_directed_weighted_graph(params['n_nodes'], params['n_edges'], params['min_w'], params['max_w'])
        start = params['start']
    print(f"Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    vis.bellman_ford_with_states(start)
    vis.animate(params['interval'])


if __name__ == "__main__":
    main()
