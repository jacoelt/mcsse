# Tag Search Combobox Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the static 30-item tag checkbox list in the search filters with a searchable combobox that renders selected tags as removable chips.

**Architecture:** Introduce a new presentational React component `TagCombobox` that owns its local UI state (open/close, typed query) but keeps selected tags lifted to `SearchFilters` via an `onChange(names[])` callback. The combobox renders chips and an input inside a single bordered box, plus a dropdown panel below. Filtering, selection toggling, and outside-click-close are all handled client-side. No backend changes — the existing `/api/servers/?tags=a,b` contract is preserved.

**Tech Stack:** React 18 (hooks), Tailwind CSS. Test runners: Django `manage.py test` for backend regression only (no frontend component tests exist in this project).

**Spec:** `docs/superpowers/specs/2026-04-20-tag-search-combobox-design.md`

---

## File Structure

**Create:**
- `front/src/components/TagCombobox.jsx` — self-contained combobox with chips and filterable dropdown.

**Modify:**
- `front/src/components/SearchFilters.jsx` — replace lines 147–172 (`{/* Tags */}` block) with a `<TagCombobox ... />` instance. Parse/join the comma-separated `params.tags` string at this boundary.

**Unchanged (but relied upon):**
- `front/src/api/client.js` — `fetchFilters()` returns `filters.tags` as `[{ name, display_name, count }]`.
- `back/core/views.py` — the `/api/servers/` endpoint already filters by comma-separated tag names.

---

## Task 1: Baseline — verify repo is green before changes

**Files:** none

- [ ] **Step 1: Run the backend test suite as a baseline**

Run (from repo root):
```bash
cd back && source venv/Scripts/activate && python manage.py test core.tests fetcher.tests
```
Expected: all tests pass. If anything fails, STOP and report the failure per `CLAUDE.md`. Do not proceed.

- [ ] **Step 2: Confirm the current tag filter works in the browser**

Run (in a second terminal, from repo root):
```bash
cd front && npm install
npm run dev
```
Open the URL shown in the terminal. Confirm the Tags block on the left shows a vertical list of checkboxes capped at 30 tags and that checking one updates the server results. Stop the dev server when done (Ctrl+C) unless you want to leave it running for later visual checks.

---

## Task 2: Create `TagCombobox` skeleton with chips and input (no dropdown yet)

**Files:**
- Create: `front/src/components/TagCombobox.jsx`

- [ ] **Step 1: Create the file with a minimal chip-and-input render**

Create `front/src/components/TagCombobox.jsx` with the following content:

```jsx
import { useState, useRef, useEffect } from 'react'

export default function TagCombobox({ tags, selectedNames, onChange }) {
  const [query, setQuery] = useState('')
  const selectedSet = new Set(selectedNames)

  const selectedTags = tags.filter(t => selectedSet.has(t.name))

  function removeTag(name) {
    onChange(selectedNames.filter(n => n !== name))
  }

  return (
    <div>
      <label className="block text-xs font-medium text-gray-400 mb-1">Tags</label>
      <div className="bg-gray-700 border border-gray-600 rounded px-2 py-1.5 focus-within:border-emerald-500">
        <div className="flex flex-wrap items-center gap-1">
          {selectedTags.map(tag => (
            <span
              key={tag.name}
              className="inline-flex items-center gap-1 bg-emerald-600/30 text-emerald-200 border border-emerald-600/50 rounded px-2 py-0.5 text-xs"
            >
              {tag.display_name}
              <button
                type="button"
                onClick={() => removeTag(tag.name)}
                className="hover:text-white"
                aria-label={`Remove ${tag.display_name}`}
              >
                ×
              </button>
            </span>
          ))}
          <input
            type="text"
            value={query}
            onChange={e => setQuery(e.target.value)}
            placeholder={selectedTags.length === 0 ? 'Search tags...' : ''}
            className="flex-1 min-w-[6rem] bg-transparent text-sm text-gray-200 placeholder-gray-500 focus:outline-none"
          />
        </div>
      </div>
    </div>
  )
}
```

- [ ] **Step 2: Smoke-test the skeleton by rendering it in isolation**

