# Smart Civic Complaint Management System

**DSA-II PBL Project (CCSE0301) | SDG 11 – Sustainable Cities**
B.Tech CSE-A, NIET Greater Noida | Faculty: Mr. Shamshad Ali

A terminal-based Python prototype that organises, prioritises and routes public
utility complaints (road, water, streetlight, waste, drainage) using Data Structures
and Algorithms. It needs only Python 3.8+ and no external libraries.

## Features and DSA concepts

| Module | Concept | File | Used for |
|---|---|---|---|
| 1 | Binary Search Tree, traversals, AVL Tree, Max Heap | `dsa/binary_tree.py`, `dsa/avl_tree.py`, `dsa/max_heap.py` | Storing and searching complaints, priority handling |
| 2 | Graphs (adjacency list, BFS, Floyd-Warshall) | `dsa/graph.py` | Location connections and distances |
| 3 | Dynamic Programming (0/1 Knapsack) | `dsa/knapsack.py` | Choosing complaints that fit today's working hours |
| 4 | Backtracking, Branch and Bound | `dsa/route_planner.py` | Minimum-distance route for a field worker |
| 5 | Advanced Data Structures (Binomial Heap) | `dsa/binomial_heap.py` | Merging department-wise priority queues |

## How to run

```bash
python main.py            # interactive menu (options 1-10)
python main.py --demo     # runs every feature once
python -m unittest tests.test_all -v    # 8 automated tests
```

## Menu options

1. View all complaints (AVL in-order traversal)
2. Search complaint by ID
3. Add new complaint
4. Tree traversals (pre / in / post / level order)
5. BST vs AVL height comparison
6. Priority processing (Max Heap)
7. Merge department queues (Binomial Heap)
8. Location graph and neighbours (Adjacency List, BFS)
9. Select complaints for today's capacity (Knapsack – DP)
10. Plan field-worker route (Backtracking + Branch and Bound)

## Sample output

```
BST vs AVL: inserting IDs 1..15 in sorted order
  Plain BST height : 15   (skewed - behaves like a linked list, search O(n))
  AVL tree height  :  4   (balanced after 11 rotations, search O(log n))

0/1 Knapsack (Dynamic Programming) - capacity 8 hours
Optimal selection: total priority = 27, hours used = 8
For comparison, greedy 'highest priority first' gives total priority = 18

Route planning (Backtracking + Branch and Bound)
  Best route : Office -> Market -> Station -> Park Road -> Sector 12 -> Office
  Total distance: 25 km
```

Full output of the demo run is in `demo_output.txt`.

## Data

Sample data only: `data/complaints.json` (10 complaints) and
`data/locations.json` (6 locations, 8 roads).

## Limitations

Academic prototype: small sample dataset, no database, no web or mobile interface.

## Author

Anmol | ERP: 0251CSE081 | Roll No: 2501330100078