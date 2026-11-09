#!/usr/bin/env bash
# Lanceur générique pour les puzzles/optimisations solo (SoloGameRunner).
# Usage:
#   run_solo_referee.sh batch <dossier-referee> <bot.py> test1.json [test2.json ...]
#   run_solo_referee.sh view  <dossier-referee> <bot.py> test.json [port]   (http://localhost:PORT)
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/env.sh"

MODE="$1"; REF="$(cd "$2" && pwd)"; BOT="$(realpath "$3")"; shift 3
CP="$("$COMMON_DIR/referee_classpath.sh" "$REF")"
BUILD="$COMMON_DIR/.build"
mkdir -p "$BUILD"
javac -cp "$CP" -d "$BUILD" "$COMMON_DIR/java/LocalBatch.java" "$COMMON_DIR/java/LocalView.java"

case "$MODE" in
  batch) java -cp "$BUILD:$CP" LocalBatch "python3 $BOT" "$@" ;;
  # La vue lit ses ressources relativement au dossier du referee.
  view)  cd "$REF"; java -cp "$BUILD:$CP" LocalView "python3 $BOT" "$@" ;;
  *) echo "mode inconnu: $MODE" >&2; exit 1 ;;
esac
