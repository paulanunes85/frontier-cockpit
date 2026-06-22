# Consolidating Multiple Skills

Read this when asked to merge, consolidate, or combine existing skills into fewer skills.

## When to Consolidate

Look for these signals that separate skills should be one:

### Strong signals (consolidate)

- **Linear pipeline**: Skill A's output is Skill B's input. Each skill ends with "see Skill B for the next step."
- **Cross-references**: Skills constantly reference each other. Users need to mentally chain 3+ skills for one task.
- **Near-identical scripts**: Two scripts with the same structure, differing only in a flag value or file path.
- **Duplicate files**: Same example YAML, same reference doc, or same version map appearing in multiple skills.
- **Shared prerequisites**: All skills require the same tools, versions, and setup.

### Weak signals (maybe consolidate)

- **Same audience**: All skills target the same persona, but the workflows are genuinely independent.
- **Same domain**: Skills cover the same product/area but handle unrelated concerns (e.g., CI debugging vs local testing).

### Don't consolidate

- **No shared context**: Skills have different prerequisites, different audiences, and no cross-references.
- **Different tools**: One skill uses `acli`, another uses `yarn` — they share nothing but the product name.
- **Different repos**: Skills operate on different repositories with different workflows.

## Consolidation Workflow

### Step 1: Analyze

Before writing any code:

1. Read every SKILL.md in the candidate set.
2. Map the cross-references. Draw the dependency graph — which skills point to which.
3. Inventory shared content: scripts, references, examples, version maps, prerequisites.
4. Count total SKILL.md lines. If the sum exceeds 500 lines, the consolidated skill needs a sub-command router with references.
5. Identify the "seams" — which content becomes the router SKILL.md body and which becomes reference files.

### Step 2: Design the consolidated skill

Choose the architecture:

| Total lines | Approach |
|-------------|----------|
| < 500 | Single SKILL.md, no sub-commands |
| 500–2000 | Sub-command router + reference files per command |
| > 2000 | Consider whether consolidation is the right move |

For sub-command routers:

- Each old skill typically becomes one sub-command with its own `references/<command>.md`.
- Shared setup, prerequisites, and version info go in the SKILL.md body.
- Deep-dive references from the old skills move to `references/` with their original filenames.

### Step 3: Merge scripts

When consolidating near-identical scripts:

1. Diff the scripts. Identify what actually differs (usually a flag value, a directory name, or an optional step).
2. Keep the more mature script's structure (better error handling, more features).
3. Add a `--type` or `--mode` flag to express the variant behavior.
4. Verify both paths still work — run `--help` and test with both `--type` values.
5. **Harmonize patterns between scripts** in the same skill. Watch for:
   - One script checks `NO_COLOR`, the other doesn't
   - One uses `shell=True` on Windows, the other doesn't
   - One checks `stdout.isatty()` but logs to `stderr`
   - Different exit code conventions
   - Different JSON output formats

### Step 4: Consolidate examples

- Diff example files across the old skills. Often 60%+ is identical.
- Create one unified example file with sections for each variant.
- Remove duplicates — one example per pattern, not one per old skill.

### Step 5: Update all consumers

This is where consolidations break. Search the **entire project** for old skill names:

```bash
grep -rn "old-skill-name" --include="*.md" --include="*.py" --include="*.json" --include="*.yaml" --exclude-dir=.git .
```

**Must update:**

| Location | What to change |
|----------|---------------|
| Parent router SKILL.md | Routing table, intake menu numbers, skills index |
| README.md | Skill tables, directory trees, descriptions |
| ADRs / docs | Historical references to old skill names |
| Script docstrings | `--help` text referencing old workflow names |
| Other skills' references | Cross-references like "see the X skill" |
| CI / build configs | Paths to moved files |

**Gotcha: renumber menus.** If a router's intake menu had items 6-9 and you consolidated them into item 6, renumber 10→7, 11→8, etc. Update the routing table to match. Agents parse "pick a number" literally.

### Step 6: Audit reference paths

Reference files use relative paths. After moving files, paths break in subtle ways:

- A reference in `references/export.md` that says `Read references/export-options.md` is wrong — it would resolve to `references/references/export-options.md` from the file's perspective.
- Choose a convention: paths relative to the file, or paths relative to SKILL.md. Document which.
- Be consistent — don't mix conventions within the same skill.

**Recommended convention:** Paths in SKILL.md are relative to SKILL.md. Paths in reference files point to siblings by filename only (e.g., `Read export-options.md (in this directory)`).

### Step 7: Review

Run the standard Phase 5 review checklist from SKILL.md, plus these consolidation-specific checks:

- [ ] No references to old skill names anywhere in the project
- [ ] Router intake menu is sequentially numbered (no gaps)
- [ ] Router routing table numbers match the intake menu
- [ ] Script docstrings and `--help` text reference the new skill name
- [ ] Reference paths resolve correctly from each file's location
- [ ] All example files from old skills are represented in the consolidated examples
- [ ] Scripts in the same skill use consistent patterns (NO_COLOR, shell flags, TTY checks, exit codes)
- [ ] README skill tables and directory trees match the new structure
- [ ] All tests still pass

## Anti-Patterns

### Incomplete grep

Searching for old names in `skills/` only. Old names appear in README, ADRs, CI configs, and script help text. Search the entire project.

### Path assumptions after moves

Copying a reference file without updating its internal relative paths. A file that said `../rhdh/references/versions.md` may need a different path after moving to a new directory.

### Keeping empty directories

After deleting old skills, empty directories or `__pycache__/` may linger. Clean up.

### Forgetting the description

The new consolidated skill's description must cover all trigger phrases from all old skills. Check each old description and verify the new one would trigger for the same queries.
