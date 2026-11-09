#!/usr/bin/env bash
# Usage: ./run-referee.sh view|batch [bot0.py] [bot1.py] [seed] [niveau_ligue] [port]
# Referee OFFICIEL (vendor/referee). niveau_ligue: 1..5 (Wood 3 du puzzle ~ niveau bas, 5 = règles complètes).
set -euo pipefail
cd "$(dirname "$0")"
MODE="${1:-view}"; B0="${2:-bot.py}"; B1="${3:-bot.py}"; SEED="${4:-1}"; LEVEL="${5:-5}"; PORT="${6:-8888}"
RES=vendor/referee/src/main/resources
if [ "$MODE" = view ] && [ ! -f "$RES/view/graphics/ViewModule.js" ]; then
  (cd "$RES" && npm install --no-audit --no-fund --silent && npx tsc)
fi
../common/run_duel_referee.sh "$MODE" vendor/referee "$LEVEL" "$SEED" "$PORT" "$B0" "$B1" 2>&1 | grep -v '^SLF4J'
