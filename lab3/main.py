import time
import random
import matplotlib.pyplot as plt
from collections import deque
import sys

sys.setrecursionlimit(100000)


# ============================================================
# DFS Implementation (Iterative with stack)
# ============================================================
def dfs(graph, start):
    visited = set()
    stack = [start]
    order = []
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            order.append(node)
            for neighbor in reversed(graph[node]):
                if neighbor not in visited:
                    stack.append(neighbor)
    return order


# ============================================================
# BFS Implementation (Queue-based)
# ============================================================
def bfs(graph, start):
    visited = set()
    queue = deque([start])
    visited.add(start)
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order


# ============================================================
# Graph generators
# ============================================================
def generate_sparse_graph(n):
    """Sparse connected graph: spanning tree + V/10 extra edges."""
    graph = {i: [] for i in range(n)}
    for i in range(1, n):
        parent = random.randint(0, i - 1)
        graph[parent].append(i)
        graph[i].append(parent)
    extra = max(1, n // 10)
    for _ in range(extra):
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v and v not in graph[u]:
            graph[u].append(v)
            graph[v].append(u)
    return graph


def generate_dense_graph(n):
    """Dense connected graph: ~30% of all possible edges."""
    graph = {i: [] for i in range(n)}
    for i in range(1, n):
        parent = random.randint(0, i - 1)
        graph[parent].append(i)
        graph[i].append(parent)
    target_edges = int(0.3 * n * (n - 1) / 2)
    edge_set = set()
    for node in graph:
        for nb in graph[node]:
            edge_set.add((min(node, nb), max(node, nb)))
    attempts = 0
    while len(edge_set) < target_edges and attempts < target_edges * 3:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v:
            e = (min(u, v), max(u, v))
            if e not in edge_set:
                edge_set.add(e)
                graph[u].append(v)
                graph[v].append(u)
        attempts += 1
    return graph


# ============================================================
# Timing function
# ============================================================
def measure_time(func, graph, start, runs=5):
    times = []
    for _ in range(runs):
        t0 = time.perf_counter()
        func(graph, start)
        t1 = time.perf_counter()
        times.append(t1 - t0)
    return sum(times) / len(times)


# ============================================================
# Run experiments
# ============================================================
random.seed(42)

sparse_sizes = [100, 500, 1000, 2000, 5000, 10000, 20000, 50000]
dense_sizes = [100, 500, 1000, 2000, 5000]

results_sparse_dfs = []
results_sparse_bfs = []
results_dense_dfs = []
results_dense_bfs = []

print("=" * 55)
print("SPARSE GRAPH EXPERIMENTS")
print("=" * 55)
print(f"{'Nodes':>8}  {'DFS (s)':>12}  {'BFS (s)':>12}")
print("-" * 36)

for n in sparse_sizes:
    g = generate_sparse_graph(n)
    t_dfs = measure_time(dfs, g, 0)
    t_bfs = measure_time(bfs, g, 0)
    results_sparse_dfs.append(t_dfs)
    results_sparse_bfs.append(t_bfs)
    print(f"{n:>8}  {t_dfs:>12.6f}  {t_bfs:>12.6f}")

print()
print("=" * 55)
print("DENSE GRAPH EXPERIMENTS")
print("=" * 55)
print(f"{'Nodes':>8}  {'DFS (s)':>12}  {'BFS (s)':>12}")
print("-" * 36)

for n in dense_sizes:
    g = generate_dense_graph(n)
    t_dfs = measure_time(dfs, g, 0)
    t_bfs = measure_time(bfs, g, 0)
    results_dense_dfs.append(t_dfs)
    results_dense_bfs.append(t_bfs)
    print(f"{n:>8}  {t_dfs:>12.6f}  {t_bfs:>12.6f}")

print()
print("Generating graphs...")


# ============================================================
# Figure 1: DFS vs BFS on Sparse Graphs
# ============================================================
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(sparse_sizes, results_sparse_dfs, 'o-', label='DFS', color='#2196F3', linewidth=2)
ax.plot(sparse_sizes, results_sparse_bfs, 's-', label='BFS', color='#F44336', linewidth=2)
ax.set_xlabel('Number of Nodes (V)', fontsize=12)
ax.set_ylabel('Time (seconds)', fontsize=12)
ax.set_title('DFS vs BFS on Sparse Graphs', fontsize=14)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('fig_sparse_comparison.png', dpi=150)
plt.show()

# ============================================================
# Figure 2: DFS vs BFS on Dense Graphs
# ============================================================
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(dense_sizes, results_dense_dfs, 'o-', label='DFS', color='#2196F3', linewidth=2)
ax.plot(dense_sizes, results_dense_bfs, 's-', label='BFS', color='#F44336', linewidth=2)
ax.set_xlabel('Number of Nodes (V)', fontsize=12)
ax.set_ylabel('Time (seconds)', fontsize=12)
ax.set_title('DFS vs BFS on Dense Graphs', fontsize=14)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('fig_dense_comparison.png', dpi=150)
plt.show()

# ============================================================
# Figure 3: DFS Sparse vs Dense
# ============================================================
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(sparse_sizes, results_sparse_dfs, 'o-', label='DFS Sparse', color='#2196F3', linewidth=2)
ax.plot(dense_sizes, results_dense_dfs, 's-', label='DFS Dense', color='#FF9800', linewidth=2)
ax.set_xlabel('Number of Nodes (V)', fontsize=12)
ax.set_ylabel('Time (seconds)', fontsize=12)
ax.set_title('DFS: Sparse vs Dense Graph Performance', fontsize=14)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('fig_dfs_density.png', dpi=150)
plt.show()

# ============================================================
# Figure 4: BFS Sparse vs Dense
# ============================================================
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(sparse_sizes, results_sparse_bfs, 'o-', label='BFS Sparse', color='#F44336', linewidth=2)
ax.plot(dense_sizes, results_dense_bfs, 's-', label='BFS Dense', color='#9C27B0', linewidth=2)
ax.set_xlabel('Number of Nodes (V)', fontsize=12)
ax.set_ylabel('Time (seconds)', fontsize=12)
ax.set_title('BFS: Sparse vs Dense Graph Performance', fontsize=14)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('fig_bfs_density.png', dpi=150)
plt.show()

print("Done. 4 graphs saved as PNG files in the current directory.")