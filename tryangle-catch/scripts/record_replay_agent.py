#!/usr/bin/env python3
"""Replay one seat's recorded actions and record every observation the referee sends.

Usage: record_replay_agent.py <seat> ; env CODINGAME_REPLAY_LOG and CODINGAME_RECORD_DIR.
Writes <record dir>/seat<seat>.txt: the initial block, then one block per turn,
separated by lines containing only '---'.
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from replay_agent import recorded_actions  # noqa: E402


def read_line():
    line = sys.stdin.buffer.readline()
    return line.decode().rstrip("\n") if line else None


def read_block(out, groups):
    """Copy a turn: scores, `groups[0]` rows, then three count-prefixed sections."""
    line = read_line()
    if line is None:
        return False
    out.append(line)
    for _ in range(groups):
        row = read_line()
        if row is None:
            return False
        out.append(row)
    for _ in range(3):
        count = read_line()
        if count is None:
            return False
        out.append(count)
        for _ in range(int(count.split()[0])):
            row = read_line()
            if row is None:
                return False
            out.append(row)
    return True


def main():
    seat = int(sys.argv[1])
    actions = recorded_actions(os.environ["CODINGAME_REPLAY_LOG"], seat)
    target = Path(os.environ["CODINGAME_RECORD_DIR"]) / f"seat{seat}.txt"
    target.parent.mkdir(parents=True, exist_ok=True)
    first = read_line()
    if first is None:
        return
    n = int(first.split()[0])
    header = [first]
    for _ in range(n):
        header.append(read_line())
    with target.open("w") as stream:
        stream.write("\n".join(header) + "\n")
        index = 0
        while True:
            block = []
            if not read_block(block, n):
                break
            stream.write("---\n" + "\n".join(block) + "\n")
            stream.flush()
            print(actions[index] if index < len(actions) else "WAIT", flush=True)
            index += 1


if __name__ == "__main__":
    main()
