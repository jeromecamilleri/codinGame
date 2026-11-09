#!/usr/bin/env python3
"""Starter agent for CodinGame Fall Challenge 2026 (TryAngle Catch), Bronze."""

import itertools
import sys
from collections import deque


def read_ints():
    line = sys.stdin.buffer.readline()
    if not line:
        return None
    return [int(x) for x in line.split()]


def bfs_all(adjacency):
    n = len(adjacency)
    distances = [[n + 1] * n for _ in range(n)]
    for start in range(n):
        distances[start][start] = 0
        q = deque([start])
        while q:
            u = q.popleft()
            nd = distances[start][u] + 1
            for v in adjacency[u]:
                if distances[start][v] > nd:
                    distances[start][v] = nd
                    q.append(v)
    return distances


def house_owners(my_units, opp_units, adjacency):
    owners = [None] * len(my_units)
    for u, neighbors in enumerate(adjacency):
        if neighbors and all(my_units[v] > opp_units[v] for v in neighbors):
            owners[u] = 0
        elif neighbors and all(opp_units[v] > my_units[v] for v in neighbors):
            owners[u] = 1
        elif my_units[u] > opp_units[u]:
            owners[u] = 0
        elif opp_units[u] > my_units[u]:
            owners[u] = 1
    return owners


def point_inside_triangle(p, a, b, c):
    def cross(u, v, w):
        return (v[0] - u[0]) * (w[1] - u[1]) - (v[1] - u[1]) * (w[0] - u[0])

    s1 = cross(a, b, p)
    s2 = cross(b, c, p)
    s3 = cross(c, a, p)
    return (s1 > 0 and s2 > 0 and s3 > 0) or (s1 < 0 and s2 < 0 and s3 < 0)


def projected_owners(targets, opp_units, adjacency):
    planned = [0] * len(adjacency)
    for node in targets:
        planned[node] += 1
    owners = [None] * len(adjacency)
    for u, neighbors in enumerate(adjacency):
        if neighbors and all(planned[v] > opp_units[v] for v in neighbors):
            owners[u] = 0
        elif neighbors and all(opp_units[v] > planned[v] for v in neighbors):
            owners[u] = 1
        elif planned[u] > opp_units[u]:
            owners[u] = 0
        elif opp_units[u] > planned[u]:
            owners[u] = 1
    return planned, owners


def plan_score(targets, triangles, opp_units, adjacency):
    planned, owners = projected_owners(targets, opp_units, adjacency)
    score = 0.0
    for tri in triangles:
        corners = tri["corners"]
        if tri["owner"] == 0:
            # Keep our scoring triangles safe when the planned unit layout permits it.
            if all(owners[c] == 0 for c in corners):
                score += 2.0
            continue
        if not tri["me_can"]:
            continue
        owned = sum(owners[c] == 0 for c in corners)
        if owned == 1:
            score += 1.5
        elif owned == 2:
            score += 6.0
        elif owned == 3:
            score += 26.0 if tri["owner"] == -1 else 34.0
    return score


def choose_capture_plan(tokens, fixed_tokens, triangles, owners, my_units, opp_units, distances):
    available = [i for i in range(len(tokens)) if i not in fixed_tokens]
    best_score = -10**9
    best_targets = {}
    for tri in triangles:
        if tri["owner"] == 0 or not tri["me_can"]:
            continue
        corners = tri["corners"]
        slots = []
        already_owned = 0
        for corner in corners:
            if owners[corner] == 0:
                already_owned += 1
                continue
            need = max(1, opp_units[corner] + 1 - my_units[corner])
            slots.extend([corner] * need)
        if len(slots) > len(available):
            continue
        if not slots:
            score = 100.0 * already_owned + (20.0 if tri["owner"] == 1 else 0.0)
            if score > best_score:
                best_score, best_targets = score, {}
            continue

        for order in itertools.permutations(corners):
            ordered_slots = []
            for corner in order:
                ordered_slots.extend([corner] * slots.count(corner))
            chosen = []
            used = set()
            total_distance = 0
            max_distance = 0
            for corner in ordered_slots:
                options = [i for i in available if i not in used]
                if not options:
                    break
                token = min(options, key=lambda i: distances[tokens[i]][corner])
                d = distances[tokens[token]][corner]
                used.add(token)
                chosen.append((token, corner))
                total_distance += d
                max_distance = max(max_distance, d)
            if len(chosen) != len(slots):
                continue
            score = (100.0 * already_owned - 8.0 * total_distance -
                     3.0 * max_distance - 12.0 * len(slots) +
                     (20.0 if tri["owner"] == 1 else 0.0))
            if score > best_score:
                best_score = score
                best_targets = dict(chosen)
    return best_targets


