import random
import time
import sys
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


# SECTION 1 ALGORITHM IMPLEMENTATIONS

# this global variable counts how many comparisons each algorithm makes
comparison_count = 0

def reset_counter():
    # resets the counter before each benchmark run so results don't mix
    global comparison_count
    comparison_count = 0


# quicksort
# picks a pivot from the middle of the array and splits elements into
# left (smaller), middle (equal), and right (larger), then recurses on each side
def quicksort(arr):
    global comparison_count
    if len(arr) <= 1:
        return arr  # base case: a single element is already sorted
    pivot = arr[len(arr) // 2]  # choosing the middle element avoids worst case on sorted input
    left   = []
    middle = []
    right  = []
    for x in arr:
        comparison_count += 1  # count every time we compare an element to the pivot
        if x < pivot:
            left.append(x)
        elif x == pivot:
            middle.append(x)
        else:
            right.append(x)
    return quicksort(left) + middle + quicksort(right)  # combine the sorted parts


# mergesort
# splits the array in half recursively until we have single elements,
# then merges those halves back together in sorted order
def mergesort(arr):
    if len(arr) <= 1:
        return arr  # base case: nothing to split
    mid   = len(arr) // 2         # find the midpoint
    left  = mergesort(arr[:mid])  # sort the left half
    right = mergesort(arr[mid:])  # sort the right half
    return merge(left, right)     # merge both sorted halves

def merge(left, right):
    global comparison_count
    result = []
    i = j = 0
    # walk through both halves simultaneously, picking the smaller element each time
    while i < len(left) and j < len(right):
        comparison_count += 1  # count every head-to-head comparison between the two halves
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])   # append whatever is left in the left half
    result.extend(right[j:])  # append whatever is left in the right half
    return result


# heapsort
# rearranges the array into a max-heap structure, then repeatedly moves
# the largest element (the root) to the end of the array
def heapsort(arr):
    arr = arr[:]  # work on a copy so the original array stays unchanged
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):  # start from the last non-leaf node and heapify down
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]  # swap the current max (root) to its final position
        heapify(arr, i, 0)               # restore the heap property on the reduced array
    return arr

def heapify(arr, n, i):
    # ensures the subtree rooted at index i satisfies the max-heap property
    global comparison_count
    largest = i
    left    = 2 * i + 1  # index of left child
    right   = 2 * i + 2  # index of right child
    if left < n:
        comparison_count += 1
        if arr[left] > arr[largest]:   # check if left child is larger than current root
            largest = left
    if right < n:
        comparison_count += 1
        if arr[right] > arr[largest]:  # check if right child is even larger
            largest = right
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  # swap root with the largest child
        heapify(arr, n, largest)                      # recursively fix the affected subtree


# insertionsort (4th algorithm, chosen for contrast with the o(n log n) group)
# takes each element and inserts it into the correct position among the already-sorted elements
def insertionsort(arr):
    global comparison_count
    arr = arr[:]  # work on a copy
    for i in range(1, len(arr)):
        key = arr[i]  # the element we are currently placing
        j   = i - 1
        while j >= 0:
            comparison_count += 1     # count each comparison as we shift elements rightward
            if arr[j] > key:
                arr[j + 1] = arr[j]  # shift the larger element one position to the right
                j -= 1
            else:
                break  # found the correct spot, stop shifting
        arr[j + 1] = key  # place the element in its correct position
    return arr


# SECTION 2 INPUT DATA PROPERTIES

# we test three distributions to expose best, average, and worst case behaviour
# random   - shuffled data, the typical real-world scenario
# sorted   - already ascending, best case for insertionsort, tricky for naive quicksort
# reversed - descending, often the hardest case for comparison-based sorts

def generate_random(n):
    return random.sample(range(n * 10), n)  # n unique random integers

def generate_sorted(n):
    return list(range(n))  # 0, 1, 2, ..., n-1

def generate_reversed(n):
    return list(range(n, 0, -1))  # n, n-1, ..., 1


