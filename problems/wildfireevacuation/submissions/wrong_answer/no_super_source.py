# if a user were to not include a super source, which is needed as max-flow algo assumes only one starting and ending point
# but this problem has multiple sources (towns) and sinks (shelters)
from collections import deque

def max_evacuated(T, S, p, c, roads):
    caps = {}

    def add_edge(u, v, w):
        caps.setdefault(u, {})
        caps[u][v] = caps[u].get(v, 0) + w
    # no super source has been initialisde along with the town, shelter and super sink. only the roads are initialised 
    for u, v, w in roads:
        add_edge(u, v, w)

    # uses one town as the source and shelter 1 as the only sink 
    source = 1
    sink = T + 1
    return ford_fulkerson(caps, source, sink)


def ford_fulkerson(caps, s, t):
    # from u->v to v-> u. reverse bc it let a later augmenting path undo flow sent earlier, which is how the algorithm reroutes people
    for u in list(caps):
        for v in list(caps[u]):
            caps.setdefault(v, {})
            if u not in caps[v]:
                caps[v][u] = 0
    # flows[u][v] holds the flow currently sent along u -> v; it starts at 0
    flows = {u: {v: 0 for v in caps[u]} for u in caps}
    flow = 0

    # this keeps finding augmenting paths until none remain
    while True:
        path = find_augmenting_path(caps, flows, s, t)
        if path is None:
            break
        flow += push_flow(caps, flows, path)
    return flow

# uses BFS to find the shortest path from S to T using edges with spare capacity 
def find_augmenting_path(caps, flows, s, t):
    parents = {s: s}
    queue = deque([s])
    while queue:
        u = queue.popleft()
        for v in caps.get(u, {}):
            if v not in parents and flows[u][v] < caps[u][v]:
                parents[v] = u
                queue.append(v)
    if t not in parents:
        return None
     # Walk back from t to s using the parent links, then reverse the list so the path runs from s to t
    path = [t]
    while path[-1] != s:
        path.append(parents[path[-1]])
    path.reverse()
    return path


def push_flow(caps, flows, path):
    #smallest spare capacity of any edge on the path
    bottleneck = float('inf')
    for u, v in zip(path, path[1:]):
        bottleneck = min(bottleneck, caps[u][v] - flows[u][v])
    for u, v in zip(path, path[1:]):
        flows[u][v] += bottleneck
        flows[v][u] -= bottleneck
    return bottleneck

# Read the input: the counts, the town populations, the shelter capacities, then one line per road (start, end, capacity).
T, S, R = map(int, input().split())
p = list(map(int, input().split()))
c = list(map(int, input().split()))
roads = [tuple(map(int, input().split())) for _ in range(R)]
print(max_evacuated(T, S, p, c, roads))