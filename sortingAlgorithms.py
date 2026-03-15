"""
Assignment 2: Divide-and-Conquer Algorithms
Implementations of Merge Sort and Quick Sort with performance benchmarking.
"""

import time
import tracemalloc
import random
import sys

# ─────────────────────────────────────────────
#  MERGE SORT
# ─────────────────────────────────────────────

def merge_sort(arr):
    """
    Merge Sort: Divide-and-Conquer sorting algorithm.
    
    Steps:
      1. Base case: arrays of length 0 or 1 are already sorted.
      2. Divide: split the array into two halves.
      3. Conquer: recursively sort each half.
      4. Combine: merge the two sorted halves into one sorted array.
    
    Time Complexity:
      Best / Worst / Average: O(n log n)
    Space Complexity: O(n) auxiliary
    """
    if len(arr) <= 1:
        return arr

    # --- Divide ---
    mid = len(arr) // 2
    left  = merge_sort(arr[:mid])   # Conquer left half
    right = merge_sort(arr[mid:])   # Conquer right half

    return _merge(left, right)      # Combine


def _merge(left, right):
    """Merge two sorted lists into one sorted list."""
    result = []
    i = j = 0

    # Compare elements from both halves and append the smaller one
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Append any remaining elements
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ─────────────────────────────────────────────
#  QUICK SORT
# ─────────────────────────────────────────────

def quick_sort(arr, low=0, high=None):
    """
    Quick Sort: Divide-and-Conquer sorting algorithm (in-place).
    
    Steps:
      1. Base case: sub-array of size 0 or 1 is already sorted.
      2. Partition: choose a pivot (median-of-three) and rearrange
         elements so that all elements < pivot come before it and
         all elements > pivot come after it.
      3. Recurse on the left and right sub-arrays.
    
    Pivot strategy: median-of-three to avoid O(n²) on sorted input.
    
    Time Complexity:
      Best / Average: O(n log n)
      Worst (degenerate pivot): O(n²)
    Space Complexity: O(log n) stack space on average
    """
    if high is None:
        arr = arr[:]        # Work on a copy so the original is untouched
        high = len(arr) - 1

    if low < high:
        pivot_index = _partition(arr, low, high)
        quick_sort(arr, low, pivot_index - 1)
        quick_sort(arr, pivot_index + 1, high)

    return arr


def _median_of_three(arr, low, high):
    """Return the index of the median value among arr[low], arr[mid], arr[high]."""
    mid = (low + high) // 2
    # Sort the three candidates and return the middle index
    if arr[low] > arr[mid]:
        arr[low], arr[mid] = arr[mid], arr[low]
    if arr[low] > arr[high]:
        arr[low], arr[high] = arr[high], arr[low]
    if arr[mid] > arr[high]:
        arr[mid], arr[high] = arr[high], arr[mid]
    # arr[mid] is now the median; place it at high-1 as pivot
    arr[mid], arr[high] = arr[high], arr[mid]
    return arr[high]


def _partition(arr, low, high):
    """
    Lomuto partition scheme with median-of-three pivot selection.
    Rearranges arr[low..high] around the chosen pivot.
    Returns the final index of the pivot.
    """
    pivot = _median_of_three(arr, low, high)
    i = low - 1                     # Index of the last element ≤ pivot

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# ─────────────────────────────────────────────
#  BENCHMARKING UTILITIES
# ─────────────────────────────────────────────

def benchmark(sort_fn, data, label):
    """
    Measure execution time (seconds) and peak memory usage (KB)
    for a given sorting function on a copy of `data`.
    """
    arr = data[:]  # Ensure we sort a fresh copy each time

    tracemalloc.start()
    start_time = time.perf_counter()

    sort_fn(arr)   # Run the algorithm

    elapsed = time.perf_counter() - start_time
    _, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    peak_kb = peak_mem / 1024
    print(f"  {label:<35} time={elapsed:.6f}s   peak_mem={peak_kb:.1f} KB")
    return elapsed, peak_kb


def run_benchmarks():
    """Run both algorithms on sorted, reverse-sorted, and random datasets."""
    sizes = [1_000, 5_000, 10_000]

    print("=" * 70)
    print("  DIVIDE-AND-CONQUER SORTING BENCHMARK")
    print("=" * 70)

    for n in sizes:
        datasets = {
            "Sorted":         list(range(n)),
            "Reverse-Sorted": list(range(n, 0, -1)),
            "Random":         random.sample(range(n * 10), n),
        }

        print(f"\n── n = {n:,} ──────────────────────────────────────────────")

        for dtype, data in datasets.items():
            print(f"\n  [{dtype}]")
            benchmark(merge_sort, data, "Merge Sort")

            # Increase recursion limit for large Quick Sort inputs on sorted data
            old_limit = sys.getrecursionlimit()
            sys.setrecursionlimit(max(old_limit, n * 2))
            try:
                benchmark(quick_sort, data, "Quick Sort (median-of-3)")
            except RecursionError:
                print(f"  {'Quick Sort (median-of-3)':<35} RecursionError on n={n}")
            finally:
                sys.setrecursionlimit(old_limit)

    print("\n" + "=" * 70)


# ─────────────────────────────────────────────
#  CORRECTNESS VERIFICATION
# ─────────────────────────────────────────────

def verify():
    """Quick smoke-test to verify both algorithms produce correct output."""
    tests = [
        [],
        [1],
        [3, 1, 4, 1, 5, 9, 2, 6],
        list(range(10, 0, -1)),
    ]
    print("\nCorrectness checks:")
    for t in tests:
        ms = merge_sort(t[:])
        qs = quick_sort(t[:])
        expected = sorted(t)
        status = "✓" if ms == expected == qs else "✗"
        print(f"  {status}  Input: {t[:8]}{'...' if len(t)>8 else ''}")


if __name__ == "__main__":
    verify()
    run_benchmarks()