# SECTION 3 METRICS

# two metrics are recorded for each run:
#   execution time   - measures real-world speed in seconds
#   comparison count - measures algorithmic work, independent of hardware speed

def benchmark(sort_fn, data):
    reset_counter()            # clear the global counter before starting
    arr   = data[:]            # sort a copy so the original stays intact for other algorithms
    start = time.perf_counter()
    sort_fn(arr)
    elapsed = time.perf_counter() - start  # total time taken by the sort
    return elapsed, comparison_count


# SECTION 4 EMPIRICAL ANALYSIS

# input sizes span a wide range so we can clearly see how each algorithm scales
sizes = [100, 500, 1000, 2000, 5000, 10000]

distributions = {
    "random":   generate_random,
    "sorted":   generate_sorted,
    "reversed": generate_reversed,
}

algorithms = {
    "quicksort":     quicksort,
    "mergesort":     mergesort,
    "heapsort":      heapsort,
    "insertionsort": insertionsort,
}

# python's default recursion limit is 1000; deep recursive calls on large arrays need more
sys.setrecursionlimit(20000)

# nested dict: results[distribution][algorithm] holds lists of times and comparison counts
results = {dist: {alg: {"time": [], "comps": []} for alg in algorithms}
           for dist in distributions}

print("running benchmarks, this may take a moment...\n")

for dist_name, gen_fn in distributions.items():
    print(f"  distribution: {dist_name}")
    for n in sizes:
        data = gen_fn(n)  # generate fresh input for this size and distribution
        for alg_name, sort_fn in algorithms.items():
            t, c = benchmark(sort_fn, data)                  # run the benchmark
            results[dist_name][alg_name]["time"].append(t)   # store time result
            results[dist_name][alg_name]["comps"].append(c)  # store comparison count
        print(f"    n={n:>6}  done")
    print()

print("benchmarks complete, generating plots...\n")


# SECTION 5 GRAPHICAL PRESENTATION

# one distinct color per algorithm so the lines are easy to tell apart
colors = {
    "quicksort":     "#e74c3c",
    "mergesort":     "#3498db",
    "heapsort":      "#2ecc71",
    "insertionsort": "#f39c12",
}

fig = plt.figure(figsize=(18, 14))
fig.suptitle("empirical analysis of sorting algorithms", fontsize=16, fontweight="bold", y=0.98)

# layout: 3 rows (one per distribution) x 2 columns (time on left, comparisons on right)
gs = gridspec.GridSpec(3, 2, figure=fig, hspace=0.45, wspace=0.3)

for row, dist_name in enumerate(distributions):
    # left column: execution time
    ax_time = fig.add_subplot(gs[row, 0])
    for alg_name in algorithms:
        ax_time.plot(
            sizes,
            results[dist_name][alg_name]["time"],
            marker="o", linewidth=2, markersize=4,
            color=colors[alg_name], label=alg_name
        )
    ax_time.set_title(f"{dist_name} input - execution time", fontsize=11)
    ax_time.set_xlabel("input size (n)")
    ax_time.set_ylabel("time (seconds)")
    ax_time.legend(fontsize=8)
    ax_time.grid(True, alpha=0.3)

    # right column: number of comparisons
    ax_comp = fig.add_subplot(gs[row, 1])
    for alg_name in algorithms:
        ax_comp.plot(
            sizes,
            results[dist_name][alg_name]["comps"],
            marker="s", linewidth=2, markersize=4,
            color=colors[alg_name], label=alg_name
        )
    ax_comp.set_title(f"{dist_name} input - number of comparisons", fontsize=11)
    ax_comp.set_xlabel("input size (n)")
    ax_comp.set_ylabel("comparisons")
    ax_comp.legend(fontsize=8)
    ax_comp.grid(True, alpha=0.3)

plt.savefig("sorting_analysis.png", dpi=150, bbox_inches="tight")  # save the figure to disk
plt.show()
print("plot saved as 'sorting_analysis.png'")