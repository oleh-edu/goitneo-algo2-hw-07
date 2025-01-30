import random
import time

class Node:
    def __init__(self, key, value):
        self.data = (key, value)
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def push(self, key, value):
        new_node = Node(key, value)
        new_node.next = self.head
        if self.head:
            self.head.prev = new_node
        else:
            self.tail = new_node
        self.head = new_node
        return new_node

    def remove(self, node):
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        node.prev = None
        node.next = None

    def move_to_front(self, node):
        if node != self.head:
            self.remove(node)
            node.next = self.head
            if self.head:
                self.head.prev = node
            self.head = node

    def remove_last(self):
        if self.tail:
            last = self.tail
            self.remove(last)
            return last
        return None

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.list = DoublyLinkedList()

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self.list.move_to_front(node)
            return node.data[1]
        return -1

    def put(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.data = (key, value)
            self.list.move_to_front(node)
        else:
            if len(self.cache) >= self.capacity:
                last = self.list.remove_last()
                if last:
                    del self.cache[last.data[0]]
            new_node = self.list.push(key, value)
            self.cache[key] = new_node

def range_sum_no_cache(array, L, R):
    return sum(array[L:R+1])

def update_no_cache(array, index, value):
    array[index] = value

def range_sum_with_cache(array, L, R):
    cached_result = cache.get((L, R))
    if cached_result != -1:
        return cached_result
    
    result = sum(array[L:R+1])
    cache.put((L, R), result)
    return result

def update_with_cache(array, index, value):
    array[index] = value
    cache.cache.clear()

def generate_queries(Q, N):
    queries = []
    for _ in range(Q):
        if random.random() < 0.7:
            L, R = sorted(random.sample(range(N), 2))
            queries.append(('Range', L, R))
        else:
            index = random.randint(0, N-1)
            value = random.randint(1, 1000)
            queries.append(('Update', index, value))
    return queries

def execute_no_cache(array, queries):
    start_time = time.time()
    for query in queries:
        if query[0] == 'Range':
            range_sum_no_cache(array, query[1], query[2])
        else:
            update_no_cache(array, query[1], query[2])
    return time.time() - start_time

def execute_with_cache(array, queries):
    global cache
    cache = LRUCache(5000)
    start_time = time.time()
    for query in queries:
        if query[0] == 'Range':
            range_sum_with_cache(array, query[1], query[2])
        else:
            update_with_cache(array, query[1], query[2])
    return time.time() - start_time

if __name__ == "__main__":
    N = 100_000
    array = [random.randint(1, 1000) for _ in range(N)]
    cache = LRUCache(5000)
    
    Q = 50_000
    queries = generate_queries(Q, N)
    
    no_cache_time = execute_no_cache(array, queries)
    cache_time = execute_with_cache(array, queries)
    
    print(f"[*] Execution time without caching: {no_cache_time:.2f} seconds")
    print(f"[*] Execution time with LRU cache: {cache_time:.2f} seconds")
