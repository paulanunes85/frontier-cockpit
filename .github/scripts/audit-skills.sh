#!/usr/bin/env bash
# Audit every skill under .github/skills against the repository's authoring
# conventions. High-signal checks only (no false positives): frontmatter on
# line 1, name matches folder, required keys present, and no sandbox paths.
# Exits non-zero if any check fails. Used by .vscode/tasks.json and CI.
set -u

# Resolve repo root from this script's location (.github/scripts/).
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SKILLS_DIR="$ROOT/.github/skills"
fail=0

if [ ! -d "$SKILLS_DIR" ]; then
  echo "No .github/skills directory; nothing to audit."
  exit 0
fi

for dir in "$SKILLS_DIR"/*/; do
  skill="$(basename "$dir")"
  f="$dir/SKILL.md"

  if [ ! -f "$f" ]; then
    echo "FAIL [$skill] missing SKILL.md"
    fail=1
    continue
  fi

  # 1. Frontmatter must start on line 1.
  if [ "$(head -1 "$f")" != "---" ]; then
    echo "FAIL [$skill] frontmatter not on line 1"
    fail=1
  fi

  # 2. name key present and equal to the folder name.
  name="$(awk -F': *' '/^name:/{print $2; exit}' "$f" | tr -d '"'"'"' ')"
  if [ -z "$name" ]; then
    echo "FAIL [$skill] missing 'name' in frontmatter"
    fail=1
  elif [ "$name" != "$skill" ]; then
    echo "FAIL [$skill] name '$name' does not match folder"
    fail=1
  fi

  # 3. description key present.
  if ! grep -q '^description:' "$f"; then
    echo "FAIL [$skill] missing 'description' in frontmatter"
    fail=1
  fi
done

# 4. No sandbox path leaks anywhere in the skills tree.
if grep -rnI "/home/claude\|/mnt/skills\|/mnt/user-data" "$SKILLS_DIR" >/dev/null 2>&1; then
  echo "FAIL sandbox path leak(s) found:"
  grep -rnI "/home/claude\|/mnt/skills\|/mnt/user-data" "$SKILLS_DIR"
  fail=1
fi

if [ "$fail" -eq 0 ]; then
  echo "All skill checks passed."
fi
exit "$fail"
