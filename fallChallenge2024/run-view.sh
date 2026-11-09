#!/usr/bin/env bash
# Usage: ./run-view.sh [bot.py] [N] [port]  -> visualiseur sur http://localhost:8888
set -euo pipefail
cd "$(dirname "$0")"
BOT="${1:-bot_v1.py}"; N="${2:-1}"; PORT="${3:-8888}"
[ -f "$BOT" ] || { echo "Bot introuvable: $BOT"; exit 1; }
RES=vendor/referee/src/main/resources
if [ ! -f "$RES/view/graphics/ViewModule.js" ]; then   # la vue TypeScript doit être compilée une fois
  (cd "$RES" && npm install --no-audit --no-fund --silent && npx tsc)
fi
../common/run_solo_referee.sh view vendor/referee "$BOT" "$PWD/vendor/referee/config/test$N.json" "$PORT"
