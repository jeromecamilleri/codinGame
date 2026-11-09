#!/usr/bin/env bash
# Usage: ./run-view.sh [port]  -> visualiseur http://localhost:8888/viewer.html (Ctrl+C pour arrêter)
cd "$(dirname "$0")"
PORT="${1:-8888}"
echo "Ouvrir http://localhost:$PORT/viewer.html"
exec python3 -m http.server "$PORT" --bind 127.0.0.1
