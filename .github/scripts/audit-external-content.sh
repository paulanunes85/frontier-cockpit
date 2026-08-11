#!/usr/bin/env bash
# Audit imported or adapted external GitHub Copilot primitives for provenance,
# license compatibility, and common portability or supply-chain hazards.
set -u

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
GH="$ROOT/.github"
fail=0

err() {
  echo "FAIL [$1] $2"
  fail=1
}

allowed_license() {
  case "$1" in
    MIT|Apache-2.0|BSD-2-Clause|BSD-3-Clause|CC0-1.0) return 0 ;;
    *) return 1 ;;
  esac
}

check_frontmatter_key() {
  local file="$1" key="$2" base="$3"
  awk '/^---$/{c++; next} c==1' "$file" | grep -q "^$key:" || err "$base" "missing '$key' metadata"
}

check_external_file() {
  local file="$1" base license
  base="${file#$ROOT/}"

  if ! awk '/^---$/{c++; next} c==1' "$file" | grep -q '^source:'; then
    return 0
  fi

  check_frontmatter_key "$file" source "$base"
  check_frontmatter_key "$file" source_url "$base"
  check_frontmatter_key "$file" license "$base"
  check_frontmatter_key "$file" imported_date "$base"
  check_frontmatter_key "$file" last_sync "$base"

  license="$(awk -F': *' '/^license:/{print $2; exit}' "$file" | tr -d '"'"'"' ')"
  if [ -n "$license" ] && ! allowed_license "$license"; then
    err "$base" "license '$license' is not in the allowed list"
  fi

  if grep -nE '/home/claude|/mnt/skills|/mnt/user-data|/tmp/[^ ]*secret|api[_-]?key[=:][^$]|token[=:][^$]' "$file" >/dev/null 2>&1; then
    err "$base" "possible sandbox path or secret pattern found"
  fi

  if grep -nE '@latest|curl .*[|] *sh|wget .*[|] *sh' "$file" >/dev/null 2>&1; then
    err "$base" "possible unpinned dependency or pipe-to-shell pattern found"
  fi
}

while IFS= read -r file; do
  check_external_file "$file"
done < <(find "$GH/agents" "$GH/skills" "$GH/prompts" "$GH/instructions" -type f \( -name '*.md' -o -name 'SKILL.md' \) 2>/dev/null | sort)

if [ "$fail" -eq 0 ]; then
  echo "All external content checks passed."
fi
exit "$fail"
