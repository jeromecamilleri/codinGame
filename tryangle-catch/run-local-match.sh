#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REFEREE="$ROOT/vendor/TryAngle-Catch"
SEED="${1:-20261108}"
BOT1="${2:-$ROOT/bot_simple.py}"
BOT2="${3:-$ROOT/bot.py}"
STARTING_UNITS="${4:-3}"
STARTING_TRIANGLES="${5:-3}"
if [[ "$BOT1" != /* ]]; then BOT1="$ROOT/$BOT1"; fi
if [[ "$BOT2" != /* ]]; then BOT2="$ROOT/$BOT2"; fi

if [[ ! -f "$BOT1" ]]; then
  echo "Bot script not found: $BOT1" >&2
  exit 1
fi
if [[ ! -f "$BOT2" ]]; then
  echo "Bot script not found: $BOT2" >&2
  exit 1
fi

"$ROOT/scripts/build-local-referee.sh"
cd "$REFEREE"
CLASSPATH="$REFEREE/target/classes:$REFEREE/target/dependency/*"
exec java --add-opens=java.base/java.lang=ALL-UNNAMED \
  -Dlog4j.configurationFile="$REFEREE/src/test/resources/log4j2.properties" \
  -cp "$CLASSPATH" local.LocalMatchMain \
  "$BOT1" "$BOT2" "$SEED" "$STARTING_UNITS" "$STARTING_TRIANGLES"
