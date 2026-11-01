"""Module 4 (Backtracking, Branch and Bound): route planning (TSP style).
A field worker starts at the Office, visits every selected complaint location
exactly once and returns. Backtracking builds routes one stop at a time;
Branch and Bound prunes any partial route whose lower bound >= best cost found."""


def plan_route(dist, stops, start="Office"):
    stops = sorted(set(stops) - {start})
    best = {"cost": float("inf"), "route": None}
    stats = {"explored": 0, "pruned": 0}

    def lower_bound(cost, current, remaining):
        # cost so far + cheapest way out of the current stop and of every remaining stop
        lb = cost
        if remaining:
            lb += min(dist[current][r] for r in remaining)
            for r in remaining:
                others = [x for x in remaining if x != r] + [start]
                lb += min(dist[r][o] for o in others)
        else:
            lb += dist[current][start]
        return lb

    def solve(current, remaining, cost, path):
        stats["explored"] += 1
        if not remaining:                                    # all visited -> return home
            total = cost + dist[current][start]
            if total < best["cost"]:
                best["cost"], best["route"] = total, path + [start]
            return
        for nxt in remaining:                                # branch
            new_cost = cost + dist[current][nxt]
            rest = [r for r in remaining if r != nxt]
            if lower_bound(new_cost, nxt, rest) >= best["cost"]:   # bound
                stats["pruned"] += 1
                continue
            solve(nxt, rest, new_cost, path + [nxt])         # backtrack after return

    solve(start, stops, 0, [start])
    return best["route"], best["cost"], stats
