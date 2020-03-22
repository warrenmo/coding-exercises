#!/usr/bin/env python3

import heapq

def kthSmallestBrute(arr, k):
    arrSorted = sorted(arr)
    return arrSorted[k-1]

def kthSmallestHeap(arr, k):
    maxHeap = list([i * -1 for i in arr[:k]])
    heapq.heapify(maxHeap)
    for i in [i * -1 for i in arr[k:]]:
        if i > maxHeap[0]:
            heapq.heappushpop(maxHeap, i)
        else:
            continue
    return maxHeap[0] * -1


if __name__ == "__main__":
    tests = [[17, 42, 5, 0, 10, -3, 2, 9]] 
    for test in tests:
        print(kthSmallestBrute(test, 3))
        print(kthSmallestHeap(test, 3))
