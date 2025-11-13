import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random


class KruskalVisualizer:
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

    def set_graph_from_edges(self, n_nodes, edges):
        self.G.clear()
        self.G.add_nodes_from(range(n_nodes))
        for u, v, w in edges:
            if 0 <= u < n_nodes and 0 <= v < n_nodes and u != v:
                self.G.add_edge(u, v, weight=int(w))
        self.pos = nx.spring_layout(self.G)
        return self.G

    def kruskal_with_states(self):
        self.states = []
        parent = {u: u for u in self.G.nodes()}
        rank = {u: 0 for u in self.G.nodes()}

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            ra, rb = find(a), find(b)
            if ra == rb:
                return False
            if rank[ra] < rank[rb]:
                parent[ra] = rb
            elif rank[ra] > rank[rb]:
                parent[rb] = ra
            else:
                parent[rb] = ra
                rank[ra] += 1
            return True

        edges = [(u, v, d['weight']) for u, v, d in self.G.edges(data=True)]
        edges.sort(key=lambda x: x[2])
        mst = []

        self.states.append({
            'mst': list(mst),
            'candidate': None,
            'decision': None,
            'status': 'Start Kruskal: sort edges by weight'
        })

        for u, v, w in edges:
            can_include = (find(u) != find(v))
            self.states.append({
                'mst': list(mst),
                'candidate': (u, v),
                'decision': 'check',
                'status': f'Check edge {u}-{v} (w={w})'
            })
            if can_include:
                union(u, v)
                mst.append((u, v))
                self.states.append({
                    'mst': list(mst),
                    'candidate': (u, v),
                    'decision': 'include',
                    'status': f'Include edge {u}-{v}'
                })
            else:
                self.states.append({
                    'mst': list(mst),
                    'candidate': (u, v),
                    'decision': 'reject',
                    'status': f'Reject edge {u}-{v} (forms cycle)'
                })

        self.states.append({
            'mst': list(mst),
            'candidate': None,
            'decision': 'done',
            'status': 'MST complete'
        })

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
            if state['mst']:
                nx.draw_networkx_edges(self.G, self.pos, edgelist=state['mst'], edge_color='g', width=3, ax=ax_graph)
            if state['candidate']:
                cand = [state['candidate']]
                color = 'yellow' if state['decision'] in ['check'] else ('g' if state['decision'] == 'include' else 'red')
                nx.draw_networkx_edges(self.G, self.pos, edgelist=cand, edge_color=color, width=3, ax=ax_graph)
            nx.draw_networkx_nodes(self.G, self.pos, node_color='lightblue', node_size=500, ax=ax_graph)
            labels = {(u, v): d['weight'] for u, v, d in self.G.edges(data=True)}
            nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=labels, ax=ax_graph)
            nx.draw_networkx_labels(self.G, self.pos, ax=ax_graph)
            ax_graph.set_title(f"Kruskal's MST\nStep {frame + 1}/{len(self.states)}")
            ax_graph.axis('off')

            # Text panel
            ax_text.axis('off')
            mst_weight = sum(self.G[u][v]['weight'] for (u, v) in state['mst']) if state['mst'] else 0
            cand_txt = '-'
            cand_w = '-'
            if state['candidate']:
                u, v = state['candidate']
                cand_txt = f"{u}-{v}"
                cand_w = self.G[u][v]['weight']
            decision = state.get('decision', '-')
            action_map = { 'check': 'Checking edge', 'include': 'Add edge', 'reject': 'Skip edge', 'done': 'Finished' }
            action = action_map.get(decision, state['status'])
            lines = [
                f"Step {frame + 1} of {len(self.states)}",
                f"Action: {action}",
                f"Candidate: {cand_txt} (w={cand_w})",
                "",
                f"MST edges: {state['mst']}",
                f"MST total weight: {mst_weight}",
                "",
                "Rule: add edge only if it makes no cycle"
            ]
            y = 0.95
            for line in lines:
                ax_text.text(0.05, y, line, fontsize=10, fontfamily='monospace')
                y -= 0.05

        self.anim = animation.FuncAnimation(self.fig, update, frames=len(self.states), interval=interval, repeat=False)
        plt.tight_layout()
        plt.show()


def get_user_input():
    print("\nKruskal's MST Visualizer")
    print("========================")
    print("Press Enter to use defaults or choose manual input.")
    mode = (input("\nMode [D=default, M=manual] [D]: ") or "D").strip().lower()
    if mode.startswith('m'):
        while True:
            try:
                n_nodes = int(input("\nNodes [8]: ") or "8")
                break
            except ValueError:
                print("Invalid. Try again.")
        print("Enter undirected edges as: u v w  (blank line to finish). Nodes are 0..N-1")
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
        return { 'mode': 'manual', 'n_nodes': n_nodes, 'edges': edges, 'interval': interval }
    else:
        while True:
            try:
                n_nodes = int(input("\nNodes [8]: ") or "8")
                n_edges = int(input("Edges [12]: ") or "12")
                min_w = int(input("Min weight [1]: ") or "1")
                max_w = int(input("Max weight [10]: ") or "10")
                if n_nodes > 1 and n_edges >= n_nodes - 1 and max_w >= min_w:
                    break
            except ValueError:
                pass
            print("Invalid. Try again.")
        interval = int(input("\nSpeed ms/frame [800]: ") or "800")
        return { 'mode': 'default', 'n_nodes': n_nodes, 'n_edges': n_edges, 'min_w': min_w, 'max_w': max_w, 'interval': interval }


def main():
    params = get_user_input()
    vis = KruskalVisualizer()
    if params['mode'] == 'manual':
        G = vis.set_graph_from_edges(params['n_nodes'], params['edges'])
    else:
        G = vis.generate_weighted_graph(params['n_nodes'], params['n_edges'], params['min_w'], params['max_w'])
    print(f"Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    vis.kruskal_with_states()
    vis.animate(params['interval'])


if __name__ == "__main__":
    main()
