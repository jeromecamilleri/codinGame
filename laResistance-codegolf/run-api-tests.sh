#!/usr/bin/env bash
# Usage: ./run-api-tests.sh [fichier.py] [N ...]   -> test games CodinGame (vrai validateur), un à la fois
# Affiche success / found / expected pour chaque cas ; le token n'est jamais affiché.
set -uo pipefail
cd "$(dirname "$0")"
source ../common/env.sh
BOT="${1:-golf.py}"; shift || true
[ $# -eq 0 ] && set -- $(seq 1 6)
for n in "$@"; do
  r=$(jq -n --rawfile code "$BOT" --argjson t "$n" '{language:"Python3",code:$code,testcase:$t}' \
      | cg -X POST "$CG_API/puzzles/the-resistance-codesize/test-games?wait=30" -H 'Content-Type: application/json' --data-binary @-)
  echo "$r" | jq -c --argjson n "$n" '{test:$n, status, success, found, expected, error, timeout}'
  sleep 2
done
