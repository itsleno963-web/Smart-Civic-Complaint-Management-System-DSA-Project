"""Module 1 (Trees): AVL Tree - a self-balancing BST.
Balance factor of every node is kept between -1 and +1 using rotations."""
from dsa.binary_tree import BinarySearchTree, Node


def _h(n):
    return n.height if n else 0


def _update(n):
    n.height = 1 + max(_h(n.left), _h(n.right))


def _balance(n):
    return _h(n.left) - _h(n.right) if n else 0


def _rotate_right(y):          # LL case
    x = y.left
    y.left, x.right = x.right, y
    _update(y); _update(x)
    return x


def _rotate_left(x):           # RR case
    y = x.right
    x.right, y.left = y.left, x
    _update(x); _update(y)
    return y


class AVLTree(BinarySearchTree):
    def __init__(self):
        super().__init__()
        self.rotations = 0     # counted so the demo can show rotations happening

    def _insert(self, node, key, data):
        if node is None:
            self.size += 1
            return Node(key, data)
        if key < node.key:
            node.left = self._insert(node.left, key, data)
        elif key > node.key:
            node.right = self._insert(node.right, key, data)
        else:
            node.data = data
            return node
        return self._rebalance(node)

    def _rebalance(self, node):
        _update(node)
        bf = _balance(node)
        if bf > 1:                                   # left heavy
            if _balance(node.left) < 0:              # LR case
                node.left = _rotate_left(node.left); self.rotations += 1
            self.rotations += 1
            return _rotate_right(node)               # LL case
        if bf < -1:                                  # right heavy
            if _balance(node.right) > 0:             # RL case
                node.right = _rotate_right(node.right); self.rotations += 1
            self.rotations += 1
            return _rotate_left(node)                # RR case
        return node

    def is_balanced(self):
        def check(n):
            if n is None:
                return True
            return abs(_balance(n)) <= 1 and check(n.left) and check(n.right)
        return check(self.root)
