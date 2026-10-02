# if someone were to forget or not take the bottleneck into account, the code will run much slower.

from collections import deque

def max_evacuated(T, S, p, c, roads):
    SOURCE, SINK = 0, T + S + 1
    caps = {}

     # small helper function so that if there are duplicated roads between two locations, this will sum their capacities instead of overwriting each other   
    def add_edge(u, v, w):
        caps.setdefault(u, {})
        caps[u][v] = caps[u].get(v, 0) + w

     # super-source to each town: capacity is the town's population, so that no town can send out more people than it has
    for i in range(1, T + 1):
        add_edge(SOURCE, i, p[i - 1])
    # this shows that each shelter is the super-sink. no shelter can take in more people than it can fit.
    for j in range(1, S + 1):
        add_edge(T + j, SINK, c[j - 1])
     # this creates the onee-way roads: an edge from u to v that can carry at most w people
    for u, v, w in roads:
        add_edge(u, v, w)

    return ford_fulkerson(caps, SOURCE, SINK)

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
        for v in caps[u]:
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

def push_flow(caps, flows, path): #pushes a fixed 1 unit instead of the path's true bottleneck capacity
    #smallest spare capacity of any edge on the path
    for u, v in zip(path, path[1:]):
        flows[u][v] += 1
        flows[v][u] -= 1
    return 1

# Read the input: the counts, the town populations, the shelter capacities, then one line per road (start, end, capacity).
T, S, R = map(int, input().split())
p = list(map(int, input().split()))
c = list(map(int, input().split()))
roads = [tuple(map(int, input().split())) for _ in range(R)]
print(max_evacuated(T, S, p, c, roads))