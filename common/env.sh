#!/usr/bin/env bash
# À sourcer: définit COMMON_DIR, REPO_ROOT, MVN et la fonction cg() (API CodinGame).
COMMON_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$COMMON_DIR")"
TOOLS_DIR="$REPO_ROOT/.tools"
MAVEN_VERSION="3.9.11"
MVN="$TOOLS_DIR/apache-maven-$MAVEN_VERSION/bin/mvn"
CG_API="https://www.codingame.com/api/v1"
CG_TOKEN_FILE="${CG_TOKEN_FILE:-$HOME/.config/codingame/token}"

# Usage: cg [curl args] URL ; le token n'est jamais affiché.
cg() { curl -s -H "Authorization: Bearer $(cat "$CG_TOKEN_FILE")" "$@"; }
