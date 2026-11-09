#!/usr/bin/env bash
# Usage: referee_classpath.sh <dossier-referee>
# Compile le referee (Maven partagé) et affiche son classpath complet (mis en cache dans .classpath).
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/env.sh"

REF="$(cd "$1" && pwd)"
[[ -x "$MVN" ]] || "$COMMON_DIR/setup-tools.sh" >&2
if [[ ! -s "$REF/.classpath" || ! -d "$REF/target/classes" || "$REF/pom.xml" -nt "$REF/.classpath" ]]; then
  "$MVN" -q -f "$REF/pom.xml" compile dependency:build-classpath \
    -Dmdep.outputFile="$REF/.classpath" >&2
fi
echo "$REF/target/classes:$(cat "$REF/.classpath")"
