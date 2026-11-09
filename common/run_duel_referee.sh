#!/usr/bin/env bash
# Lanceur générique pour un referee à 2 joueurs (MultiplayerGameRunner).
# Usage: run_duel_referee.sh view|batch <dossier-referee> <niveau-ligue> <seed> <port> <bot0.py> <bot1.py>
#   view  -> visualiseur http://localhost:PORT/test.html ; batch -> une ligne RESULT (scores)
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/env.sh"

MODE="$1"; REF="$(cd "$2" && pwd)"; LEVEL="$3"; SEED="$4"; PORT="$5"; B0="$(realpath "$6")"; B1="$(realpath "$7")"
CP="$("$COMMON_DIR/referee_classpath.sh" "$REF")"
BUILD="$COMMON_DIR/.build"
mkdir -p "$BUILD"
javac -cp "$CP" -d "$BUILD" "$COMMON_DIR/java/LocalDuel.java"
cd "$REF"
java --add-opens=java.base/java.lang=ALL-UNNAMED -cp "$BUILD:$CP" LocalDuel "$MODE" "$LEVEL" "$SEED" "$PORT" "python3 $B0" "python3 $B1"
