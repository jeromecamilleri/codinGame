#!/usr/bin/env python3
"""Outils API CodinGame partagés (le token reste dans ~/.config/codingame/token, jamais affiché).

  cg_api.py replay ID [ID ...] [--out DIR]   télécharge replays/raw/ID.json (findByGameId)
  cg_api.py puzzle PUBLIC_ID [--out DIR]     enregistre puzzle.json et statement.md
"""
import argparse
import json
import os
import urllib.request
from pathlib import Path

API = "https://www.codingame.com/api/v1"
TOKEN_FILE = Path(os.environ.get("CG_TOKEN_FILE", Path.home() / ".config/codingame/token"))


def token():
    return TOKEN_FILE.read_text().strip()


def get(path):
    req = urllib.request.Request(API + path, headers={"Authorization": f"Bearer {token()}"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def fetch_replay(game_id):
    req = urllib.request.Request(
        "https://www.codingame.com/services/gameResult/findByGameId",
        data=json.dumps([int(game_id), None]).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("replay")
    r.add_argument("ids", nargs="+")
    r.add_argument("--out", type=Path, default=Path("replays/raw"))
    p = sub.add_parser("puzzle")
    p.add_argument("public_id")
    p.add_argument("--out", type=Path, default=Path("."))
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    if a.cmd == "replay":
        for gid in a.ids:
            gid = gid.rstrip("/").split("/")[-1]
            (a.out / f"{gid}.json").write_text(json.dumps(fetch_replay(gid)))
            print(f"{a.out / (gid + '.json')}")
    else:
        data = get(f"/puzzles/{a.public_id}")
        (a.out / "puzzle.json").write_text(json.dumps(data, indent=2, ensure_ascii=False))
        statement = data.get("statement") or data.get("description") or ""
        (a.out / "statement.md").write_text(statement)
        print(f"{a.out}/puzzle.json, statement.md")


if __name__ == "__main__":
    main()
