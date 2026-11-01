"""Smart Civic Complaint Management System  -  DSA-II PBL (SDG 11)
Terminal prototype.  Run:  python main.py          (interactive menu)
                           python main.py --demo   (runs every feature once)
"""
import json
import os
import sys

from dsa.binary_tree import BinarySearchTree
from dsa.avl_tree import AVLTree
from dsa.max_heap import MaxHeap
from dsa.binomial_heap import BinomialHeap
from dsa.graph import LocationGraph
from dsa.knapsack import select_complaints, greedy_by_priority
from dsa.route_planner import plan_route

BASE = os.path.dirname(os.path.abspath(__file__))
LINE = "=" * 78


class CivicSystem:
    def __init__(self):
        with open(os.path.join(BASE, "data", "complaints.json")) as f:
            self.complaints = json.load(f)
        self.tree = AVLTree()                       # Module 1: store / search
        self.heap = MaxHeap()                       # Module 1: priority queue
        self.graph = LocationGraph.from_json(       # Module 2: locations
            os.path.join(BASE, "data", "locations.json"))
        for c in self.complaints:
            self.tree.insert(c["id"], c)
            self.heap.push(c)

    # ---------- helpers ----------
    def add_complaint(self, c):
        self.complaints.append(c)
        self.tree.insert(c["id"], c)
        self.heap.push(c)

    def pending(self):
        return [c for c in self.complaints if c["status"] != "Resolved"]


def show(complaints, title=None):
    if title:
        print(f"\n{title}")
    print("-" * 78)
    print(f"{'ID':<5}{'CATEGORY':<10}{'LOCATION':<11}{'PRIORITY':<9}{'EFFORT':<7}{'STATUS':<12}DESCRIPTION")
    print("-" * 78)
    for c in complaints:
        print(f"{c['id']:<5}{c['category']:<10}{c['location']:<11}{c['priority']:<9}"
              f"{c['effort']:<7}{c['status']:<12}{c['description'][:28]}")
    print("-" * 78)


# ---------------- feature functions ----------------
def f_view_all(s):
    show(s.tree.inorder(), "All complaints (in-order traversal of AVL tree = sorted by ID)")


def f_search(s, cid=None):
    if cid is None:
        cid = int(input("Enter complaint ID: "))
    c = s.tree.search(cid)
    print(f"\nSearch result for ID {cid}:")
    show([c]) if c else print("  Complaint not found.")


def f_add(s):
    c = {"id": int(input("ID: ")), "category": input("Category: "), "location": input("Location: "),
         "date": input("Date (YYYY-MM-DD): "), "status": "Pending",
         "priority": int(input("Priority (1-10): ")), "effort": int(input("Effort (hours): ")),
         "description": input("Description: ")}
    s.add_complaint(c)
    print("Complaint added to AVL tree and priority heap.")


def f_traversals(s):
    print("\nTree traversals (complaint IDs):")
    ids = lambda lst: [c["id"] for c in lst]
    print("  Pre-order  :", ids(s.tree.preorder()))
    print("  In-order   :", ids(s.tree.inorder()))
    print("  Post-order :", ids(s.tree.postorder()))
    print("  Level-order:", ids(s.tree.level_order()))
    print(f"  Tree height: {s.tree.height()}   Balanced: {s.tree.is_balanced()}")


def f_bst_vs_avl(s):
    print("\nBST vs AVL: inserting IDs 1..15 in sorted order")
    bst, avl = BinarySearchTree(), AVLTree()
    for i in range(1, 16):
        bst.insert(i, {"id": i}); avl.insert(i, {"id": i})
    print(f"  Plain BST height : {bst.height():>2}   (skewed - behaves like a linked list, search O(n))")
    print(f"  AVL tree height  : {avl.height():>2}   (balanced after {avl.rotations} rotations, search O(log n))")


def f_heap(s):
    print("\nMax Heap: handling complaints in priority order (top 5)")
    h = MaxHeap()
    for c in s.pending():
        h.push(c)
    for rank in range(1, 6):
        c = h.pop()
        print(f"  {rank}. ID {c['id']}  priority {c['priority']}  {c['category']:<9} {c['location']:<10} {c['description']}")


