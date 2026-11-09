"""Local standalone simulator of Cellularena (Wood rules: ROOT, BASIC, HARVESTER).

Usage: python3 sim.py [--seed N] [--games N] [--turns 100] [--p0 "python3 bot.py"] [--p1 "python3 bot.py"] [-v]
Score = number of organs at the end; more organs wins.
"""
import argparse
import random
import subprocess
from collections import deque

DIRS = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
COST = {"BASIC": (1, 0, 0, 0), "HARVESTER": (0, 0, 1, 1)}  # A, B, C, D
PROTEINS = "ABCD"
TURN_TIMEOUT = 5.0


class Organ:
    def __init__(self, oid, owner, x, y, typ, d, parent, root):
        self.id, self.owner, self.x, self.y = oid, owner, x, y
        self.type, self.dir, self.parent, self.root = typ, d, parent, root


class Game:
    def __init__(self, seed, start_stock=(2, 0, 1, 1)):
        rnd = random.Random(seed)
        self.w, self.h = rnd.randint(14, 20) * 2 // 2, rnd.randint(7, 10)
        self.w -= self.w % 2
        self.walls, self.prots = set(), {}
        for _ in range(rnd.randint(4, 12)):  # point-symmetric map
            x, y = rnd.randrange(self.w), rnd.randrange(self.h)
            self.walls |= {(x, y), (self.w - 1 - x, y)}
        for _ in range(rnd.randint(4, 8)):
            x, y = rnd.randrange(self.w), rnd.randrange(self.h)
            t = rnd.choice(PROTEINS)
            if (x, y) not in self.walls:
                self.prots[(x, y)] = t
                self.prots[(self.w - 1 - x, y)] = t
        self.organs, self.next_id = {}, 1
        self.stock = [list(start_stock), list(start_stock)]
        y = self.h // 2
        for p, x in ((0, 0), (1, self.w - 1)):
            self.walls.discard((x, y))
            self.prots.pop((x, y), None)
            self.organs[(x, y)] = Organ(self.next_id, p, x, y, "ROOT", "X", 0, self.next_id)
            self.next_id += 1

    def inside(self, c):
        return 0 <= c[0] < self.w and 0 <= c[1] < self.h

    def free(self, c):
        return self.inside(c) and c not in self.walls and c not in self.organs

    def state_lines(self, me):
        ents = [f"{x} {y} WALL -1 0 X 0 0" for x, y in sorted(self.walls)]
        ents += [f"{x} {y} {t} -1 0 X 0 0" for (x, y), t in sorted(self.prots.items())]
        for o in sorted(self.organs.values(), key=lambda o: o.id):
            ents.append(f"{o.x} {o.y} {o.type} {1 if o.owner == me else 0} {o.id} {o.dir} {o.parent} {o.root}")
        return [str(len(ents))] + ents + [" ".join(map(str, self.stock[me])), " ".join(map(str, self.stock[1 - me])), "1"]

    def apply(self, p, cmd):
        """Returns the new organ or None; invalid commands act as WAIT."""
        parts = cmd.split()
        if len(parts) < 5 or parts[0] != "GROW":
            return None
        try:
            oid, tx, ty = int(parts[1]), int(parts[2]), int(parts[3])
        except ValueError:
            return None
        typ, d = parts[4], (parts[5] if len(parts) > 5 else "N")
        src = next((o for o in self.organs.values() if o.id == oid and o.owner == p), None)
        if src is None or typ not in COST or d not in DIRS:
            return None
        if any(s < c for s, c in zip(self.stock[p], COST[typ])):
            return None
        cell = self.first_step(src, (tx, ty))
        if cell is None:
            return None
        for i, c in enumerate(COST[typ]):
            self.stock[p][i] -= c
        if cell in self.prots:  # growing on a source absorbs it
            self.stock[p][PROTEINS.index(self.prots.pop(cell))] += 3
        o = Organ(self.next_id, p, cell[0], cell[1], typ, d if typ == "HARVESTER" else "N", src.id, src.root)
        self.next_id += 1
        return o

    def first_step(self, src, target):
        start = (src.x, src.y)
        if not self.inside(target):
            return None
        prev = {start: None}
        q = deque([start])
        while q:
            c = q.popleft()
            if c == target:
                break
            for dx, dy in DIRS.values():
                nb = (c[0] + dx, c[1] + dy)
                if nb not in prev and (nb == target or self.free(nb)) and self.free(nb):
                    prev[nb] = c
                    q.append(nb)
        if target not in prev:
            return None
        c = target
        while prev[c] != start:
            c = prev[c]
        return c

    def end_turn_harvest(self):
        for p in (0, 1):
            got = set()
            for o in self.organs.values():
                if o.owner == p and o.type == "HARVESTER":
                    dx, dy = DIRS[o.dir]
                    c = (o.x + dx, o.y + dy)
                    if c in self.prots:
                        got.add(c)
            for c in got:
                self.stock[p][PROTEINS.index(self.prots[c])] += 1

    def count(self, p):
        return sum(1 for o in self.organs.values() if o.owner == p)


def play(cmds, seed, turns, verbose):
    g = Game(seed)
    procs = [subprocess.Popen(c, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=None if verbose else subprocess.DEVNULL, text=True) for c in cmds]
    try:
        for p in procs:
            p.stdin.write(f"{g.w} {g.h}\n")
        idle = 0
        for t in range(turns):
            new = []
            for i, p in enumerate(procs):
                p.stdin.write("\n".join(g.state_lines(i)) + "\n")
                p.stdin.flush()
            for i, p in enumerate(procs):
                line = p.stdout.readline().strip()
                if verbose:
                    print(f"t{t} p{i}: {line}")
                new.append((i, line))
            made = 0
            # both grow simultaneously: a contested cell goes to nobody
            res = []
            for i, line in new:
                res.append((i, g.apply(i, line)))
            cells = [(o.x, o.y) for _, o in res if o]
            for i, o in res:
                if o and cells.count((o.x, o.y)) == 1:
                    g.organs[(o.x, o.y)] = o
                    made += 1
            g.end_turn_harvest()
            idle = idle + 1 if made == 0 else 0
            if idle >= 3 and all(not any(s >= 1 for s in st[:1]) for st in g.stock) and t > 0:
                pass
            if idle >= 10:
                break
    finally:
        for p in procs:
            p.kill()
    return g.count(0), g.count(1)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--games", type=int, default=1)
    ap.add_argument("--turns", type=int, default=100)
    ap.add_argument("--p0", default="python3 bot.py")
    ap.add_argument("--p1", default="python3 bot.py")
    ap.add_argument("-v", action="store_true")
    a = ap.parse_args()
    wins = [0, 0, 0]
    for s in range(a.seed, a.seed + a.games):
        s0, s1 = play([a.p0, a.p1], s, a.turns, a.v)
        wins[0 if s0 > s1 else 1 if s1 > s0 else 2] += 1
        print(f"seed {s}: p0={s0} organs, p1={s1} organs")
    print(f"p0 wins {wins[0]}, p1 wins {wins[1]}, draws {wins[2]}")
