#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REFEREE="$ROOT/vendor/TryAngle-Catch"
MAVEN="$ROOT/.tools/apache-maven-3.9.11/bin/mvn"

if [[ ! -x "$MAVEN" ]]; then
  echo "Local Maven is missing: $MAVEN" >&2
  exit 1
fi

"$MAVEN" -q -o -f "$REFEREE/pom.xml" compile dependency:copy-dependencies \
  -DincludeScope=runtime \
  -DoutputDirectory="$REFEREE/target/dependency"

echo "Local referee build is ready."
