import sys
from math import hypot


def err(*a):
    print(*a, file=sys.stderr, flush=True)


def orient(a, b, c):
    v = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return (v > 0) - (v < 0)


def seg_cross(a, b, c, d):
    return orient(a, b, c) * orient(a, b, d) < 0 and orient(c, d, a) * orient(c, d, b) < 0


def on_seg(a, b, p):
    return abs(hypot(p[0] - a[0], p[1] - a[1]) + hypot(b[0] - p[0], b[1] - p[1]) - hypot(b[0] - a[0], b[1] - a[1])) < 1e-7


pos = {}
kind = {}      # id -> 'L' or module type (int)
ltypes = {}    # landing id -> set of astronaut types
tubes = set()
deg = {}
pod_id = 0
parent = {}


def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def dist(a, b):
    return hypot(pos[a][0] - pos[b][0], pos[a][1] - pos[b][1])


def cost(a, b):
    return int(dist(a, b) * 10)


def valid(a, b):
    if a == b or (min(a, b), max(a, b)) in tubes:
        return False
    if deg.get(a, 0) >= 5 or deg.get(b, 0) >= 5:
        return False
    for k, p in pos.items():
        if k != a and k != b and on_seg(pos[a], pos[b], p):
            return False
    for (c, d) in tubes:
        if seg_cross(pos[a], pos[b], pos[c], pos[d]):
            return False
    return True


def comp_types(root):
    return {kind[k] for k in pos if kind[k] != 'L' and find(k) == root}


def main():
    global pod_id
    while True:
        resources = int(input())
        for _ in range(int(input())):
            input()
        for _ in range(int(input())):
            input()
        new_l = []
        for _ in range(int(input())):
            t = input().split()
            if t[0] == '0':
                i = int(t[1])
                pos[i] = (int(t[2]), int(t[3]))
                kind[i] = 'L'
                ltypes[i] = set(map(int, t[5:]))
                new_l.append(i)
            else:
                i = int(t[1])
                pos[i] = (int(t[2]), int(t[3]))
                kind[i] = int(t[0])
            parent[i] = i
        actions = []
        todo = [l for l in ltypes if find(l) == l and not any(find(l) == find(m) and kind[m] in ltypes[l] for m in pos if kind[m] != 'L')]
        todo.sort(key=lambda l: -len(ltypes[l]))
        for l in todo:
            for _ in range(3):
                best = None
                for b in pos:
                    if b == l:
                        continue
                    r = find(b)
                    if kind[b] != 'L' and kind[b] in ltypes[l]:
                        ok = True
                    elif r != find(l) and comp_types(r) & ltypes[l]:
                        ok = True
                    else:
                        ok = False
                    if not ok or not valid(l, b):
                        continue
                    c = cost(l, b)
                    if c + 1000 > resources:
                        continue
                    if best is None or c < best[0]:
                        best = (c, b)
                if best is None:
                    break
                c, b = best
                pod_id += 1
                actions.append("TUBE %d %d" % (l, b))
                actions.append("POD %d %d %d %d" % (pod_id, l, b, l))
                resources -= c + 1000
                tubes.add((min(l, b), max(l, b)))
                deg[l] = deg.get(l, 0) + 1
                deg[b] = deg.get(b, 0) + 1
                parent[find(l)] = find(b)
                if any(kind[m] in ltypes[l] for m in pos if kind[m] != 'L' and find(m) == find(l)):
                    break
        err("ressources restantes:", resources, "| actions:", len(actions))
        print(";".join(actions) if actions else "WAIT", flush=True)


main()
