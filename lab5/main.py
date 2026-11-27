import time
import random
import heapq
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# ─────────────────────────────────────────────
# DISJOINT-SET (Union-Find) for Kruskal
# ─────────────────────────────────────────────
class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])   # path compression
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True


# ─────────────────────────────────────────────
# KRUSKAL'S ALGORITHM
# Input : n – number of vertices
#         edges – list of (weight, u, v)
# Output: list of MST edges, total weight
# ─────────────────────────────────────────────
def kruskal(n, edges):
    """
    Kruskal's algorithm for Minimum Spanning Tree.
    Time complexity: O(E log E)
    """
    ds = DisjointSet(n)
    mst_edges = []
    total_weight = 0

    for weight, u, v in sorted(edges):          # sort by weight
        if ds.union(u, v):
            mst_edges.append((u, v, weight))
            total_weight += weight
            if len(mst_edges) == n - 1:
                break

    return mst_edges, total_weight


# ─────────────────────────────────────────────
# PRIM'S ALGORITHM
# Input : n – number of vertices
#         adj – adjacency list {u: [(weight, v), ...]}
# Output: list of MST edges, total weight
# ─────────────────────────────────────────────
def prim(n, adj):
    """
    Prim's algorithm for Minimum Spanning Tree.
    Time complexity: O(E log V) with min-heap
    """
    visited = [False] * n
    min_heap = [(0, 0, -1)]   # (weight, vertex, parent)
    mst_edges = []
    total_weight = 0

    while min_heap:
        weight, u, parent = heapq.heappop(min_heap)
        if visited[u]:
            continue
        visited[u] = True
        total_weight += weight
        if parent != -1:
            mst_edges.append((parent, u, weight))
        for w, v in adj[u]:
            if not visited[v]:
                heapq.heappush(min_heap, (w, v, u))

    return mst_edges, total_weight


# ─────────────────────────────────────────────
# GRAPH GENERATOR
# Generates a random connected weighted graph
# ─────────────────────────────────────────────
def generate_graph(n, max_weight=100):
    """Generate a random connected graph with n vertices."""
    edges = []
    adj = {i: [] for i in range(n)}

    # Ensure connectivity: create a spanning path first
    vertices = list(range(n))
    random.shuffle(vertices)
    for i in range(n - 1):
        u, v = vertices[i], vertices[i + 1]
        w = random.randint(1, max_weight)
        edges.append((w, u, v))
        adj[u].append((w, v))
        adj[v].append((w, u))

    # Add extra random edges (~1.5n extra)
    extra = int(1.5 * n)
    for _ in range(extra):
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v:
            w = random.randint(1, max_weight)
            edges.append((w, u, v))
            adj[u].append((w, v))
            adj[v].append((w, u))

    return edges, adj


# ─────────────────────────────────────────────
# EMPIRICAL ANALYSIS
# ─────────────────────────────────────────────
node_counts = [10, 50, 100, 200, 500, 750, 1000, 1500, 2000]
RUNS = 5   # average over multiple runs

kruskal_times = []
prim_times    = []

for n in node_counts:
    k_total = 0.0
    p_total = 0.0
    for _ in range(RUNS):
        edges, adj = generate_graph(n)

        t0 = time.perf_counter()
        kruskal(n, edges)
        k_total += time.perf_counter() - t0

        t0 = time.perf_counter()
        prim(n, adj)
        p_total += time.perf_counter() - t0

    kruskal_times.append(k_total / RUNS)
    prim_times.append(p_total / RUNS)
    print(f"n={n:5d}  Kruskal={kruskal_times[-1]:.6f}s  Prim={prim_times[-1]:.6f}s")


# ─────────────────────────────────────────────
# SAVE RESULTS TABLE
# ─────────────────────────────────────────────
print("\n{:>8}  {:>16}  {:>16}".format("Nodes", "Kruskal (s)", "Prim (s)"))
print("-" * 46)
for n, kt, pt in zip(node_counts, kruskal_times, prim_times):
    print(f"{n:>8}  {kt:>16.6f}  {pt:>16.6f}")


# ─────────────────────────────────────────────
# PLOT
# ─────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].plot(node_counts, kruskal_times, 'b-o', linewidth=2, markersize=6, label="Kruskal")
axes[0].plot(node_counts, prim_times,    'r-s', linewidth=2, markersize=6, label="Prim")
axes[0].set_xlabel("Number of Nodes (n)", fontsize=12)
axes[0].set_ylabel("Execution Time (s)",  fontsize=12)
axes[0].set_title("Kruskal vs Prim – Execution Time", fontsize=13)
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].plot(node_counts, kruskal_times, 'b-o', linewidth=2, markersize=6, label="Kruskal")
axes[1].set_xlabel("Number of Nodes (n)", fontsize=12)
axes[1].set_ylabel("Execution Time (s)",  fontsize=12)
axes[1].set_title("Kruskal – Execution Time", fontsize=13)
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("results_graph.png", dpi=150, bbox_inches='tight')
plt.close()
print("\nGraph saved to results_graph.png")