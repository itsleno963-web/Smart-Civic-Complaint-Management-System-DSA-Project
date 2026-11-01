"""Module 3 (Dynamic Programming): 0/1 Knapsack.
Choose which complaints to resolve in one day.
weight = effort (hours), value = priority, capacity = working hours available."""


def select_complaints(complaints, capacity):
    n = len(complaints)
    # dp[i][w] = best total priority using first i complaints with w hours
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        c = complaints[i - 1]
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]                           # skip complaint
            if c["effort"] <= w:                              # or take it
                dp[i][w] = max(dp[i][w], dp[i - 1][w - c["effort"]] + c["priority"])
    # trace back which complaints were chosen
    chosen, w = [], capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            chosen.append(complaints[i - 1])
            w -= complaints[i - 1]["effort"]
    chosen.reverse()
    return dp[n][capacity], chosen


def greedy_by_priority(complaints, capacity):
    """For comparison only: just take highest priorities while they fit."""
    total, used, chosen = 0, 0, []
    for c in sorted(complaints, key=lambda c: -c["priority"]):
        if used + c["effort"] <= capacity:
            chosen.append(c); used += c["effort"]; total += c["priority"]
    return total, chosen
