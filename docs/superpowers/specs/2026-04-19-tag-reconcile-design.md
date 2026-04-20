# Tag Reconciliation Design

**Date:** 2026-04-19
**Status:** Approved for implementation planning
**Scope:** Add reconciliation logic that collapses semantically-similar tags into a canonical set across the ingest pipeline and existing DB data.

---

## Problem

`core.models.Tag` currently stores 873 rows. The only dedup mechanism is `slugify(tag_name.lower().strip())`, which catches case variants (`PvP` == `pvp`) but misses:

- **Separator/spacing noise** — `bed-wars` / `bedwars` / `bed wars`, `box-pvp` / `boxpvp`, `classicprison` / `classic-prison`
- **Plural/singular** — `auction`/`auctions`, `clan`/`clans`, `boss`/`bosses`
- **Abbreviations & synonyms** — `ctf` ↔ `capture-the-flag`, `bedw` ↔ `bedwars`
- **Typos** — `beadrock`, `bulding`, plus encoding garbage like `Crack�`
- **Other languages** — `aventura`, `anarquia`, `brasileiro`, `creatif`
- **Junk / noise** — `amazing`, `awesome`, `any`, `all`, `and-higher`, bare version numbers (`1710`, `12160`, `118`)

The result is a polluted filter facet that degrades the search UX.

## Goals

- Deterministic mapping of raw scraped tag strings to a canonical set.
- Applied identically at ingest time (every fetch) and as a one-shot cleanup over existing data.
- Re-runnable when rules evolve (new aliases, new stopwords).
- Rules live in code, reviewed via normal PR flow.

## Non-goals

- Fuzzy / Levenshtein / embedding-based similarity.
- Admin UI for editing rules.
- Auto-suggesting new aliases from the tag table.

---

## Design

### 1. Normalization pipeline

Pure function `fetcher.tag_rules.normalize_tag(raw: str) -> str | None`. Returns a canonical slug, or `None` if the tag should be dropped.

Steps, in order:

1. **Strip + lowercase** — `"  PvP Server  "` → `"pvp server"`.
2. **Unicode normalize (NFKD) + drop non-ASCII** — `"créatif"` → `"creatif"`; drops `�` and similar encoding garbage.
3. **Remove all non-alphanumerics** — `"pvp server"` → `"pvpserver"`, `"bed-wars"` → `"bedwars"`. (Aggressive collapse chosen to fold the majority of real duplication without requiring large alias tables.)
4. **Bare-numeric drop** — if the result is all digits (e.g. `"1710"`, `"12160"`), return `None`. These are mangled Minecraft versions and duplicate the existing `Server.game_version` field.
5. **Empty check** — if the result is empty, return `None`.
6. **Stopword check** — if result is in `STOPWORDS`, return `None`.
7. **Alias lookup** — if result is a key in `ALIASES`, replace with its value.
8. **Singularize** via `inflect.engine().singular_noun(x) or x` — `"bosses"` → `"boss"`, `"clans"` → `"clan"`. `inflect` returns `False` when already singular; fall back to the input.
9. **Second stopword check** — singularization could produce a stopword.
10. **Second alias lookup** — singularization could produce an aliased form.
11. Return the result.

Alias keys and values are themselves already-normalized strings (lowercase, alphanumeric only) so that the map stays stable regardless of how the raw input is formatted.

**Alias lookup is single-step, not transitive.** A value must not also be a key. Enforced by a unit test: `assert not (ALIASES.keys() & set(ALIASES.values()))`.

### 2. Rules module

New file `back/fetcher/tag_rules.py`:

