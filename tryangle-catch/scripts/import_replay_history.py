#!/usr/bin/env python3
"""Build a compact JSONL index from archived CodinGame text replay logs."""

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "replays" / "raw"
DEFAULT_OUTPUT = ROOT / "replays" / "replay_history.jsonl"
ACTION_RE = re.compile(r"^(MOVE|SPAWN|ADD_PATH|REMOVE_PATH|ATTACK|WAIT)\b", re.I)
EVENT_RE = re.compile(
    r"\$(\d+):?\s+(captured|spawned|surrounded|added|can't score any more points|"
    r"no units or triangles left|is dominated|timeout)(?:\s+(\d+))?"
)


def parse_log(path):
    text = path.read_text(errors="replace")
    game_match = re.search(r"^game (\d+)$", text, re.M)
    if not game_match:
        raise ValueError(f"No game id in {path}")
    game_id = game_match.group(1)

    names = {
        int(m.group(1)): m.group(2).strip()
        for m in re.finditer(r"^\s*(\d+) (.*?) \(.*?agent_id [^)]+\)", text, re.M)
    }
    action_counts = defaultdict(Counter)
    action_histogram = defaultdict(Counter)
    move_pairs = defaultdict(Counter)
    events = defaultdict(Counter)
    first_capture = {}
    rejection_count = Counter()
    current = None

    for line in text.splitlines():
        frame_match = re.match(r"frame (\d+) agent (\d+)", line)
        if frame_match:
            current = (int(frame_match.group(1)), int(frame_match.group(2)))
            continue

        if line.startswith("  stdout:") and current:
            player = current[1]
            commands_this_frame = 0
            for command in line[len("  stdout:"):].split(";"):
                command = command.strip()
                action_match = ACTION_RE.match(command)
                if not action_match:
                    continue
                action = action_match.group(1).upper()
                action_counts[player][action] += 1
                commands_this_frame += 1
                if action == "MOVE":
                    parts = command.split()
                    if len(parts) >= 3:
                        move_pairs[player][f"{parts[1]}->{parts[2]}"] += 1
            action_histogram[player][str(commands_this_frame)] += 1
            continue

        if line.startswith("  summary:"):
            message = line[len("  summary:"):].strip()
            if "Task can't be applied" in message or "Unknown command" in message:
                player_match = re.search(r"\$(\d+)", message)
                if player_match:
                    rejection_count[int(player_match.group(1))] += 1
            event_match = EVENT_RE.search(message)
            if event_match:
                player = int(event_match.group(1))
                event = event_match.group(2)
                amount = int(event_match.group(3) or 1)
                events[player][event] += amount
                if event == "captured" and player not in first_capture and current:
                    first_capture[player] = current[0]
                if event in ("can't score any more points", "no units or triangles left",
                             "is dominated", "timeout"):
                    events[player]["loss_reason"] = event

    scores_match = re.search(r"scores: 0=(-?\d+) 1=(-?\d+)", text)
    scores = [int(scores_match.group(1)), int(scores_match.group(2))] if scores_match else None
    ranking_match = re.search(r"ranking \(agent indexes, winner first\):\s*(\d+)\s+(\d+)", text)
    winner = int(ranking_match.group(1)) if ranking_match else None
    seed_match = re.search(r"^options: seed=(-?\d+)", text, re.M)

    players = []
    for player_id in sorted(set(names) | set(action_counts) | set(events)):
        players.append({
            "index": player_id,
            "nickname": names.get(player_id, f"player-{player_id}"),
            "action_counts": dict(action_counts[player_id]),
            "commands_per_turn": dict(action_histogram[player_id]),
            "top_moves": move_pairs[player_id].most_common(10),
            "events": dict(events[player_id]),
            "first_capture_frame": first_capture.get(player_id),
            "rejected_or_invalid_actions": rejection_count[player_id],
        })

    return {
        "game_id": game_id,
        "seed": seed_match.group(1) if seed_match else None,
        "players": players,
        "scores": scores,
        "winner_index": winner,
        "raw_log": str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),
        "source": "CodinGame game text log; per-turn input observations are not included",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("logs", nargs="*", help="raw game logs; defaults to replays/raw/*.log")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    files = [Path(p) for p in args.logs] if args.logs else sorted(DEFAULT_INPUT.glob("*.log"))
    if not files:
        parser.error(f"No replay logs found in {DEFAULT_INPUT}")
    output = args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w") as stream:
        for path in files:
            stream.write(json.dumps(parse_log(path), ensure_ascii=False, separators=(",", ":")))
            stream.write("\n")
    print(f"Wrote {len(files)} game records to {output}")


if __name__ == "__main__":
    main()