def f_binomial(s):
    print("\nBinomial Heap: merging department priority queues")
    depts = {}
    for c in s.pending():
        depts.setdefault(c["category"], BinomialHeap()).insert(c)
    for name, h in depts.items():
        top = h.peek()
        print(f"  {name:<9} heap: {len(h)} complaints, top = ID {top['id']} (priority {top['priority']}), tree orders {h.tree_orders()}")
    city = BinomialHeap()
    for h in depts.values():
        city.merge(h)
    print(f"  --> Merged city-level heap: {len(city)} complaints, tree orders {city.tree_orders()}")
    print("  Highest-priority complaints city-wide:")
    for i in range(1, 4):
        c = city.extract_max()
        print(f"     {i}. ID {c['id']}  priority {c['priority']}  {c['category']:<9} {c['location']}")


def f_graph(s, loc=None):
    if loc is None:
        loc = input("Enter location: ")
    print(f"\nLocation graph (adjacency list):")
    for u, nb in s.graph.adj.items():
        print(f"  {u:<10} -> {', '.join(f'{v} ({km} km)' for v, km in nb.items())}")
    if loc in s.graph.adj:
        print(f"\n  Neighbours of {loc}: {s.graph.neighbours(loc)}")
        print(f"  BFS order from {loc}: {s.graph.bfs(loc)}")
    else:
        print("  Unknown location.")


def f_knapsack(s, capacity=None):
    if capacity is None:
        capacity = int(input("Working hours available today: "))
    pend = s.pending()
    best, chosen = select_complaints(pend, capacity)
    gbest, gchosen = greedy_by_priority(pend, capacity)
    print(f"\n0/1 Knapsack (Dynamic Programming) - capacity {capacity} hours")
    show(chosen, f"Optimal selection: total priority = {best}, hours used = {sum(c['effort'] for c in chosen)}")
    print(f"For comparison, greedy 'highest priority first' gives total priority = {gbest}")
    return chosen


def f_route(s, chosen=None):
    if chosen is None:
        chosen = f_knapsack(s, 8)
    stops = [c["location"] for c in chosen]
    dist = s.graph.shortest_distances()                 # Floyd-Warshall
    route, cost, st = plan_route(dist, stops, "Office")
    print(f"\nRoute planning (Backtracking + Branch and Bound) for stops: {sorted(set(stops))}")
    print("  Best route :", " -> ".join(route))
    print(f"  Total distance: {cost} km")
    print(f"  Search nodes explored: {st['explored']}, branches pruned: {st['pruned']}")


MENU = """
{line}
        SMART CIVIC COMPLAINT MANAGEMENT SYSTEM
{line}
 1. View all complaints (AVL in-order traversal)
 2. Search complaint by ID (AVL search)
 3. Add new complaint
 4. Tree traversals (pre / in / post / level order)
 5. BST vs AVL height comparison
 6. Priority processing (Max Heap)
 7. Merge department queues (Binomial Heap)
 8. Location graph and neighbours (Adjacency List, BFS)
 9. Select complaints for today's capacity (Knapsack - DP)
10. Plan field-worker route (Backtracking + Branch and Bound)
 0. Exit
{line}"""


def menu():
    s = CivicSystem()
    actions = {"1": f_view_all, "2": f_search, "3": f_add, "4": f_traversals, "5": f_bst_vs_avl,
               "6": f_heap, "7": f_binomial, "8": f_graph, "9": f_knapsack, "10": f_route}
    while True:
        print(MENU.format(line=LINE))
        ch = input("Choose an option (0-10): ").strip()
        if ch == "0":
            print("Goodbye!"); return
        try:
            actions.get(ch, lambda x: print("Invalid option."))(s)
        except ValueError:
            print("Invalid input, please try again.")


def demo():
    s = CivicSystem()
    print(LINE); print("   SMART CIVIC COMPLAINT MANAGEMENT SYSTEM - DEMO RUN"); print(LINE)
    print("\n### MODULE 1: TREES ###")
    f_view_all(s); f_search(s, 105); f_search(s, 999); f_traversals(s); f_bst_vs_avl(s); f_heap(s)
    print("\n### MODULE 2: GRAPHS ###"); f_graph(s, "Market")
    print("\n### MODULE 3: DYNAMIC PROGRAMMING ###"); chosen = f_knapsack(s, 8)
    print("\n### MODULE 4: BACKTRACKING, BRANCH AND BOUND ###"); f_route(s, chosen)
    print("\n### MODULE 5: ADVANCED DATA STRUCTURES (BINOMIAL HEAP) ###"); f_binomial(s)


if __name__ == "__main__":
    demo() if "--demo" in sys.argv else menu()