```python
import re
import unicodedata

import inflect

_inflect = inflect.engine()

STOPWORDS: frozenset[str] = frozenset({
    # Populated by reviewing current 873-tag table. Expected size: 30-60.
    "all", "any", "amazing", "awesome", "andhigher", "andmore",
    # ... full list seeded before first run, user-reviewed
})

ALIASES: dict[str, str] = {
    # Keys and values are post-normalization (lowercase, alphanumeric only).
    "bedw": "bedwars",
    "bedwar": "bedwars",
    "ctf": "capturetheflag",
    "aventura": "adventure",
    "anarquia": "anarchy",
    "brasileiro": "brazilian",
    # ... full list seeded before first run, user-reviewed
}

DISPLAY_OVERRIDES: dict[str, str] = {
    "pvp": "PvP",
    "pve": "PvE",
    "ctf": "CTF",
    "capturetheflag": "Capture the Flag",
    "smp": "SMP",
    "rpg": "RPG",
    "bedwars": "Bed Wars",
    # ... seeded as needed
}


def normalize_tag(raw: str) -> str | None:
    if not raw:
        return None
    x = raw.strip().lower()
    x = unicodedata.normalize("NFKD", x)
    x = x.encode("ascii", "ignore").decode("ascii")
    x = re.sub(r"[^a-z0-9]", "", x)
    if not x or x.isdigit():
        return None
    if x in STOPWORDS:
        return None
    x = ALIASES.get(x, x)
    singular = _inflect.singular_noun(x)
    if singular:
        x = singular
    if x in STOPWORDS:
        return None
    x = ALIASES.get(x, x)
    return x or None


def display_name_for(canonical: str) -> str:
    if canonical in DISPLAY_OVERRIDES:
        return DISPLAY_OVERRIDES[canonical]
    return canonical.title()
```

**Why three structures instead of one:** `STOPWORDS` is "drop"; `ALIASES` is "rewrite"; `DISPLAY_OVERRIDES` is a separate UX concern (the default `.title()` of `bedwars` is ugly — users read `Bed Wars`).

**Seeded content:** before implementation, the three dicts are pre-populated by reviewing the current 873-tag table. The user reviews the diff of the seed data before the migration command is run.

### 3. Ingest integration

Two small changes in `fetcher/reconciler.py`:

**`_merge_entries`:**

```python
from .tag_rules import normalize_tag

# replaces: result["tags"].add(tag.lower().strip())
for tag in server.tags:
    canonical = normalize_tag(tag)
    if canonical:
        result["tags"].add(canonical)
```

**`_sync_tags`:**

```python
from .tag_rules import display_name_for

# replaces the slugify()-based path
for slug in tag_names:
    tag, _ = Tag.objects.get_or_create(
        name=slug,
        defaults={"display_name": display_name_for(slug)},
    )
    tag_objects.append(tag)
```

The set passed to `_sync_tags` now contains canonical slugs only, so `get_or_create` keys cleanly. Existing Tag rows' `display_name` is preserved (never overwritten on re-sync) — the override only applies when creating a new Tag.

Every new fetch cycle produces only canonical tags. The DB can only grow with canonical-named Tag rows (plus the legacy 873 until they are cleaned by the migration command).

### 4. Migration command

New management command `back/fetcher/management/commands/reconcile_tags.py`. Re-runnable any time `tag_rules.py` changes.

**Algorithm** (single `transaction.atomic()` block):

1. Load every `Tag` into memory.
2. For each tag, compute `normalize_tag(tag.name)`:
   - `None` → mark for delete (stopword / bare-numeric / unicode noise).
   - Equal to `tag.name` → keep as canonical.
   - Different from `tag.name` → mark to merge into the canonical Tag with that slug. If no existing tag has the canonical name, and only this one source tag maps to it, **rename** the source tag in place (`UPDATE tag SET name=..., display_name=...`) — no M2M moves needed. Otherwise merge all sources into the existing-or-newly-created canonical Tag.
3. Execute:
   - **Merges:** for each `(source_tag_id, target_tag_id)` pair, move `Server.tags.through` rows from source to target, skipping rows where a `(server_id, target_tag_id)` row already exists (avoid the M2M unique-constraint violation). Then delete the source Tag.
   - **Deletes:** bulk-delete `Server.tags.through` rows for all to-delete tag ids, then bulk-delete the Tags.

