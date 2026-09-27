#!/bin/sh
# Scan text for credential-shaped strings.
# Usage:
#   scripts/scan-secrets.sh              # tracked files, excluding vendor/
#   scripts/scan-secrets.sh --stdin name # scan stdin; "name" is the label
#   scripts/scan-secrets.sh --self-test
# The settings placeholder sk-or-... does not match. Install the git hook
# with scripts/install-hooks.sh. Git does not turn the hook on by itself.

set -eu

or_pat='sk-or-v1-[A-Za-z0-9]{20,}'
ant_pat='sk-ant-[A-Za-z0-9_-]{20,}'
aws_pat='AKIA[0-9A-Z]{16}'
gh_pat='ghp_[A-Za-z0-9]{20,}'
pat_pat='github_pat_[A-Za-z0-9_]{20,}'
slack_pat='xox[baprs]-[A-Za-z0-9-]{10,}'
key_pat='(api[_-]?key|apikey)[[:space:]]*[=:][[:space:]]*['"'"'\"]?[A-Za-z0-9]{32,}'
priv=$(printf '%s%s' '-----BEGIN ' 'PRIVATE KEY-----')

scan_stream() {
  label=$1
  # grep -E returns 1 when there is no match. That is success for a scanner.
  if grep -nE -e "$or_pat" -e "$ant_pat" -e "$aws_pat" -e "$gh_pat" -e "$pat_pat" -e "$slack_pat" -e "$key_pat" -e "$priv" > /tmp/gs-secret-hits.$$ 2>/dev/null; then
    echo "secret-scan: match in $label" >&2
    # printf, not sed: a path label contains slashes, which break s/^/label/.
    while IFS= read -r line || [ -n "$line" ]; do
      printf '%s:%s\n' "$label" "$line" >&2
    done < /tmp/gs-secret-hits.$$
    rm -f /tmp/gs-secret-hits.$$
    return 1
  fi
  rm -f /tmp/gs-secret-hits.$$
  return 0
}

if [ "${1:-}" = "--self-test" ]; then
  fail=0
  # Built at runtime. A literal token of this shape in this file is a hit
  # when the repo scan reads the script.
  sample=$(printf '%s%s' 'sk-or-v1-abc' 'defghijklmnopqrstuv')
  set +e
  report=$(printf '%s\n' "$sample" | scan_stream 'scripts/scan-secrets.sh' 2>&1)
  status=$?
  set -e
  if [ "$status" -eq 0 ]; then
    echo "secret-scan self-test: sample key was not detected" >&2
    fail=1
  fi
  case "$report" in
    *'scripts/scan-secrets.sh:'*"$sample"*) ;;
    *)
      echo "secret-scan self-test: slash path was not reported" >&2
      fail=1
      ;;
  esac
  case "$report" in
    *'unknown option'*)
      echo "secret-scan self-test: reporter crashed" >&2
      fail=1
      ;;
  esac
  printf '%s\n' 'sk-or-...' | scan_stream probe || fail=1
  printf '%s\n' 'placeholder api_key=YOUR_FRED_KEY' | scan_stream probe || fail=1
  if [ "$fail" -ne 0 ]; then
    echo "secret-scan self-test failed" >&2
    exit 1
  fi
  echo "secret-scan self-test ok"
  exit 0
fi

if [ "${1:-}" = "--stdin" ]; then
  scan_stream "${2:-stdin}"
  exit $?
fi

root=$(git rev-parse --show-toplevel)
cd "$root"
fail=0
git ls-files | while IFS= read -r f; do
  case "$f" in
    vendor/*|*.png|*.jpg|*.gif|*.pdf|*.min.js) continue ;;
  esac
  [ -f "$f" ] || continue
  # Skip binary-looking files.
  if grep -q $'\0' "$f" 2>/dev/null; then
    continue
  fi
  if ! scan_stream "$f" < "$f"; then
    echo "$f" >> /tmp/gs-secret-fail.$$
  fi
done
if [ -s /tmp/gs-secret-fail.$$ ]; then
  rm -f /tmp/gs-secret-fail.$$
  exit 1
fi
rm -f /tmp/gs-secret-fail.$$
echo "secret-scan: no matches"
exit 0
