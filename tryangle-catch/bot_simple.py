#!/usr/bin/env python3
"""Conservative first bot: keep units safe and spawn a few reinforcements."""

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


def get_house_owners(my_units, opponent_units, neighbors):
    owners = [None] * len(my_units)
    for house, adjacent in enumerate(neighbors):
        if adjacent and all(my_units[n] > opponent_units[n] for n in adjacent):
            owners[house] = 0
        elif adjacent and all(opponent_units[n] > my_units[n] for n in adjacent):
            owners[house] = 1
        elif my_units[house] > opponent_units[house]:
            owners[house] = 0
        elif opponent_units[house] > my_units[house]:
            owners[house] = 1
    return owners


def distances_to_enemy_frontier(opponent_units, neighbors):
    """Distance to enemy-occupied houses, allowing contact at the destination."""
    enemy_houses = [house for house, count in enumerate(opponent_units) if count > 0]
    distances = [len(neighbors) + 1] * len(neighbors)
    next_step = [None] * len(neighbors)
    queue = deque()
    for house in enemy_houses:
        distances[house] = 0
        queue.append(house)
    while queue:
        current = queue.popleft()
        for previous in neighbors[current]:
            if opponent_units[previous] > 0 or distances[previous] <= distances[current] + 1:
                continue
            distances[previous] = distances[current] + 1
            next_step[previous] = current
            queue.append(previous)
    return distances, next_step


def choose_approach_move(my_units, opponent_units, neighbors,
                         owned_triangles, distances, next_step):
    """Advance one unit toward the opponent while keeping a guard behind."""
    owners_before = get_house_owners(my_units, opponent_units, neighbors)
    best = None
    best_score = -10**9

    for source, count in enumerate(my_units):
        if count == 0:
            continue
        if distances[source] == 0 or next_step[source] is None:
            continue
        destination = next_step[source]
        # Do not feed a tiny scout into a much larger enemy stack.
        if opponent_units[destination] > count + my_units[destination]:
            continue

        after_mine = my_units[:]
        after_mine[source] -= 1
        after_mine[destination] += 1
        after_owners = get_house_owners(after_mine, opponent_units, neighbors)
        if after_mine[source] > 0 and neighbors[source] and all(
            after_owners[n] == 1 for n in neighbors[source]
        ):
            continue
        if neighbors[destination] and all(
            after_owners[n] == 1 for n in neighbors[destination]
        ):
            continue

        score = -distances[source] * 2
        if opponent_units[destination] > 0:
            score += 30 + opponent_units[destination]
        if count > 1:
            score += 1
        for corners, owner, can_capture in owned_triangles:
            before = sum(owners_before[n] == 0 for n in corners)
            after = sum(after_owners[n] == 0 for n in corners)
            if owner == 0:
                score -= 4 * max(0, before - after)
            elif can_capture:
                score += 8 * max(0, after - before)
                if after == 3:
                    score += 40

        # The enemy-house bonus encourages actual contact; ids break ties.
        score -= destination * 0.001
        if score > best_score:
            best_score = score
            best = (source, destination)

    return best


def choose_attack(my_units, opponent_units, neighbors, triangles):
    """Use a triangle to clear nearby enemy units, while preserving reserves."""
    if sum(my_units) <= 6:
        return None
    best = None
    best_score = 0
    for corners, owner, _can_capture in triangles:
        if owner != 0 or any(my_units[node] < 1 for node in corners):
            continue
        targets = set().union(*(neighbors[node] for node in corners))
        for target in targets:
            enemy_count = opponent_units[target]
            if enemy_count == 0:
                continue
            score = enemy_count * 10
            if score > best_score:
                a, b, c = corners
                best_score = score
                best = f"ATTACK {a} {b} {c} {target}"
    return best


def main():
    first = read_ints()
    if not first:
        return
    house_count = first[0]

    # House coordinates are fixed for the whole match; consume them once.
    for _ in range(house_count):
        if read_ints() is None:
            return

    while True:
        scores = read_ints()
        if scores is None:
            return

        my_units = [0] * house_count
        opponent_units = [0] * house_count
        for _ in range(house_count):
            row = read_ints()
            if row is None:
                return
            house, mine, theirs = row
            my_units[house] = mine
            opponent_units[house] = theirs

        path_count_row = read_ints()
        if path_count_row is None:
            return
        path_count = path_count_row[0]
        neighbors = [set() for _ in range(house_count)]
        for _ in range(path_count):
            edge = read_ints()
            if edge is None:
                return
            a, b = edge
            neighbors[a].add(b)
            neighbors[b].add(a)

        triangle_count_row = read_ints()
        if triangle_count_row is None:
            return
        triangle_count = triangle_count_row[0]
        owned_triangles = []
        for _ in range(triangle_count):
            row = read_ints()
            if row is None:
                return
            a, b, c, owner, can_capture, _opponent_can_capture = row
            if owner == 0:
                owned_triangles.append(((a, b, c), owner, bool(can_capture)))
            else:
                owned_triangles.append(((a, b, c), owner, bool(can_capture)))

        linkable_count_row = read_ints()
        if linkable_count_row is None:
            return
        for _ in range(linkable_count_row[0]):
            if read_ints() is None:
                return

        distances, next_step = distances_to_enemy_frontier(opponent_units, neighbors)
        move = choose_approach_move(
            my_units, opponent_units, neighbors, owned_triangles, distances, next_step
        )
        attack = choose_attack(my_units, opponent_units, neighbors, owned_triangles)

        # Spawning costs no units, but spends the triangle. Keep a small reserve
        # of owned triangles for scoring. Moving a surplus unit gets priority,
        # so the bots travel toward each other instead of just building at home.
        unit_total = sum(my_units)
        action = "WAIT"
        available_owned = [tri for tri in owned_triangles if tri[1] == 0]
        if attack is not None:
            action = attack
        elif move is not None:
            action = f"MOVE {move[0]} {move[1]} 1"
        elif unit_total < 6 and len(available_owned) > 1:
            # Spawn a forward scout; leave one triangle unused for points.
            corners, _owner, _can_capture = min(
                available_owned,
                key=lambda tri: min(distances[node] for node in tri[0]),
            )
            spawn = min(corners, key=lambda node: (distances[node], -len(neighbors[node])))
            other = [node for node in corners if node != spawn]
            action = f"SPAWN {spawn} {other[0]} {other[1]}"

        print(action, flush=True)


if __name__ == "__main__":
    main()
