#!/usr/bin/env bash
# Installe les outils partagés (Maven) dans <racine du repo>/.tools si absents.
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/env.sh"

if [[ -x "$MVN" ]]; then
  echo "Maven déjà présent: $MVN"
  exit 0
fi
mkdir -p "$TOOLS_DIR"
URL="https://archive.apache.org/dist/maven/maven-3/$MAVEN_VERSION/binaries/apache-maven-$MAVEN_VERSION-bin.tar.gz"
curl -fsSL "$URL" | tar -xz -C "$TOOLS_DIR"
echo "Maven installé: $MVN"
