#!/usr/bin/env bash
# Usage: run-head-to-head.sh BOT_A BOT_B [first_seed] [count]
# Plays both seats on each seed (standard start) and prints A wins/losses/draws.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REFEREE="$ROOT/vendor/TryAngle-Catch"
A="$1"; B="$2"; FIRST="${3:-1000}"; COUNT="${4:-20}"
[[ "$A" != /* ]] && A="$ROOT/$A"
[[ "$B" != /* ]] && B="$ROOT/$B"
SEEDS=($(seq "$FIRST" $((FIRST + COUNT - 1))))

"$ROOT/scripts/build-local-referee.sh" >/dev/null
run_pair() {
  java --add-opens=java.base/java.lang=ALL-UNNAMED \
    -Dlog4j.configurationFile="$REFEREE/src/test/resources/log4j2.properties" \
    -cp "$REFEREE/target/classes:$REFEREE/target/dependency/*" \
    local.LocalBatchMain "$1" "$2" "${SEEDS[@]}"
}

{ run_pair "$A" "$B" | sed 's/^/A0\t/'; run_pair "$B" "$A" | sed 's/^/A1\t/'; } |
  grep -P '^A[01]\t\d+\t' |
  awk -F'\t' '{ a = ($1=="A0") ? $5 : $6; b = ($1=="A0") ? $6 : $5;
    if (a>b) w++; else if (a<b) l++; else d++; if ($7 != "") f++ }
    END { printf "A wins/losses/draws: %d / %d / %d (failures: %d)\n", w, l, d, f }'
