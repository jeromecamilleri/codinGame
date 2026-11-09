#!/usr/bin/env bash
# Usage: ./run-local.sh [bot.py] [N ...]   (N = numéro de test 1..24, défaut: tous)
set -euo pipefail
cd "$(dirname "$0")"
BOT="${1:-bot_v1.py}"; shift || true
[ -f "$BOT" ] || { echo "Bot introuvable: $BOT (usage: $0 bot.py [N ...])"; exit 1; }
[ $# -eq 0 ] && set -- $(seq 1 24)
TESTS=(); for n in "$@"; do TESTS+=("$PWD/vendor/referee/config/test$n.json"); done
../common/run_solo_referee.sh batch vendor/referee "$BOT" "${TESTS[@]}" 2>&1 | grep -v '^SLF4J'
