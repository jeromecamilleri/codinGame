#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if (($# < 2)); then
  echo "Usage: run-vs-replay.sh <game-id> <your-bot.py> [recorded-player-index]" >&2
  exit 2
fi

GAME_ID="$1"
BOT="$2"
PLAYER_INDEX="${3:-1}"
if [[ ! "$GAME_ID" =~ ^[0-9]+$ ]]; then
  echo "Invalid game id: $GAME_ID" >&2
  exit 2
fi
LOG="$ROOT/replays/raw/$GAME_ID.log"
if [[ ! -f "$LOG" ]]; then
  echo "Replay log not found: $LOG" >&2
  exit 1
fi
if [[ "$BOT" != /* ]]; then BOT="$ROOT/$BOT"; fi
if [[ ! -f "$BOT" ]]; then
  echo "Bot script not found: $BOT" >&2
  exit 1
fi

SEED="$(python3 -c 'import re,sys; t=open(sys.argv[1]).read(); m=re.search(r"^options: seed=(-?\d+)",t,re.M); print(m.group(1) if m else "")' "$LOG")"
if [[ -z "$SEED" ]]; then
  echo "Could not read the original seed from $LOG" >&2
  exit 1
fi

CODINGAME_REPLAY_LOG="$LOG" CODINGAME_REPLAY_AGENT="$PLAYER_INDEX" \
  "$ROOT/run-local-match.sh" "$SEED" "$BOT" "$ROOT/scripts/replay_agent.py" 1 0
