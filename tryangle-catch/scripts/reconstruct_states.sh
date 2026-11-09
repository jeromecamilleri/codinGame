#!/usr/bin/env bash
# Usage: reconstruct_states.sh <game-id>...
# Replays both recorded seats in the local referee (standard start) and stores the
# observations each seat received in replays/states/<game-id>/seat{0,1}.txt.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REFEREE="$ROOT/vendor/TryAngle-Catch"
"$ROOT/scripts/build-local-referee.sh" >/dev/null

for GAME in "$@"; do
  LOG="$ROOT/replays/raw/$GAME.log"
  SEED="$(sed -n 's/^options: seed=\(-\?[0-9]*\).*/\1/p' "$LOG")"
  export CODINGAME_REPLAY_LOG="$LOG" CODINGAME_RECORD_DIR="$ROOT/replays/states/$GAME"
  java --add-opens=java.base/java.lang=ALL-UNNAMED \
    -Dlog4j.configurationFile="$REFEREE/src/test/resources/log4j2.properties" \
    -cp "$REFEREE/target/classes:$REFEREE/target/dependency/*" \
    local.LocalBatchMain "$ROOT/scripts/record_replay_agent.py 0" \
    "$ROOT/scripts/record_replay_agent.py 1" "$SEED" 2>&1 | tail -n 1
done
