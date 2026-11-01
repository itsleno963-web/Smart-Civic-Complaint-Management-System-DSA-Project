"""Automated tests - one per test case listed in Section 12 of the report.
Run:  python -m unittest tests.test_all -v   (from the project folder)"""
import json, os, unittest
from dsa.binary_tree import BinarySearchTree
from dsa.avl_tree import AVLTree
from dsa.max_heap import MaxHeap
from dsa.binomial_heap import BinomialHeap
from dsa.graph import LocationGraph
from dsa.knapsack import select_complaints
from dsa.route_planner import plan_route
from itertools import permutations

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = json.load(open(os.path.join(BASE, "data", "complaints.json")))


class TestSystem(unittest.TestCase):
    def test1_insert_and_search(self):
        t = AVLTree()
        for c in DATA: t.insert(c["id"], c)
        self.assertEqual(t.search(105)["category"], "Drainage")
        self.assertIsNone(t.search(999))

    def test2_avl_stays_balanced_on_sorted_input(self):
        avl, bst = AVLTree(), BinarySearchTree()
        for i in range(1, 64): avl.insert(i, i); bst.insert(i, i)
        self.assertTrue(avl.is_balanced())
        self.assertEqual(bst.height(), 63)
        self.assertLessEqual(avl.height(), 7)

    def test3_traversal_lists_all_once(self):
        t = AVLTree()
        for c in DATA: t.insert(c["id"], c)
        ids = [c["id"] for c in t.inorder()]
        self.assertEqual(ids, sorted(c["id"] for c in DATA))
        for order in (t.preorder(), t.postorder(), t.level_order()):
            self.assertEqual(len(order), len(DATA))

    def test4_heap_returns_highest_priority_first(self):
        h = MaxHeap()
        for c in DATA: h.push(c)
        pr = []
        while len(h): pr.append(h.pop()["priority"])
        self.assertEqual(pr, sorted(pr, reverse=True))

    def test5_binomial_merge(self):
        a, b = BinomialHeap(), BinomialHeap()
        for c in DATA[:5]: a.insert(c)
        for c in DATA[5:]: b.insert(c)
        a.merge(b)
        self.assertEqual(len(a), len(DATA))
        out = []
        while len(a): out.append(a.extract_max()["priority"])
        self.assertEqual(out, sorted((c["priority"] for c in DATA), reverse=True))

    def test6_graph_neighbours(self):
        g = LocationGraph.from_json(os.path.join(BASE, "data", "locations.json"))
        self.assertEqual(set(g.neighbours("Office")), {"Sector 5", "Market"})

    def test7_knapsack_within_capacity_and_optimal(self):
        best, chosen = select_complaints(DATA, 8)
        self.assertLessEqual(sum(c["effort"] for c in chosen), 8)
        self.assertEqual(best, sum(c["priority"] for c in chosen))
        # brute-force check of optimality
        from itertools import combinations
        bf = max(sum(c["priority"] for c in comb)
                 for r in range(len(DATA) + 1) for comb in combinations(DATA, r)
                 if sum(c["effort"] for c in comb) <= 8)
        self.assertEqual(best, bf)

    def test8_route_is_minimum_cost(self):
        g = LocationGraph.from_json(os.path.join(BASE, "data", "locations.json"))
        d = g.shortest_distances()
        stops = ["Sector 12", "Market", "Station"]
        route, cost, _ = plan_route(d, stops, "Office")
        self.assertEqual(sorted(route[1:-1]), sorted(stops))
        brute = min(d["Office"][p[0]] + sum(d[p[i]][p[i+1]] for i in range(len(p)-1)) + d[p[-1]]["Office"]
                    for p in permutations(stops))
        self.assertEqual(cost, brute)


if __name__ == "__main__":
    unittest.main()
