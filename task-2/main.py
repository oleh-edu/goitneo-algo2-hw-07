#!/usr/bin/env python

import timeit
import matplotlib.pyplot as plt
from functools import lru_cache

# Implementation of Fibonacci calculations with LRU cache
@lru_cache(maxsize=None)  # Unlimited cache
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)

def measure_time(executions_number, fib_function, n, tree=None):
    if tree is not None:
        stmt = lambda: fib_function(n, tree)
    else:
        stmt = lambda: fib_function(n)
    return timeit.timeit(stmt, number=executions_number)  # Execute only once

# Implementation of Splay Tree
class Node:
    def __init__(self, data, parent=None):
        self.data = data
        self.parent = parent
        self.left_node = None
        self.right_node = None

class SplayTree:
    def __init__(self):
        self.root = None

    def insert(self, data):
        if self.root is None:
            self.root = Node(data)
        else:
            self._insert_node(data, self.root)

    def _insert_node(self, data, current_node):
        if data < current_node.data:
            if current_node.left_node:
                self._insert_node(data, current_node.left_node)
            else:
                current_node.left_node = Node(data, current_node)
        else:
            if current_node.right_node:
                self._insert_node(data, current_node.right_node)
            else:
                current_node.right_node = Node(data, current_node)

    def find(self, data):
        node = self.root
        while node is not None:
            if data < node.data:
                node = node.left_node
            elif data > node.data:
                node = node.right_node
            else:
                self._splay(node)
                return node.data
        return None

    def _splay(self, node):
        while node.parent is not None:
            if node.parent.parent is None:
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                else:
                    self._rotate_left(node.parent)
            elif node == node.parent.left_node and node.parent == node.parent.parent.left_node:
                self._rotate_right(node.parent.parent)
                self._rotate_right(node.parent)
            elif node == node.parent.right_node and node.parent == node.parent.parent.right_node:
                self._rotate_left(node.parent.parent)
                self._rotate_left(node.parent)
            else:
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                    self._rotate_left(node.parent)
                else:
                    self._rotate_left(node.parent)
                    self._rotate_right(node.parent)

    def _rotate_right(self, node):
        left_child = node.left_node
        if left_child is None:
            return
        node.left_node = left_child.right_node
        if left_child.right_node:
            left_child.right_node.parent = node
        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.left_node:
            node.parent.left_node = left_child
        else:
            node.parent.right_node = left_child
        left_child.right_node = node
        node.parent = left_child

    def _rotate_left(self, node):
        right_child = node.right_node
        if right_child is None:
            return
        node.right_node = right_child.left_node
        if right_child.left_node:
            right_child.left_node.parent = node
        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left_node:
            node.parent.left_node = right_child
        else:
            node.parent.right_node = right_child
        right_child.left_node = node
        node.parent = right_child

def fibonacci_splay(n, tree):
    cached_value = tree.find(n)
    if cached_value is not None:
        return cached_value
    if n <= 1:
        result = n
    else:
        result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n)
    return result

def main():
    n_values = list(range(0, 951, 50))
    lru_times = []
    splay_times = []
    executions_number = 5

    for n in n_values:
        tree = SplayTree()
        lru_times.append(measure_time(executions_number, fibonacci_lru, n))
        splay_times.append(measure_time(executions_number, fibonacci_splay, n, tree))

    print(f"{'n':<10}{'LRU Cache Time (s)':<25}{'Splay Tree Time (s)':<25}")
    print("-" * 60)
    for i in range(len(n_values)):
        print(f"{n_values[i]:<10}{lru_times[i]:<25.8f}{splay_times[i]:<25.8f}")

    # Building a graph
    print("\nBuilding a graph")
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, lru_times, marker='o', label='LRU Cache')
    plt.plot(n_values, splay_times, marker='s', label='Splay Tree')
    plt.xlabel("Fibonacci number (n)")
    plt.ylabel("Average execution time (seconds)")
    plt.title("Comparison of execution time: LRU Cache vs Splay Tree")
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nThe program was interrupted by the user (Ctrl+C).")
    except Exception as e:
        print(f"An error occurred: {e}")
