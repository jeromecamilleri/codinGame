#!/usr/bin/env python3
"""Replay one player's recorded stdout actions as a fixed local opponent.

Set CODINGAME_REPLAY_LOG to an archived text log and
CODINGAME_REPLAY_AGENT to the recorded player index (usually 1 for Baron Bosswell).
"""

import os
import re
import sys
from pathlib import Path


def recorded_actions(log_path, player_index):
    actions = []
    current_player = None
    for line in Path(log_path).read_text(errors="replace").splitlines():
        match = re.match(r"frame \d+ agent (\d+)", line)
        if match:
            current_player = int(match.group(1))
            continue
        if current_player == player_index and line.startswith("  stdout:"):
            action = line[len("  stdout:"):].strip()
            actions.append(action if action else "WAIT")
    return actions


def read_ints():
    line = sys.stdin.buffer.readline()
    if not line:
        return None
    try:
        return [int(value) for value in line.split()]
    except ValueError:
        return None


def consume_turn(house_count):
    if read_ints() is None:  # scores
        return False
    for _ in range(house_count):
        if read_ints() is None:
            return False
    count = read_ints()
    if count is None:
        return False
    for _ in range(count[0]):
        if read_ints() is None:
            return False
    count = read_ints()
    if count is None:
        return False
    for _ in range(count[0]):
        if read_ints() is None:
            return False
    count = read_ints()
    if count is None:
        return False
    for _ in range(count[0]):
        if read_ints() is None:
            return False
    return True


def main():
    log_path = os.environ.get("CODINGAME_REPLAY_LOG")
    if not log_path:
        print("Set CODINGAME_REPLAY_LOG to a saved CodinGame log", file=sys.stderr)
        return
    try:
        player_index = int(os.environ.get("CODINGAME_REPLAY_AGENT", "1"))
        actions = recorded_actions(log_path, player_index)
    except Exception as error:
        print(f"Could not read replay actions: {error}", file=sys.stderr)
        return

    first = read_ints()
    if not first:
        return
    house_count = first[0]
    for _ in range(house_count):
        if read_ints() is None:
            return

    action_index = 0
    while consume_turn(house_count):
        action = actions[action_index] if action_index < len(actions) else "WAIT"
        action_index += 1
        print(action, flush=True)


if __name__ == "__main__":
    main()
