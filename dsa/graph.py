"""Module 2 (Graphs): Location graph using an adjacency list.
Vertices = locations, edges = roads (weighted by distance in km).
Also provides BFS and Floyd-Warshall (all-pairs shortest distances)."""
import json
from collections import deque

INF = float("inf")


class LocationGraph:
    def __init__(self):
        self.adj = {}                      # adjacency list: {location: {neighbour: km}}

    def add_location(self, name):
        self.adj.setdefault(name, {})

    def add_road(self, a, b, km):
        self.add_location(a); self.add_location(b)
        self.adj[a][b] = km
        self.adj[b][a] = km                # roads are two-way

    @classmethod
    def from_json(cls, path):
        with open(path) as f:
            d = json.load(f)
        g = cls()
        for loc in d["locations"]:
            g.add_location(loc)
        for a, b, km in d["roads"]:
            g.add_road(a, b, km)
        return g

    def neighbours(self, name):
        return dict(self.adj.get(name, {}))

    def bfs(self, start):
        """Breadth-first traversal: visits nearest (by hops) locations first."""
        seen, order, q = {start}, [], deque([start])
        while q:
            u = q.popleft()
            order.append(u)
            for v in sorted(self.adj[u]):
                if v not in seen:
                    seen.add(v); q.append(v)
        return order

    def shortest_distances(self):
        """Floyd-Warshall: shortest distance between every pair of locations."""
        names = list(self.adj)
        d = {u: {v: (0 if u == v else self.adj[u].get(v, INF)) for v in names} for u in names}
        for k in names:
            for i in names:
                for j in names:
                    if d[i][k] + d[k][j] < d[i][j]:
                        d[i][j] = d[i][k] + d[k][j]
        return d
