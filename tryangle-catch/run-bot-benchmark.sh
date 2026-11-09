#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REFEREE="$ROOT/vendor/TryAngle-Catch"
OUT="${1:-$ROOT/benchmarks/2026-11-08-v4-winning-bronze.tsv}"
shift || true
BOT_CANDIDATE="${BOT_CANDIDATE:-$ROOT/bot_v4_capture_spawn.py}"
if (($#)); then
  SEEDS=("$@")
else
  SEEDS=(20261108 20261109 20261110 20261111 20261112)
fi

"$ROOT/scripts/build-local-referee.sh" >/dev/null
mkdir -p "$(dirname "$OUT")"
printf 'seed\tbot0\tbot1\tscore0\tscore1\tfailure\tsummary\n' > "$OUT"

run_pair() {
  local first="$1" second="$2"
  java --add-opens=java.base/java.lang=ALL-UNNAMED \
    -Dlog4j.configurationFile="$REFEREE/src/test/resources/log4j2.properties" \
    -cp "$REFEREE/target/classes:$REFEREE/target/dependency/*" \
    local.LocalBatchMain "$first" "$second" "${SEEDS[@]}" >> "$OUT"
}

run_pair "$BOT_CANDIDATE" "$ROOT/bot_simple.py"
run_pair "$ROOT/bot_simple.py" "$BOT_CANDIDATE"
run_pair "$BOT_CANDIDATE" "$ROOT/bot.py"
run_pair "$ROOT/bot.py" "$BOT_CANDIDATE"
run_pair "$ROOT/bot_simple.py" "$ROOT/bot.py"
run_pair "$ROOT/bot.py" "$ROOT/bot_simple.py"

cat "$OUT"
