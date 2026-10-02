# if someone were to forget or not take the bottleneck into account, the code will run much slower.

from collections import deque

def max_evacuated(T, S, p, c, roads):
    SOURCE, SINK = 0, T + S + 1
    caps = {}

    def add_edge(u, v, w):
        caps.setdefault(u, {})
        caps[u][v] = caps[u].get(v, 0) + w

    for i in range(1, T + 1):
        add_edge(SOURCE, i, p[i - 1])
    for j in range(1, S + 1):
        add_edge(T + j, SINK, c[j - 1])
    for u, v, w in roads:
        add_edge(u, v, w)

    return ford_fulkerson(caps, SOURCE, SINK)

def ford_fulkerson(caps, s, t):
    for u in list(caps):
        for v in list(caps[u]):
            caps.setdefault(v, {})
            if u not in caps[v]:
                caps[v][u] = 0
    flows = {u: {v: 0 for v in caps[u]} for u in caps}
    flow = 0
    while True:
        path = find_augmenting_path(caps, flows, s, t)
        if path is None:
            break
        flow += push_flow(caps, flows, path)
    return flow

def find_augmenting_path(caps, flows, s, t):
    parents = {s: s}
    queue = deque([s])
    while queue:
        u = queue.popleft()
        for v in caps[u]:
            if v not in parents and flows[u][v] < caps[u][v]:
                parents[v] = u
                queue.append(v)
    if t not in parents:
        return None
    path = [t]
    while path[-1] != s:
        path.append(parents[path[-1]])
    path.reverse()
    return path

def push_flow(caps, flows, path):
    # BUG: pushes a fixed 1 unit instead of the path's true bottleneck capacity
    for u, v in zip(path, path[1:]):
        flows[u][v] += 1
        flows[v][u] -= 1
    return 1


T, S, R = map(int, input().split())
p = list(map(int, input().split()))
c = list(map(int, input().split()))
roads = [tuple(map(int, input().split())) for _ in range(R)]
print(max_evacuated(T, S, p, c, roads))