def choose_new_path(triangles, linkable, adjacency, coords, my_units, excluded):
    best = None
    best_score = 0.0
    edges = {tuple(sorted((u, v))) for u in range(len(adjacency)) for v in adjacency[u] if u < v}
    for ti, tri in enumerate(triangles):
        if ti in excluded or tri["owner"] != 0:
            continue
        corners = tri["corners"]
        if any(my_units[c] < 1 for c in corners):
            continue
        for u in corners:
            for a, b in linkable:
                if u != a and u != b:
                    continue
                v = b if u == a else a
                if tuple(sorted((u, v))) in edges:
                    continue
                new_tris = []
                for w in adjacency[u].intersection(adjacency[v]):
                    if w == u or w == v:
                        continue
                    axy, bxy, cxy = coords[u], coords[v], coords[w]
                    if any(point_inside_triangle(coords[p], axy, bxy, cxy)
                           for p in range(len(coords)) if p not in (u, v, w)):
                        continue
                    new_tris.append((u, v, w))
                if not new_tris:
                    continue
                # Prefer edges that immediately create several useful scoring targets.
                score = 0.0
                for new_tri in new_tris:
                    owned = sum(my_units[c] > 0 for c in new_tri)
                    enemy = sum(my_units[c] < 1 for c in new_tri)
                    score += 1.0 + 0.8 * owned - 0.15 * enemy
                if score > best_score:
                    others = [c for c in corners if c != u]
                    best_score = score
                    best = (ti, f"ADD_PATH {u} {others[0]} {others[1]} {v}")
    return best


def choose_attack(triangles, adjacency, my_units, opp_units):
    best = None
    best_score = 0
    for ti, tri in enumerate(triangles):
        if tri["owner"] != 0:
            continue
        corners = tri["corners"]
        if any(my_units[c] < 1 for c in corners):
            continue
        targets = set().union(*(adjacency[c] for c in corners))
        for target in targets:
            enemy = opp_units[target]
            if enemy < 2:
                continue
            # Spending the triangle is worthwhile only against a meaningful stack.
            score = 10 * enemy + sum(1 for t in triangles
                                      if target in set().union(*(adjacency[c] for c in t["corners"])))
            if score > best_score:
                best_score = score
                a, b, c = corners
                best = (ti, f"ATTACK {a} {b} {c} {target}")
    return best


