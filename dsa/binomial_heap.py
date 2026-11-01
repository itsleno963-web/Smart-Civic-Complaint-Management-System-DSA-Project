"""Module 5 (Advanced Data Structures): Binomial Heap (max-heap version).
A collection of binomial trees; two heaps can be MERGED in O(log n).
Used to merge department-wise priority queues into one city-level queue."""


class BNode:
    def __init__(self, key, item):
        self.key, self.item = key, item
        self.degree = 0
        self.parent = self.child = self.sibling = None


def _key(c):
    return (c["priority"], -c["id"])


def _link(y, z):
    """Make root y a child of root z (same degree); requires z.key >= y.key."""
    y.parent = z
    y.sibling = z.child
    z.child = y
    z.degree += 1


class BinomialHeap:
    def __init__(self):
        self.head = None                       # linked list of roots, increasing degree
        self.n = 0

    def __len__(self):
        return self.n

    def insert(self, complaint):
        h = BinomialHeap()
        h.head = BNode(_key(complaint), complaint)
        h.n = 1
        self.merge(h)

    def peek(self):
        best, x = None, self.head
        while x:
            if best is None or x.key > best.key:
                best = x
            x = x.sibling
        return best.item if best else None

    def extract_max(self):
        if not self.head:
            return None
        prev = best_prev = None
        best, x = self.head, self.head
        while x:                                           # find root with max key
            if x.key > best.key:
                best, best_prev = x, prev
            prev, x = x, x.sibling
        if best_prev:
            best_prev.sibling = best.sibling               # remove it from root list
        else:
            self.head = best.sibling
        rev, c = None, best.child                          # reverse its children list
        while c:
            nxt = c.sibling
            c.sibling, c.parent = rev, None
            rev, c = c, nxt
        h = BinomialHeap()
        h.head = rev
        self.n -= 1
        self.merge(h)                                      # h.n is 0, so self.n is unchanged
        return best.item

    def merge(self, other):
        """Union of two heaps: merge root lists, then link trees of equal degree."""
        total = self.n + other.n
        self.head = self._union(self.head, other.head)
        self.n = total
        other.head, other.n = None, 0

    @staticmethod
    def _merge_root_lists(a, b):
        dummy = tail = BNode(None, None)
        while a and b:
            if a.degree <= b.degree:
                tail.sibling, a = a, a.sibling
            else:
                tail.sibling, b = b, b.sibling
            tail = tail.sibling
        tail.sibling = a or b
        return dummy.sibling

    def _union(self, a, b):
        head = self._merge_root_lists(a, b)
        if not head:
            return None
        prev, x, nxt = None, head, head.sibling
        while nxt:
            if x.degree != nxt.degree or (nxt.sibling and nxt.sibling.degree == x.degree):
                prev, x = x, nxt                            # move on
            elif x.key >= nxt.key:
                x.sibling = nxt.sibling
                _link(nxt, x)                               # x becomes parent
            else:
                if prev: prev.sibling = nxt
                else: head = nxt
                _link(x, nxt)                               # nxt becomes parent
                x = nxt
            nxt = x.sibling
        return head

    def tree_orders(self):
        out, x = [], self.head
        while x:
            out.append(x.degree)
            x = x.sibling
        return out
