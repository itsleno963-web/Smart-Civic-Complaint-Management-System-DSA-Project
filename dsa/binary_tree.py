"""Module 1 (Trees): Binary Search Tree with traversals.
Complaints are stored using the complaint ID as the key."""
from collections import deque


class Node:
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.left = None
        self.right = None
        self.height = 1          # used by the AVL subclass


class BinarySearchTree:
    def __init__(self):
        self.root = None
        self.size = 0

    # ---------- insertion / search ----------
    def insert(self, key, data):
        self.root = self._insert(self.root, key, data)

    def _insert(self, node, key, data):
        if node is None:
            self.size += 1
            return Node(key, data)
        if key < node.key:
            node.left = self._insert(node.left, key, data)
        elif key > node.key:
            node.right = self._insert(node.right, key, data)
        else:
            node.data = data                     # same ID -> update record
        return node

    def search(self, key):
        node = self.root
        while node:
            if key == node.key:
                return node.data
            node = node.left if key < node.key else node.right
        return None

    # ---------- traversals ----------
    def inorder(self):
        out = []
        def go(n):
            if n:
                go(n.left); out.append(n.data); go(n.right)
        go(self.root)
        return out

    def preorder(self):
        out = []
        def go(n):
            if n:
                out.append(n.data); go(n.left); go(n.right)
        go(self.root)
        return out

    def postorder(self):
        out = []
        def go(n):
            if n:
                go(n.left); go(n.right); out.append(n.data)
        go(self.root)
        return out

    def level_order(self):
        out, q = [], deque([self.root] if self.root else [])
        while q:
            n = q.popleft()
            out.append(n.data)
            if n.left: q.append(n.left)
            if n.right: q.append(n.right)
        return out

    def height(self):
        def h(n):
            return 0 if n is None else 1 + max(h(n.left), h(n.right))
        return h(self.root)
