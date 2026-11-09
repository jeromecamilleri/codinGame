#!/usr/bin/env python3
"""Per-turn features of both players from replays/states/<game>/seat*.txt and the raw logs.

Prints one table per game, then an aggregate Baron-versus-others summary.
Run scripts/reconstruct_states.sh first.
"""

import json
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKPOINTS = (5, 10, 20, 40, 80)


def load_turns(path):
    blocks = path.read_text().split("---\n")
    n = int(blocks[0].split()[0])
    turns = []
    for block in blocks[1:]:
        lines = [l for l in block.split("\n")]
        score_mine, score_theirs = map(int, lines[0].split()[:2])
        mine, theirs = [0] * n, [0] * n
        for row in lines[1:1 + n]:
            node, a, b = map(int, row.split())
            mine[node], theirs[node] = a, b
        pos = 1 + n
        edge_count = int(lines[pos].split()[0])
        pos += 1 + edge_count
        tri_count = int(lines[pos].split()[0])
        triangles = [tuple(map(int, lines[pos + 1 + i].split())) for i in range(tri_count)]
        turns.append({"score": (score_mine, score_theirs), "mine": mine, "theirs": theirs,
                      "edges": edge_count, "triangles": triangles})
    return turns


def parse_log(path):
    names, actions, current = {}, {0: [], 1: []}, None
    for line in path.read_text(errors="replace").splitlines():
        m = re.match(r"\s+(\d) (.*?) \(.*agent_id", line)
        if m:
            names[int(m.group(1))] = m.group(2).strip()
        m = re.match(r"frame \d+ agent (-?\d+)", line)
        if m:
            current = int(m.group(1))
        elif line.startswith("  stdout:") and current in actions:
            text = line[len("  stdout:"):].strip()
            cmds = [c.strip() for c in text.split(";")
                    if re.match(r"\s*(MOVE|SPAWN|ADD_PATH|REMOVE_PATH|WAIT)", c)]
            actions[current].append(cmds)
    return names, actions


def features(turns, cmds):
    rows = []
    spawn_turns, move_counts, stack_moves = [], [], 0
    tri_turns = tri_spawn = 0
    for t, turn in enumerate(turns):
        mine = turn["mine"]
        owned = sum(1 for tri in turn["triangles"] if tri[3] == 0)
        foes = sum(1 for tri in turn["triangles"] if tri[3] == 1)
        rows.append({"t": t, "units": sum(mine), "houses": sum(1 for u in mine if u),
                     "max_stack": max(mine), "tri": owned, "opp_tri": foes,
                     "score": turn["score"][0], "opp_units": sum(turn["theirs"])})
        if t < len(cmds):
            moves = [c for c in cmds[t] if c.startswith("MOVE")]
            move_counts.append(len(moves))
            stack_moves += sum(1 for c in moves if int(c.split()[3]) > 1)
            if any(c.startswith("SPAWN") for c in cmds[t]):
                spawn_turns.append(t)
                if owned:
                    tri_spawn += 1
        if owned and t < len(cmds):
            tri_turns += 1
    return rows, spawn_turns, move_counts, stack_moves, (tri_turns, tri_spawn)


def main():
    summary = {}
    for game_dir in sorted((ROOT / "replays" / "states").iterdir()):
        game = game_dir.name
        names, actions = parse_log(ROOT / "replays" / "raw" / f"{game}.log")
        print(f"\n== {game}: seat0 {names.get(0)} / seat1 {names.get(1)}")
        for seat in (0, 1):
            turns = load_turns(game_dir / f"seat{seat}.txt")
            rows, spawns, moves, stacks, tri = features(turns, actions[seat])
            name = names.get(seat, f"seat{seat}")
            at = {c: rows[min(c, len(rows) - 1)] for c in CHECKPOINTS}
            line = " ".join(f"t{c}:u{r['units']}/h{r['houses']}/T{r['tri']}" for c, r in at.items())
            first = spawns[0] if spawns else None
            print(f"  {name:16} turns={len(rows)} spawns={len(spawns)} first_spawn={first} "
                  f"moves/turn={statistics.mean(moves) if moves else 0:.1f} "
                  f"max_stack={max(r['max_stack'] for r in rows)} stack_moves={stacks} "
                  f"tours_avec_triangle={tri[0]} dont_spawn={tri[1]}\n"
                  f"      {line}")
            key = "Baron" if name == "Baron Bosswell" else ("jejecam" if name == "jejecam" else "autres")
            s = summary.setdefault(key, {"parts": 0, "spawns": [], "first": [], "moves": [],
                                         **{f"u{c}": [] for c in CHECKPOINTS},
                                         **{f"T{c}": [] for c in CHECKPOINTS}})
            s["parts"] += 1
            s["spawns"].append(len(spawns))
            if first is not None:
                s["first"].append(first)
            s["moves"].extend(moves)
            for c, r in at.items():
                s[f"u{c}"].append(r["units"])
                s[f"T{c}"].append(r["tri"])
    print("\n== Moyennes par type de joueur (parties où le tour existe, sinon dernier tour)")
    for key, s in summary.items():
        avg = lambda v: f"{statistics.mean(v):.1f}" if v else "-"
        print(f"  {key:8} n={s['parts']} spawns={avg(s['spawns'])} 1er_spawn={avg(s['first'])} "
              f"moves/tour={avg(s['moves'])} "
              + " ".join(f"t{c}:u{avg(s[f'u{c}'])}/T{avg(s[f'T{c}'])}" for c in CHECKPOINTS))


if __name__ == "__main__":
    sys.exit(main())
