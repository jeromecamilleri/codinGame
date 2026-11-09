import sys
from collections import deque

DIRS = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
PROTEINS = {"A", "B", "C", "D"}

width, height = map(int, input().split())

while True:
    n = int(input())
    walls, prots, mine, occupied = set(), {}, {}, set()
    for _ in range(n):
        p = input().split()
        x, y, t, owner, oid = int(p[0]), int(p[1]), p[2], int(p[3]), int(p[4])
        if t == "WALL":
            walls.add((x, y))
            occupied.add((x, y))
        elif t in PROTEINS:
            prots[(x, y)] = t
        else:
            occupied.add((x, y))
            if owner == 1:
                mine[(x, y)] = oid
    stock = list(map(int, input().split()))
    input()
    for _ in range(int(input())):
        # BFS from all my organs to the nearest protein source
        prev = {c: None for c in mine}
        q = deque(mine)
        goal = None
        while q:
            c = q.popleft()
            if c in prots and c not in mine:
                goal = c
                break
            for dx, dy in DIRS.values():
                nb = (c[0] + dx, c[1] + dy)
                if 0 <= nb[0] < width and 0 <= nb[1] < height and nb not in prev and nb not in occupied:
                    prev[nb] = c
                    q.append(nb)
        if goal is None:
            # no protein left: just expand into any free adjacent cell
            for c, oid in mine.items():
                for dx, dy in DIRS.values():
                    nb = (c[0] + dx, c[1] + dy)
                    if 0 <= nb[0] < width and 0 <= nb[1] < height and nb not in occupied:
                        goal = nb
                        print("GROW", oid, nb[0], nb[1], "BASIC")
                        break
                if goal:
                    break
            if goal is None:
                print("WAIT")
            continue
        path = [goal]
        while prev[path[-1]] is not None:
            path.append(prev[path[-1]])
        path.reverse()  # path[0] is my organ, path[-1] is the protein
        if len(path) >= 3 and len(path) == 3 and stock[2] >= 1 and stock[3] >= 1:
            # free cell next to the protein: harvester facing it
            cell = path[1]
            d = next(k for k, (dx, dy) in DIRS.items() if (cell[0] + dx, cell[1] + dy) == goal)
            print("GROW", mine[path[0]], cell[0], cell[1], "HARVESTER", d)
            continue
        step = path[1]
        print("GROW", mine[path[0]], step[0], step[1], "BASIC")
