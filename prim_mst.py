import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
from queue import PriorityQueue


class PrimVisualizer:
    def __init__(self):
        self.G = nx.Graph()
        self.pos = None
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.states = []

    def generate_weighted_graph(self, n_nodes=8, n_edges=12, min_weight=1, max_weight=10):
        while True:
            edges = [(i, i + 1) for i in range(n_nodes - 1)]
            possible = [(i, j) for i in range(n_nodes) for j in range(i + 1, n_nodes)]
            possible = [e for e in possible if e not in edges]
            extra = random.sample(possible, min(max(0, n_edges - (n_nodes - 1)), len(possible)))
            edges.extend(extra)
            self.G.clear()
            for u, v in edges:
                w = random.randint(min_weight, max_weight)
                self.G.add_edge(u, v, weight=w)
            if nx.is_connected(self.G):
                break
        self.pos = nx.spring_layout(self.G)
        return self.G

    def prim_with_states(self, start=0):
        self.states = []
        visited = set([start])
        mst = []
        pq = PriorityQueue()
        for v in self.G.neighbors(start):
            pq.put((self.G[start][v]['weight'], start, v))
        self.states.append({'mst': list(mst), 'frontier': [], 'chosen': None, 'visited': set(visited), 'status': f'Start from {start}'})
        while not pq.empty() and len(visited) < self.G.number_of_nodes():
            frontier_snapshot = []
            temp = []
            while not pq.empty():
                w, u, v = pq.get()
                frontier_snapshot.append((u, v))
                temp.append((w, u, v))
            for item in temp:
                pq.put(item)
            self.states.append({'mst': list(mst), 'frontier': frontier_snapshot, 'chosen': None, 'visited': set(visited), 'status': 'Consider frontier edges'})
            w, u, v = pq.get()
            if v in visited:
                continue
            mst.append((u, v))
            visited.add(v)
            for x in self.G.neighbors(v):
                if x not in visited:
                    pq.put((self.G[v][x]['weight'], v, x))
            self.states.append({'mst': list(mst), 'frontier': frontier_snapshot, 'chosen': (u, v), 'visited': set(visited), 'status': f'Choose edge {u}-{v} (w={w})'})
        self.states.append({'mst': list(mst), 'frontier': [], 'chosen': None, 'visited': set(visited), 'status': 'MST complete'})
        return mst

    def animate(self, interval=800):
        def update(frame):
            self.fig.clear()
            state = self.states[frame]
            gs = self.fig.add_gridspec(1, 2, width_ratios=[2, 1])
            ax_graph = self.fig.add_subplot(gs[0])
            ax_text = self.fig.add_subplot(gs[1])

            # Graph panel
            nx.draw_networkx_edges(self.G, self.pos, edge_color='lightgray', ax=ax_graph)
            if state['frontier']:
                nx.draw_networkx_edges(self.G, self.pos, edgelist=state['frontier'], edge_color='yellow', width=2, ax=ax_graph)
            if state['mst']:
                nx.draw_networkx_edges(self.G, self.pos, edgelist=state['mst'], edge_color='g', width=3, ax=ax_graph)
            if state['chosen']:
                nx.draw_networkx_edges(self.G, self.pos, edgelist=[state['chosen']], edge_color='orange', width=4, ax=ax_graph)
            node_colors = ['lightgreen' if n in state['visited'] else 'lightblue' for n in self.G.nodes()]
            nx.draw_networkx_nodes(self.G, self.pos, node_color=node_colors, node_size=500, ax=ax_graph)
            labels = {(u, v): d['weight'] for u, v, d in self.G.edges(data=True)}
            nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=labels, ax=ax_graph)
            nx.draw_networkx_labels(self.G, self.pos, ax=ax_graph)
            ax_graph.set_title(f"Prim's MST\nStep {frame + 1}/{len(self.states)}")
            ax_graph.axis('off')

            # Text panel
            ax_text.axis('off')
            mst_weight = sum(self.G[u][v]['weight'] for (u, v) in state['mst']) if state['mst'] else 0
            frontier_str = []
            for (u, v) in state['frontier']:
                w = self.G[u][v]['weight']
                frontier_str.append(f"({u}-{v}, w={w})")
            chosen_txt = '-'
            chosen_w = '-'
            if state['chosen']:
                cu, cv = state['chosen']
                chosen_txt = f"{cu}-{cv}"
                chosen_w = self.G[cu][cv]['weight']
            lines = [
                "Status:",
                state['status'],
                "",
                "Visited:",
                f"{sorted(list(state['visited']))}",
                "",
                "Frontier (candidate edges):",
                ", ".join(frontier_str) if frontier_str else "(none)",
                "",
                "Chosen Edge:",
                f"Edge: {chosen_txt}  Weight: {chosen_w}",
                "",
                "MST So Far:",
                f"Edges: {state['mst']}",
                f"Total Weight: {mst_weight}",
                "",
                "Rule:",
                "Always pick the minimum-weight edge crossing",
                "the cut between visited and unvisited nodes."
            ]
            y = 0.95
            for line in lines:
                ax_text.text(0.05, y, line, fontsize=10, fontfamily='monospace')
                y -= 0.05

        self.anim = animation.FuncAnimation(self.fig, update, frames=len(self.states), interval=interval, repeat=False)
        plt.tight_layout()
        plt.show()


def get_user_input():
    print("\nPrim's MST Visualizer")
    print("=====================")
    while True:
        try:
            n_nodes = int(input("\nEnter number of nodes (default 8): ") or "8")
            n_edges = int(input("Enter number of edges (default 12): ") or "12")
            min_w = int(input("Enter min weight (default 1): ") or "1")
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
    vis = PrimVisualizer()
    G = vis.generate_weighted_graph(n_nodes, n_edges, min_w, max_w)
    print(f"Generated weighted graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    vis.prim_with_states(start)
    vis.animate(interval)


if __name__ == "__main__":
    main()
