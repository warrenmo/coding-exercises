#!/usr/bin/env python3

import heapq
from random import randint

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

def kthSmallestRecursive(arr, k):
    n = len(arr)
    pivotInd = randint(0, n-1)
    pivot = arr[pivotInd]

    smaller = []
    larger = []
    for i, a in enumerate(arr):
        if i == pivotInd:
            continue
        elif a < pivot:
            smaller.append(a)
        else:
            larger.append(a)

    #print('looking for the {}-th smallest'.format(k))
    #print('pivot:\t\t{}'.format(pivot))
    #print('smaller:\t{}'.format(smaller))
    #print('larger:\t\t{}'.format(larger))

    nS = len(smaller)
    if nS == k - 1:
        return pivot
    elif nS > k - 1:
        return kthSmallestRecursive(smaller, k)
    else:
        return kthSmallestRecursive(larger, k-nS-1)


if __name__ == "__main__":
    tests = [[17, 42, 5, 0, 10, -3, 2, 9]]
    k = 3
    for test in tests:
        print(test)
        for f in [kthSmallestBrute, kthSmallestHeap, kthSmallestRecursive]:
            #print(test)
            #print(kthSmallestBrute(test, k))
            #print(kthSmallestHeap(test, k))
            #print(kthSmallestRecursive(test, k))
            print(f(test, k))
