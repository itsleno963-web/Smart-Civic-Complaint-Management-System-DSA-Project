"""Module 1 (Trees / Priority Queue): Array-based Max Heap.
The complaint with the highest priority is always at the root."""


def _key(c):
    # higher priority first; for equal priority the older (smaller) ID first
    return (c["priority"], -c["id"])


class MaxHeap:
    def __init__(self):
        self.a = []

    def __len__(self):
        return len(self.a)

    def peek(self):                       # O(1)
        return self.a[0] if self.a else None

    def push(self, complaint):            # O(log n)
        self.a.append(complaint)
        i = len(self.a) - 1
        while i > 0 and _key(self.a[i]) > _key(self.a[(i - 1) // 2]):
            p = (i - 1) // 2
            self.a[i], self.a[p] = self.a[p], self.a[i]
            i = p

    def pop(self):                        # O(log n)
        if not self.a:
            return None
        top = self.a[0]
        last = self.a.pop()
        if self.a:
            self.a[0] = last
            self._heapify_down(0)
        return top

    def _heapify_down(self, i):
        n = len(self.a)
        while True:
            l, r, big = 2 * i + 1, 2 * i + 2, i
            if l < n and _key(self.a[l]) > _key(self.a[big]): big = l
            if r < n and _key(self.a[r]) > _key(self.a[big]): big = r
            if big == i:
                return
            self.a[i], self.a[big] = self.a[big], self.a[i]
            i = big
