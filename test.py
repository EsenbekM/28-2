import random


def binary_search(array, target):
    left = 0
    right = len(array) - 1
    while left <= right:
        midpoint = (left + right) // 2
        print(left, right)

        if array[midpoint] == target:
            return midpoint

        elif array[midpoint] < target:
            left = midpoint + 1

        else:
            right = midpoint - 1

    return -1