Temporarily edit `front/src/components/SearchFilters.jsx` so the existing Tags block is immediately preceded by this smoke-test block (keep the old block in place — this is purely additive for the smoke test):

```jsx
import TagCombobox from './TagCombobox'
```
(Add the import near the top, next to the existing `LogRangeSlider` import.)

Inside the returned JSX, directly above the existing `{/* Tags */}` block, add:

```jsx
{/* TEMP smoke test */}
<TagCombobox
  tags={filters.tags || []}
  selectedNames={params.tags ? params.tags.split(',') : []}
  onChange={names => set('tags', names.join(','))}
/>
```

Run `npm run dev` if not already running, reload the page, and confirm:
- The bordered box renders above the old Tags list.
- Any tag names already in `params.tags` show up as chips.
- Clicking a chip's `×` removes it from the chip row and removes the filter from the server list.
- Typing in the input does not yet filter anything (expected — dropdown comes next).

- [ ] **Step 3: Remove the smoke-test block and keep the import**

Undo the temporary JSX insertion added in Step 2 but leave the `import TagCombobox from './TagCombobox'` line in place (it will be used in Task 6). The old `{/* Tags */}` block stays for now.

- [ ] **Step 4: Commit**

```bash
git add front/src/components/TagCombobox.jsx front/src/components/SearchFilters.jsx
git commit -m "feat(ui): add TagCombobox skeleton with chips and input"
```

---

## Task 3: Add the dropdown panel that lists all tags

**Files:**
- Modify: `front/src/components/TagCombobox.jsx`

- [ ] **Step 1: Extend the component to render a dropdown (always open for now)**

Replace the entire contents of `front/src/components/TagCombobox.jsx` with:

```jsx
import { useState, useRef, useEffect } from 'react'

export default function TagCombobox({ tags, selectedNames, onChange }) {
  const [query, setQuery] = useState('')
  const [open, setOpen] = useState(true) // always open for this task; wired up in Task 4
  const selectedSet = new Set(selectedNames)
  const selectedTags = tags.filter(t => selectedSet.has(t.name))

  function removeTag(name) {
    onChange(selectedNames.filter(n => n !== name))
  }

  function toggleTag(name) {
    if (selectedSet.has(name)) {
      onChange(selectedNames.filter(n => n !== name))
    } else {
      onChange([...selectedNames, name])
    }
  }

  return (
    <div>
      <label className="block text-xs font-medium text-gray-400 mb-1">Tags</label>
      <div className="relative">
        <div className="bg-gray-700 border border-gray-600 rounded px-2 py-1.5 focus-within:border-emerald-500">
          <div className="flex flex-wrap items-center gap-1">
            {selectedTags.map(tag => (
              <span
                key={tag.name}
                className="inline-flex items-center gap-1 bg-emerald-600/30 text-emerald-200 border border-emerald-600/50 rounded px-2 py-0.5 text-xs"
              >
                {tag.display_name}
                <button
                  type="button"
                  onClick={() => removeTag(tag.name)}
                  className="hover:text-white"
                  aria-label={`Remove ${tag.display_name}`}
                >
                  ×
                </button>
              </span>
            ))}
            <input
              type="text"
              value={query}
              onChange={e => setQuery(e.target.value)}
              placeholder={selectedTags.length === 0 ? 'Search tags...' : ''}
              className="flex-1 min-w-[6rem] bg-transparent text-sm text-gray-200 placeholder-gray-500 focus:outline-none"
            />
          </div>
        </div>

        {open && (
          <div className="absolute left-0 right-0 mt-1 bg-gray-800 border border-gray-700 rounded max-h-64 overflow-y-auto z-10">
            {tags.length === 0 ? (
              <div className="px-2 py-1.5 text-sm text-gray-500">No tags found</div>
            ) : (
              tags.map(tag => {
                const isSelected = selectedSet.has(tag.name)
                return (
                  <button
                    key={tag.name}
                    type="button"
                    onClick={() => toggleTag(tag.name)}
                    className={`w-full flex items-center gap-2 px-2 py-1.5 text-sm text-left ${
                      isSelected
                        ? 'bg-emerald-600/20 text-emerald-200'
                        : 'text-gray-300 hover:bg-gray-700'
                    }`}
                  >
                    <span className="w-4 inline-block">{isSelected ? '✓' : ''}</span>
                    <span className="flex-1">{tag.display_name}</span>
                    <span className="text-xs text-gray-500">({tag.count})</span>
                  </button>
                )
              })
            )}
          </div>
        )}
      </div>
    </div>
  )
}
```