def run_turn(n, coords, my_score, opp_score, my_units, opp_units, adjacency,
             triangles, linkable, distances):
    commands = []
    used_triangles = set()

    attack = choose_attack(triangles, adjacency, my_units, opp_units)
    if attack is not None:
        ti, command = attack
        commands.append(command)
        used_triangles.add(ti)
        for c in triangles[ti]["corners"]:
            my_units[c] -= 1

    path = choose_new_path(triangles, linkable, adjacency, coords, my_units, used_triangles)
    if path is not None:
        ti, command = path
        commands.append(command)
        used_triangles.add(ti)

    tokens = [u for u, count in enumerate(my_units) for _ in range(max(0, count))]
    # Rebuild the reserved-token indexes against the final token list.
    fixed_tokens = set()
    if path is not None:
        for c in triangles[path[0]]["corners"]:
            for i, node in enumerate(tokens):
                if node == c and i not in fixed_tokens:
                    fixed_tokens.add(i)
                    break

    targets = list(tokens)
    owners = house_owners(my_units, opp_units, adjacency)
    capture_targets = choose_capture_plan(tokens, fixed_tokens, triangles, owners,
                                          my_units, opp_units, distances)
    for i, target in capture_targets.items():
        targets[i] = target
        fixed_tokens.add(i)

    # Greedily improve the remaining units' projected triangle coverage.
    for _ in range(2):
        for i, source in enumerate(tokens):
            if i in fixed_tokens:
                continue
            options = [source] + sorted(adjacency[source])
            best_node = targets[i]
            best_score = plan_score(targets, triangles, opp_units, adjacency)
            for destination in options:
                if destination == best_node:
                    continue
                old = targets[i]
                targets[i] = destination
                score = plan_score(targets, triangles, opp_units, adjacency)
                # Tiny movement cost resolves ties in favor of stable unit positions.
                score -= 0.05 * distances[source][destination]
                if score > best_score + 1e-9:
                    best_score = score
                    best_node = destination
                targets[i] = old
            targets[i] = best_node

    moves = {}
    for source, destination in zip(tokens, targets):
        if source != destination:
            moves[(source, destination)] = moves.get((source, destination), 0) + 1
    for (source, destination), amount in sorted(moves.items()):
        commands.append(f"MOVE {source} {destination} {amount}")

    # Spawn from every currently owned triangle not spent on another action.
    planned, _ = projected_owners(targets, opp_units, adjacency)
    unit_total = sum(my_units)
    future_spawns = [0] * n
    if unit_total < n:
        for ti, tri in enumerate(triangles):
            if tri["owner"] != 0 or ti in used_triangles or unit_total >= n:
                continue
            corners = tri["corners"]
            def spawn_value(c):
                value = 0.25 * len(adjacency[c]) - 0.4 * opp_units[c] + future_spawns[c]
                for other in triangles:
                    if other["owner"] == 0 or not other["me_can"] or c not in other["corners"]:
                        continue
                    count = sum(planned[x] > opp_units[x] for x in other["corners"] if x != c)
                    value += 1.0 + 2.0 * count
                return value
            spawn = max(corners, key=spawn_value)
            other = [c for c in corners if c != spawn]
            commands.append(f"SPAWN {spawn} {other[0]} {other[1]}")
            future_spawns[spawn] += 1
            unit_total += 1

    return ";".join(commands) if commands else "WAIT"


def main():
    first = read_ints()
    if first is None:
        return
    n = first[0]
    coords = [None] * n
    for _ in range(n):
        row = read_ints()
        if row is None:
            return
        node, x, y = row
        coords[node] = (x, y)

    while True:
        scores = read_ints()
        if scores is None:
            return
        my_score, opp_score = scores
        my_units = [0] * n
        opp_units = [0] * n
        for _ in range(n):
            row = read_ints()
            if row is None:
                return
            node, mine, theirs = row
            my_units[node], opp_units[node] = mine, theirs
        path_row = read_ints()
        if path_row is None:
            return
        path_count = path_row[0]
        adjacency = [set() for _ in range(n)]
        for _ in range(path_count):
            u, v = read_ints()
            adjacency[u].add(v)
            adjacency[v].add(u)
        tri_row = read_ints()
        if tri_row is None:
            return
        triangle_count = tri_row[0]
        triangles = []
        for _ in range(triangle_count):
            u, v, w, owner, me_can, opp_can = read_ints()
            triangles.append({"corners": (u, v, w), "owner": owner,
                              "me_can": bool(me_can), "opp_can": bool(opp_can)})
        link_row = read_ints()
        if link_row is None:
            return
        link_count = link_row[0]
        linkable = []
        for _ in range(link_count):
            linkable.append(tuple(read_ints()))

        distances = bfs_all(adjacency)
        action = run_turn(n, coords, my_score, opp_score, my_units, opp_units,
                          adjacency, triangles, linkable, distances)
        print(action, flush=True)


if __name__ == "__main__":
    main()
