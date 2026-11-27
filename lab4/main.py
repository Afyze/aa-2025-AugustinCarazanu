import time
import random
import matplotlib.pyplot as plt

# ============================================================
# ALGORITHM IMPLEMENTATIONS
# ============================================================

INF = float('inf')


def dijkstra(graph, src):
    """Dijkstra's algorithm using adjacency matrix.
    Returns list of shortest distances from src to all vertices.
    """
    n = len(graph)
    dist = [INF] * n
    dist[src] = 0
    visited = [False] * n

    for _ in range(n):
        u = -1
        for v in range(n):
            if not visited[v] and (u == -1 or dist[v] < dist[u]):
                u = v

        if dist[u] == INF:
            break

        visited[u] = True

        for v in range(n):
            if graph[u][v] != INF and not visited[v]:
                new_dist = dist[u] + graph[u][v]
                if new_dist < dist[v]:
                    dist[v] = new_dist

    return dist


def floyd_warshall(graph):
    """Floyd-Warshall algorithm using adjacency matrix.
    Returns distance matrix with shortest paths between all pairs.
    """
    n = len(graph)
    dist = [row[:] for row in graph]

    for i in range(n):
        dist[i][i] = 0

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] != INF and dist[k][j] != INF:
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]

    return dist


# ============================================================
# GRAPH GENERATION
# ============================================================

def generate_graph(n, density):
    """Generate a random weighted directed graph as adjacency matrix.
    n: number of vertices
    density: fraction of possible edges present (0.0 to 1.0)
    """
    graph = [[INF] * n for _ in range(n)]
    for i in range(n):
        graph[i][i] = 0

    max_edges = n * (n - 1)
    target_edges = int(max_edges * density)

    possible_edges = [(i, j) for i in range(n) for j in range(n) if i != j]
    random.shuffle(possible_edges)

    # Ensure connectivity: create a random spanning path
    perm = list(range(n))
    random.shuffle(perm)
    for idx in range(len(perm) - 1):
        i, j = perm[idx], perm[idx + 1]
        graph[i][j] = random.randint(1, 100)
        possible_edges.remove((i, j))
        target_edges -= 1

    # Add remaining edges up to target density
    for i, j in possible_edges:
        if target_edges <= 0:
            break
        if graph[i][j] == INF:
            graph[i][j] = random.randint(1, 100)
            target_edges -= 1

    return graph


# ============================================================
# BENCHMARKING
# ============================================================

def benchmark_dijkstra_all_sources(graph):
    """Run Dijkstra from all sources for all-pairs comparison."""
    n = len(graph)
    start = time.perf_counter()
    for src in range(n):
        dijkstra(graph, src)
    end = time.perf_counter()
    return end - start


def benchmark_floyd_warshall(graph):
    """Run Floyd-Warshall and return execution time."""
    start = time.perf_counter()
    floyd_warshall(graph)
    end = time.perf_counter()
    return end - start


# ============================================================
# MAIN EXPERIMENT
# ============================================================

if __name__ == "__main__":
    random.seed(42)

    node_counts = [10, 20, 50, 75, 100, 150, 200, 300]
    sparse_density = 0.15
    dense_density = 0.70

    results = {
        'sparse': {'dijkstra': [], 'floyd': []},
        'dense': {'dijkstra': [], 'floyd': []}
    }

    print("Running benchmarks...")
    print(f"{'Nodes':<8} {'Sparse Dij':<16} {'Sparse FW':<16} {'Dense Dij':<16} {'Dense FW':<16}")
    print("-" * 72)

    for n in node_counts:
        g_sparse = generate_graph(n, sparse_density)
        t_dij_sparse = benchmark_dijkstra_all_sources(g_sparse)
        t_fw_sparse = benchmark_floyd_warshall(g_sparse)

        g_dense = generate_graph(n, dense_density)
        t_dij_dense = benchmark_dijkstra_all_sources(g_dense)
        t_fw_dense = benchmark_floyd_warshall(g_dense)

        results['sparse']['dijkstra'].append(t_dij_sparse)
        results['sparse']['floyd'].append(t_fw_sparse)
        results['dense']['dijkstra'].append(t_dij_dense)
        results['dense']['floyd'].append(t_fw_dense)

        print(f"{n:<8} {t_dij_sparse:<16.6f} {t_fw_sparse:<16.6f} {t_dij_dense:<16.6f} {t_fw_dense:<16.6f}")

    print("\nBenchmarks complete. Generating charts...\n")

    # ============================================================
    # CHART 1: Sparse graph
    # ============================================================
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(node_counts, results['sparse']['dijkstra'], 'b-o', label='Dijkstra (all sources)', linewidth=2)
    ax.plot(node_counts, results['sparse']['floyd'], 'r-s', label='Floyd-Warshall', linewidth=2)
    ax.set_xlabel('Number of Nodes')
    ax.set_ylabel('Time (seconds)')
    ax.set_title('Sparse Graph (15% density): Dijkstra vs Floyd-Warshall')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('chart_sparse.png', dpi=150)
    plt.show()

    # ============================================================
    # CHART 2: Dense graph
    # ============================================================
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(node_counts, results['dense']['dijkstra'], 'b-o', label='Dijkstra (all sources)', linewidth=2)
    ax.plot(node_counts, results['dense']['floyd'], 'r-s', label='Floyd-Warshall', linewidth=2)
    ax.set_xlabel('Number of Nodes')
    ax.set_ylabel('Time (seconds)')
    ax.set_title('Dense Graph (70% density): Dijkstra vs Floyd-Warshall')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('chart_dense.png', dpi=150)
    plt.show()

    # ============================================================
    # CHART 3: Combined comparison
    # ============================================================
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(node_counts, results['sparse']['dijkstra'], 'b-o', label='Dijkstra - Sparse', linewidth=2)
    ax.plot(node_counts, results['sparse']['floyd'], 'r-s', label='Floyd-Warshall - Sparse', linewidth=2)
    ax.plot(node_counts, results['dense']['dijkstra'], 'g-^', label='Dijkstra - Dense', linewidth=2)
    ax.plot(node_counts, results['dense']['floyd'], 'm-D', label='Floyd-Warshall - Dense', linewidth=2)
    ax.set_xlabel('Number of Nodes')
    ax.set_ylabel('Time (seconds)')
    ax.set_title('All Algorithms: Sparse vs Dense Graph Comparison')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('chart_combined.png', dpi=150)
    plt.show()

    # ============================================================
    # CHART 4: Log scale
    # ============================================================
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(node_counts, results['sparse']['dijkstra'], 'b-o', label='Dijkstra - Sparse', linewidth=2)
    ax.plot(node_counts, results['sparse']['floyd'], 'r-s', label='Floyd-Warshall - Sparse', linewidth=2)
    ax.plot(node_counts, results['dense']['dijkstra'], 'g-^', label='Dijkstra - Dense', linewidth=2)
    ax.plot(node_counts, results['dense']['floyd'], 'm-D', label='Floyd-Warshall - Dense', linewidth=2)
    ax.set_xlabel('Number of Nodes')
    ax.set_ylabel('Time (seconds, log scale)')
    ax.set_title('Algorithm Comparison (Log Scale)')
    ax.set_yscale('log')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('chart_logscale.png', dpi=150)
    plt.show()

    print("All charts saved to current directory.")