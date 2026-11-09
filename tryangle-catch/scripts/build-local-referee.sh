#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REFEREE="$ROOT/vendor/TryAngle-Catch"
source "$ROOT/../common/env.sh"

[[ -x "$MVN" ]] || "$COMMON_DIR/setup-tools.sh"

"$MVN" -q -o -f "$REFEREE/pom.xml" compile dependency:copy-dependencies \
  -DincludeScope=runtime \
  -DoutputDirectory="$REFEREE/target/dependency"

echo "Local referee build is ready."