- [ ] **Step 2: Smoke-test the dropdown**

Re-add the temporary block from Task 2 Step 2 to `SearchFilters.jsx` (just above the existing `{/* Tags */}` block), run the dev server, and confirm:
- The dropdown is visible below the input.
- Every tag from `filters.tags` is listed.
- Selected tags render with a checkmark and emerald styling.
- Clicking an unselected row adds a chip and the row becomes selected (checkmark appears).
- Clicking a selected row removes the chip and the row becomes unselected.

Remove the temporary block again before continuing.

- [ ] **Step 3: Commit**

```bash
git add front/src/components/TagCombobox.jsx
git commit -m "feat(ui): add dropdown panel to TagCombobox"
```

---

## Task 4: Add open/close behavior (focus-to-open, outside-click-to-close)

**Files:**
- Modify: `front/src/components/TagCombobox.jsx`

- [ ] **Step 1: Replace the `open` state wiring so it starts closed and reacts to focus and outside clicks**

In `front/src/components/TagCombobox.jsx`, change:

```jsx
const [open, setOpen] = useState(true) // always open for this task; wired up in Task 4
```

to:

```jsx
const [open, setOpen] = useState(false)
const rootRef = useRef(null)

useEffect(() => {
  function handleMouseDown(e) {
    if (rootRef.current && !rootRef.current.contains(e.target)) {
      setOpen(false)
    }
  }
  document.addEventListener('mousedown', handleMouseDown)
  return () => document.removeEventListener('mousedown', handleMouseDown)
}, [])
```

Then wire the ref and open-on-interaction handlers. The component currently starts with:

```jsx
return (
  <div>
    <label className="block text-xs font-medium text-gray-400 mb-1">Tags</label>
```

Change the outermost `<div>` (the one wrapping the `<label>` and the `<div className="relative">` below it) to:

```jsx
return (
  <div ref={rootRef} onClick={() => setOpen(true)}>
    <label className="block text-xs font-medium text-gray-400 mb-1">Tags</label>
```

And add `onFocus={() => setOpen(true)}` to the `<input>` element so tabbing into it also opens the dropdown:

```jsx
<input
  type="text"
  value={query}
  onChange={e => setQuery(e.target.value)}
  onFocus={() => setOpen(true)}
  placeholder={selectedTags.length === 0 ? 'Search tags...' : ''}
  className="flex-1 min-w-[6rem] bg-transparent text-sm text-gray-200 placeholder-gray-500 focus:outline-none"
/>
```

- [ ] **Step 2: Smoke-test open/close**

Re-add the temporary smoke-test block from Task 2 Step 2 and confirm:
- On initial render, the dropdown is closed.
- Clicking anywhere inside the bordered box opens the dropdown.
- Focusing the input (via Tab) opens the dropdown.
- Clicking elsewhere on the page closes it.
- Clicking a dropdown row does not close the dropdown (the click is inside `rootRef`).
- Clicking a chip's `×` does not close the dropdown.

Remove the temporary block before continuing.

- [ ] **Step 3: Commit**

```bash
git add front/src/components/TagCombobox.jsx
git commit -m "feat(ui): open TagCombobox on focus, close on outside click"
```

---

## Task 5: Filter the dropdown by the typed query

**Files:**
- Modify: `front/src/components/TagCombobox.jsx`

- [ ] **Step 1: Compute filtered tag list**

In `front/src/components/TagCombobox.jsx`, just above the `return (` line, add:

```jsx
const q = query.trim().toLowerCase()
const filteredTags = q === ''
  ? tags
  : tags.filter(t =>
      t.display_name.toLowerCase().includes(q) ||
      t.name.toLowerCase().includes(q)
    )
```

Then, in the dropdown `{open && (...)}` block, replace every use of `tags` with `filteredTags`. After the change, the dropdown block looks like:

