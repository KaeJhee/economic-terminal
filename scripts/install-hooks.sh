#!/bin/sh
# Point this clone at .githooks. Git does not do this on clone.
set -eu
cd "$(dirname "$0")/.."
git config core.hooksPath .githooks
chmod +x .githooks/pre-push scripts/scan-secrets.sh scripts/run-stats-tests.mjs
echo "This clone will run .githooks/pre-push before git push."
echo "Other clones stay unchanged until they run this script."
