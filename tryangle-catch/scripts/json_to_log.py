#!/usr/bin/env python3
"""Convert CodinGame API replay JSON files into the text-log layout used by the other scripts."""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "replays" / "raw"


def convert(data):
    lines = [f"game {data['gameId']}"]
    referee = [line for line in data.get("refereeInput", "").split("\n") if line]
    lines.append("options: " + referee[0] if referee else "options:")
    lines.extend("    " + line for line in referee[1:])
    lines.append("agents:")
    for agent in data["agents"]:
        name = (agent.get("codingamer") or {}).get("pseudo") \
            or (agent.get("arenaboss") or {}).get("nickname") or f"player-{agent['index']}"
        prefix = "me, " if agent["index"] == 0 else ""
        lines.append(f"  {agent['index']} {name} ({prefix}agent_id {agent['agentId']})")
    for index, frame in enumerate(data["frames"]):
        agent = frame.get("agentId")
        lines.append(f"frame {index} agent {agent}" if agent is not None else f"frame {index}")
        for line in (frame.get("summary") or "").splitlines():
            if line.strip():
                lines.append("  summary: " + line.strip())
        stdout = (frame.get("stdout") or "").strip()
        if stdout:
            lines.append("  stdout: " + stdout)
    scores = data.get("scores", [])
    ranks = data.get("ranks", [])
    lines.append("result")
    lines.append("  scores: " + " ".join(f"{i}={int(s)}" for i, s in enumerate(scores)))
    order = sorted(range(len(ranks)), key=lambda i: ranks[i])
    lines.append("  ranking (agent indexes, winner first): " + " ".join(map(str, order)))
    for tip in data.get("tooltips", []):
        item = json.loads(tip)
        lines.append(f"  tooltips: frame {item['turn']}: {item['text']}")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*", type=Path, help="defaults to replays/raw/*.json")
    args = parser.parse_args()
    for path in args.files or sorted(RAW.glob("*.json")):
        data = json.loads(path.read_text())
        target = path.with_suffix(".log")
        target.write_text(convert(data))
        print(f"{path} -> {target}")


if __name__ == "__main__":
    main()