```jsx
{open && (
  <div className="absolute left-0 right-0 mt-1 bg-gray-800 border border-gray-700 rounded max-h-64 overflow-y-auto z-10">
    {filteredTags.length === 0 ? (
      <div className="px-2 py-1.5 text-sm text-gray-500">No tags found</div>
    ) : (
      filteredTags.map(tag => {
        const isSelected = selectedSet.has(tag.name)
        return (
          <button
            key={tag.name}
            type="button"
            onClick={() => toggleTag(tag.name)}
            className={`w-full flex items-center gap-2 px-2 py-1.5 text-sm text-left ${
              isSelected
                ? 'bg-emerald-600/20 text-emerald-200'
                : 'text-gray-300 hover:bg-gray-700'
            }`}
          >
            <span className="w-4 inline-block">{isSelected ? '✓' : ''}</span>
            <span className="flex-1">{tag.display_name}</span>
            <span className="text-xs text-gray-500">({tag.count})</span>
          </button>
        )
      })
    )}
  </div>
)}
```

- [ ] **Step 2: Smoke-test filtering**

Re-add the temporary smoke-test block, run the dev server, and confirm:
- Typing a substring present in at least one tag narrows the list.
- Typing something with no matches shows the "No tags found" row.
- Clearing the input restores the full list.
- Selecting a filtered tag still works; the chip is added and the typed query stays intact.

Remove the temporary block before continuing.

- [ ] **Step 3: Commit**

```bash
git add front/src/components/TagCombobox.jsx
git commit -m "feat(ui): filter TagCombobox dropdown by typed query"
```

---

## Task 6: Wire `TagCombobox` into `SearchFilters` and remove the old checkbox list

**Files:**
- Modify: `front/src/components/SearchFilters.jsx`

- [ ] **Step 1: Replace the old Tags block with the new component**

In `front/src/components/SearchFilters.jsx`, remove lines 147–172 (the block starting with `{/* Tags */}` and ending with the closing `</div>` of that block) and replace it with:

```jsx
        <TagCombobox
          tags={filters.tags || []}
          selectedNames={params.tags ? params.tags.split(',').filter(Boolean) : []}
          onChange={names => set('tags', names.length > 0 ? names.join(',') : undefined)}
        />
```

Confirm the `import TagCombobox from './TagCombobox'` line added in Task 2 is still present near the top of the file. If it was removed, re-add it next to the `LogRangeSlider` import.

- [ ] **Step 2: Smoke-test the integrated behavior**

Start the dev server if not already running:
```bash
cd front && npm run dev
```
Open the search page and confirm:
- The old vertical checkbox list is gone.
- The new combobox appears in the same spot.
- Selecting a tag in the combobox narrows the server results below.
- Selecting additional tags further narrows the results (AND semantics, same as before).
- Removing all chips removes the `tags` query param (results return to unfiltered).
- Refreshing the page with `?tags=survival,pvp` in the URL shows both chips pre-selected.

- [ ] **Step 3: Commit**

```bash
git add front/src/components/SearchFilters.jsx
git commit -m "feat(ui): replace tag checkbox list with TagCombobox"
```

---

## Task 7: Final verification

**Files:** none

- [ ] **Step 1: Re-run the backend test suite**

Run:
```bash
cd back && source venv/Scripts/activate && python manage.py test core.tests fetcher.tests
```
Expected: all tests pass. (Backend was not touched; this is a belt-and-suspenders check per `CLAUDE.md`.)

- [ ] **Step 2: Manual regression walk-through**

With `npm run dev` running, perform the full scenario end-to-end in the browser:
1. Load the page clean (no `tags=` in URL).
2. Click the combobox — dropdown opens, all tags listed.
3. Type a query, confirm filter works.
4. Click two tags — both become chips with checkmarks in dropdown.
5. Remove one via its chip `×` — its dropdown row unchecks.
6. Remove the other via the dropdown row itself — chip disappears.
7. Click outside the combobox — dropdown closes.
8. Click "Reset filters" — any remaining chips clear.

- [ ] **Step 3: Close the GitHub issue reference**

This work addresses issue #4. Mention that in the PR description when one is opened. Do not auto-close the issue from a commit (per the user's git/PR preferences).
