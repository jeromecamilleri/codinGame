#!/usr/bin/env python3
"""Version 6: v5 plus blocking of 2- and 3-house move cycles and a safe fallback.

Derived from v5; earlier versions remain preserved.
"""

import sys
from collections import deque

ARMY_CAP = 6
HISTORY_TURNS = 3


def read_ints():
    line = sys.stdin.buffer.readline()
    if not line:
        return None
    values = []
    for token in line.split():
        try:
            values.append(int(token))
        except ValueError:
            continue
    return values


def cycle_blocks(history):
    """Pairs (a, b) meaning a move b->a would close a 2- or 3-house cycle."""
    arcs = set().union(*history) if history else set()
    blocks = set(arcs)
    for a, b in arcs:
        for b2, c in arcs:
            if b2 == b and c != a:
                blocks.add((a, c))
    return blocks


def owners_of(mine, theirs, neighbors):
    owners = [None] * len(mine)
    for node, adjacent in enumerate(neighbors):
        if adjacent and all(mine[n] > theirs[n] for n in adjacent):
            owners[node] = 0
        elif adjacent and all(theirs[n] > mine[n] for n in adjacent):
            owners[node] = 1
        elif mine[node] > theirs[node]:
            owners[node] = 0
        elif theirs[node] > mine[node]:
            owners[node] = 1
    return owners


def distances_from(start, neighbors):
    distances = [None] * len(neighbors)
    first_step = [None] * len(neighbors)
    distances[start] = 0
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for nxt in neighbors[node]:
            if distances[nxt] is not None:
                continue
            distances[nxt] = distances[node] + 1
            first_step[nxt] = nxt if node == start else first_step[node]
            queue.append(nxt)
    return distances, first_step


def choose_triangle_move(mine, theirs, neighbors, triangles, owners,
                         blocked=None, routes=None, last_moves=()):
    """Move one unit toward the best reachable, claimable triangle corner."""
    best = None
    best_score = 0
    blocked = blocked or set()
    routes = routes if routes is not None else {}
    for corners, owner, can_capture in triangles:
        if owner == 0 or not can_capture:
            continue
        owned_count = sum(owners[c] == 0 for c in corners)
        # Work first on triangles already close to completion. Still seed a
        # one-corner triangle when no nearly complete target is available.
        priority = {2: 100, 1: 20, 0: 0}.get(owned_count, 0)
        for target in corners:
            if owners[target] == 0:
                continue
            for source, count in enumerate(mine):
                if count <= 0 or source in blocked:
                    continue
                if source not in routes:
                    routes[source] = distances_from(source, neighbors)
                distances, first_step = routes[source]
                distance = distances[target]
                if distance is None or distance == 0:
                    continue
                step = first_step[target]
                if step in blocked or (step, source) in last_moves:
                    continue
                # Avoid handing an enemy stack an easy kill.
                if theirs[step] >= count + mine[step]:
                    continue
                # Preserve triangles that are already ours, but allow a unit
                # to leave a corner when neighboring ownership still holds it.
                if count == 1 and any(
                    tri_owner == 0 and all(owners[c] == 0 for c in tri_corners)
                    for tri_corners, tri_owner, _ in triangles
                ):
                    after = mine[:]
                    after[source] -= 1
                    after[step] += 1
                    after_owners = owners_of(after, theirs, neighbors)
                    if any(
                        tri_owner == 0
                        and all(owners[c] == 0 for c in tri_corners)
                        and not all(after_owners[c] == 0 for c in tri_corners)
                        for tri_corners, tri_owner, _ in triangles
                    ):
                        continue
                score = priority - distance * 4 - theirs[step] * 12
                # Favor a corner we can occupy immediately and deny the enemy.
                if theirs[target] > mine[target]:
                    score += 12
                score -= target * 0.001 + source * 0.00001
                if score > best_score:
                    best_score = score
                    best = (source, step)
    return best


