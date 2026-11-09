#!/usr/bin/env python3
"""Lance des test games CodinGame (puzzle bot programming) contre des agents adverses et archive les logs.

  cg_test_games.py PUZZLE bot.py --opp AGENT_ID [--opp ID ...] [--count N] [--out DIR]

Les logs JSON (coups de l'adversaire dans `stdout`) vont dans DIR/<test_game_id>.json et .log (texte).
Une seule partie à la fois ; le token n'est jamais affiché.
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

API = "https://www.codingame.com/api/v1"
TOKEN = Path(os.environ.get("CG_TOKEN_FILE", Path.home() / ".config/codingame/token")).read_text().strip()


def call(method, path, body=None):
    req = urllib.request.Request(
        API + path, method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.load(r) if "json" in r.headers.get("Content-Type", "") else r.read().decode()
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        try:
            return e.code, json.loads(raw)
        except ValueError:
            return e.code, raw


def wait_done(puzzle, gid, fmt):
    while True:
        status, data = call("GET", f"/test-games/{gid}?wait=30&format={fmt}")
        if status == 200 and (not isinstance(data, dict) or data.get("status") in ("done", "failed")):
            return data
        if isinstance(data, str) and "status: running" not in data:
            return data
        time.sleep(2)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("puzzle")
    ap.add_argument("bot", type=Path)
    ap.add_argument("--opp", action="append", required=True, help="agent_id adverse (répétable)")
    ap.add_argument("--count", type=int, default=3, help="parties par adversaire")
    ap.add_argument("--out", type=Path, default=Path("replays/boss"))
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    code = a.bot.read_text()
    for opp in a.opp:
        for i in range(a.count):
            body = {"language": "Python3", "code": code, "opponents": [opp]}
            while True:
                status, data = call("POST", f"/puzzles/{a.puzzle}/test-games?wait=30", body)
                if status == 409 and isinstance(data, dict) and data.get("test_game_id"):
                    time.sleep(5)
                    continue
                if status == 429:
                    time.sleep(int(15))
                    continue
                break
            if status not in (200, 202) or not isinstance(data, dict):
                print(f"opp {opp}: erreur {status} {str(data)[:300]}", file=sys.stderr)
                continue
            gid = data["test_game_id"]
            if data.get("status") != "done":
                wait_done(a.puzzle, gid, "json")
            _, js = call("GET", f"/test-games/{gid}?format=json")
            _, txt = call("GET", f"/test-games/{gid}?format=text")
            (a.out / f"{opp}_{gid}.json").write_text(json.dumps(js))
            (a.out / f"{opp}_{gid}.log").write_text(txt if isinstance(txt, str) else json.dumps(txt))
            print(f"opp {opp} game {gid} -> {a.out}")
            time.sleep(7)


if __name__ == "__main__":
    main()