**Reference implementation sketch:**

```python
with transaction.atomic():
    through = Server.tags.through

    # Merges
    for source_id, target_id in merges:
        through.objects.filter(tag_id=source_id).exclude(
            server_id__in=through.objects.filter(tag_id=target_id).values("server_id")
        ).update(tag_id=target_id)
        through.objects.filter(tag_id=source_id).delete()
        Tag.objects.filter(id=source_id).delete()

    # Deletes
    through.objects.filter(tag_id__in=delete_ids).delete()
    Tag.objects.filter(id__in=delete_ids).delete()
```

**CLI:**

```
python manage.py reconcile_tags             # execute
python manage.py reconcile_tags --dry-run   # plan summary only, no writes
python manage.py reconcile_tags -v 2        # per-tag action log
```

**Dry-run output format:**

```
873 tags analyzed:
  412 keep as-is
  287 merge    (e.g. bed-wars → bedwars, clans → clan, aventura → adventure)
  174 delete   (stopwords + bare numeric version tags)
After: ~586 canonical tags
```

### 5. Testing

**`back/fetcher/tests/test_tag_rules.py`** — table-driven unit tests for `normalize_tag`:

```python
cases = [
    ("PvP",               "pvp"),
    ("  Bed Wars  ",      "bedwars"),
    ("bed-wars",          "bedwars"),
    ("bedwars",           "bedwars"),
    ("bedw",              "bedwars"),         # alias
    ("créatif",           "creative"),        # unicode + alias
    ("Crack\ufffd",       "cracked"),         # strip garbage, then alias
    ("auctions",          "auction"),         # singularize
    ("bosses",            "boss"),
    ("ctf",               "capturetheflag"),  # alias
    ("amazing",           None),              # stopword
    ("1710",              None),              # bare version number
    ("aventura",          "adventure"),       # translation
    ("",                  None),
    ("   ",               None),
]
```

**`back/fetcher/tests/test_reconciler.py`** — add:

- `test_tag_plural_normalization`
- `test_tag_stopword_drop`
- `test_tag_alias_rewrite`
- `test_tag_separator_collapse`
- `test_tag_unicode_strip`

Existing `test_tags_are_unioned` continues to pass unchanged.

**`back/fetcher/tests/test_reconcile_tags_command.py`** — migration command tests:

- Plural merge moves M2M relations correctly.
- Stopword removal deletes the Tag and unlinks servers without affecting the servers.
- Duplicate M2M entries post-merge don't violate the unique constraint (the `.exclude(...)` guard).
- `--dry-run` performs zero DB writes.
- Re-running on an already-clean DB is a no-op.

### 6. Manual verification

Steps to perform after implementation, before calling the work done:

1. Full test suite passes: `cd back && source venv/Scripts/activate && python manage.py test core.tests fetcher.tests`.
2. `python manage.py reconcile_tags --dry-run` produces a plan that visually matches the seed rules. User sign-off required.
3. Copy `db.sqlite3` to a backup file.
4. `python manage.py reconcile_tags` — observe count output.
5. Spot-check: `Tag.objects.get(name="bedwars").servers.count()` ≈ sum of pre-merge `bed-wars` + `bedwars` + `bedw` + `bed wars` counts.

---

## Dependencies

- `inflect` (new) — add to `back/requirements.txt`.

## Files touched

**New:**
- `back/fetcher/tag_rules.py`
- `back/fetcher/management/commands/reconcile_tags.py`
- `back/fetcher/tests/test_tag_rules.py`
- `back/fetcher/tests/test_reconcile_tags_command.py`

**Modified:**
- `back/fetcher/reconciler.py` — `_merge_entries` and `_sync_tags` use `normalize_tag` / `display_name_for`.
- `back/fetcher/tests/test_reconciler.py` — five new tests.
- `back/requirements.txt` — add `inflect`.