def choose_approach_move(mine, theirs, neighbors, blocked=None, routes=None,
                         last_moves=()):
    """If no triangle plan is attractive, advance a safe unit toward an enemy."""
    enemies = [i for i, count in enumerate(theirs) if count > 0]
    if not enemies:
        return None
    best = None
    best_score = 0
    blocked = blocked or set()
    routes = routes if routes is not None else {}
    for source, count in enumerate(mine):
        if count <= 0 or source in blocked:
            continue
        if source not in routes:
            routes[source] = distances_from(source, neighbors)
        distances, first_step = routes[source]
        for enemy in enemies:
            distance = distances[enemy]
            if distance is None or distance == 0:
                continue
            step = first_step[enemy]
            if step in blocked or (step, source) in last_moves:
                continue
            if theirs[step] >= count + mine[step]:
                continue
            score = 20 - 4 * distance - 10 * theirs[step]
            score -= source * 0.0001 + step * 0.00001
            if score > best_score:
                best_score, best = score, (source, step)
    return best


def parse_turn(n):
    scores = read_ints()
    if scores is None:
        return None
    mine, theirs = [0] * n, [0] * n
    for _ in range(n):
        row = read_ints()
        if row is None:
            return None
        node, a, b = row
        mine[node], theirs[node] = a, b

    path_row = read_ints()
    if path_row is None:
        return None
    neighbors = [set() for _ in range(n)]
    for _ in range(path_row[0]):
        edge = read_ints()
        if edge is None:
            return None
        a, b = edge
        neighbors[a].add(b)
        neighbors[b].add(a)

    triangle_row = read_ints()
    if triangle_row is None:
        return None
    triangles = []
    for _ in range(triangle_row[0]):
        row = read_ints()
        if row is None:
            return None
        a, b, c, owner, can_capture, _opponent_can = row
        triangles.append(((a, b, c), owner, bool(can_capture)))

    linkable_row = read_ints()
    if linkable_row is None:
        return None
    for _ in range(linkable_row[0]):
        if read_ints() is None:
            return None
    return mine, theirs, neighbors, triangles


def main():
    first = read_ints()
    if not first:
        return
    n = first[0]
    for _ in range(n):
        if read_ints() is None:
            return

    history = deque(maxlen=HISTORY_TURNS)
    while True:
        try:
            state = parse_turn(n)
        except (ValueError, IndexError):
            print("WAIT", flush=True)
            continue
        if state is None:
            return
        try:
            actions, this_moves = decide(state, cycle_blocks(history))
        except Exception:
            actions, this_moves = [], set()
        history.append(this_moves)
        print(";".join(actions) if actions else "WAIT", flush=True)


def decide(state, last_moves):
    mine, theirs, neighbors, triangles = state
    actions = []
    this_moves = set()
    blocked = set()
    routes = {}
    # Move up to three separate units toward a shared triangle objective.
    for _ in range(3):
        owners = owners_of(mine, theirs, neighbors)
        move = choose_triangle_move(
            mine, theirs, neighbors, triangles, owners, blocked, routes, last_moves
        )
        if move is None and not actions:
            move = choose_approach_move(
                mine, theirs, neighbors, blocked, routes, last_moves)
        if move is None:
            break
        source, destination = move
        actions.append(f"MOVE {source} {destination} 1")
        this_moves.add((source, destination))
        blocked.update((source, destination))
        mine[source] -= 1
        mine[destination] += 1
    post_move_owners = owners_of(mine, theirs, neighbors)

    # Improvement 2: turn a surplus of scoring triangles into units, but
    # preserve one triangle and stop at a modest force size.
    owned = [
        (corners, owner) for corners, owner, _ in triangles
        if owner == 0 and all(post_move_owners[c] == 0 for c in corners)
    ]
    unit_total = sum(mine)
    if unit_total < ARMY_CAP and (len(owned) > 1 or (unit_total < 4 and len(owned) > 0)):
        corners, _ = max(
            owned,
            key=lambda item: (sum(len(neighbors[n]) for n in item[0]),
                              -sum(theirs[n] for n in item[0])),
        )
        a, b, c = corners
        actions.append(f"SPAWN {a} {b} {c}")

    return actions, this_moves


if __name__ == "__main__":
    main()
