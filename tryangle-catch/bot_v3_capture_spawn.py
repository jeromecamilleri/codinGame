#!/usr/bin/env python3
"""Version 3: focus moves on claimable triangles, then reinforce from triangles.

History: bot.py (triangle planner/path builder) and bot_simple.py (safe approach)
are retained unchanged as earlier versions.
"""

import sys
from collections import deque


def read_ints():
    line = sys.stdin.buffer.readline()
    if not line:
        return None
    try:
        return [int(value) for value in line.split()]
    except ValueError:
        return None


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


def choose_triangle_move(mine, theirs, neighbors, triangles, owners):
    """Move one unit toward the best reachable, claimable triangle corner."""
    best = None
    best_score = 0
    for corners, owner, can_capture in triangles:
        if owner == 0 or not can_capture:
            continue
        owned_count = sum(owners[c] == 0 for c in corners)
        # Work first on triangles already close to completion. Still seed a
        # one-corner triangle when no nearly complete target is available.
        priority = {2: 100, 1: 35, 0: 5}.get(owned_count, 0)
        for target in corners:
            if owners[target] == 0:
                continue
            for source, count in enumerate(mine):
                if count <= 0:
                    continue
                distances, first_step = distances_from(source, neighbors)
                distance = distances[target]
                if distance is None or distance == 0:
                    continue
                step = first_step[target]
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


def choose_approach_move(mine, theirs, neighbors):
    """If no triangle plan is attractive, advance a safe unit toward an enemy."""
    enemies = [i for i, count in enumerate(theirs) if count > 0]
    if not enemies:
        return None
    best = None
    best_score = 0
    for source, count in enumerate(mine):
        if count <= 0:
            continue
        distances, first_step = distances_from(source, neighbors)
        for enemy in enemies:
            distance = distances[enemy]
            if distance is None or distance == 0:
                continue
            step = first_step[enemy]
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

    while True:
        state = parse_turn(n)
        if state is None:
            return
        mine, theirs, neighbors, triangles = state
        owners = owners_of(mine, theirs, neighbors)

        actions = []
        # Improvement 1: deliberately complete available triangle captures.
        move = choose_triangle_move(mine, theirs, neighbors, triangles, owners)
        if move is None:
            move = choose_approach_move(mine, theirs, neighbors)
        if move is not None:
            actions.append(f"MOVE {move[0]} {move[1]} 1")
            mine[move[0]] -= 1
            mine[move[1]] += 1
        post_move_owners = owners_of(mine, theirs, neighbors)

        # Improvement 2: turn a surplus of scoring triangles into units, but
        # preserve one triangle and stop at a modest force size.
        owned = [
            (corners, owner) for corners, owner, _ in triangles
            if owner == 0 and all(post_move_owners[c] == 0 for c in corners)
        ]
        if sum(mine) < 8 and len(owned) > 1:
            corners, _ = max(
                owned,
                key=lambda item: (sum(len(neighbors[n]) for n in item[0]),
                                  -sum(theirs[n] for n in item[0])),
            )
            a, b, c = corners
            actions.append(f"SPAWN {a} {b} {c}")

        print(";".join(actions) if actions else "WAIT", flush=True)


if __name__ == "__main__":
    main()
