class BinaryHeap:
    def __init__(self):
        self.heap = []
        self.pos = {}

    def __len__(self):
        return len(self.heap)

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.pos[self.heap[i][1]] = i
        self.pos[self.heap[j][1]] = j

    def _sift_up(self, i):
        parent = (i - 1) // 2
        while i > 0 and self.heap[i][0] < self.heap[parent][0]:
            self._swap(i, parent)
            i = parent
            parent = (i - 1) // 2

    def _sift_down(self, i):
        n = len(self.heap)
        while True:
            smallest = i
            left = 2 * i + 1
            right = 2 * i + 2
            if left < n and self.heap[left][0] < self.heap[smallest][0]:
                smallest = left
            if right < n and self.heap[right][0] < self.heap[smallest][0]:
                smallest = right
            if smallest == i:
                break
            self._swap(i, smallest)
            i = smallest

    def push(self, priority, item):
        if item in self.pos:
            idx = self.pos[item]
            old_priority = self.heap[idx][0]
            self.heap[idx] = (priority, item)
            if priority < old_priority:
                self._sift_up(idx)
            else:
                self._sift_down(idx)
        else:
            self.heap.append((priority, item))
            self.pos[item] = len(self.heap) - 1
            self._sift_up(len(self.heap) - 1)

    def pop(self):
        if not self.heap:
            return None
        if len(self.heap) == 1:
            priority, item = self.heap.pop()
            del self.pos[item]
            return priority, item
        self._swap(0, len(self.heap) - 1)
        priority, item = self.heap.pop()
        del self.pos[item]
        self._sift_down(0)
        return priority, item

    def contains(self, item):
        return item in self.pos

    def is_empty(self):
        return len(self.heap) == 0
