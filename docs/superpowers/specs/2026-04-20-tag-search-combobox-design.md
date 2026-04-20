# Tag Search Combobox — Design

**Issue:** [#4 Update tag search](https://github.com/jacoelt/Minecraft-Server-Search-Engine/issues/4)
**Status:** Approved
**Date:** 2026-04-20

## Problem

The tag filter in `SearchFilters.jsx` is a static checkbox list capped at 30 tags with a short scroll area. Users cannot discover or select tags beyond the first 30, and there is no way to search within the tag list.

## Goals

- Users can search the full tag list by typing.
- Selected tags appear as removable chips inside the input box.
- Clicking a tag in the dropdown toggles its selection.
- No backend changes — existing `?tags=a,b` API filter is reused as-is.

## Non-goals

- Keyboard navigation (Enter to add, Arrow keys, Backspace to remove last chip). Can be added later.
- Creating custom tags not returned by `/api/filters/`.
- Changing how tags are derived, normalized, or stored.

## UI

A new component `TagCombobox.jsx` replaces the existing Tags block in `SearchFilters.jsx`.

**Layout (closed):**

```
┌───────────────────────────────────────────┐
│  Tags                                     │
│ ┌───────────────────────────────────────┐ │
│ │ [pvp ×] [survival ×] _type here_      │ │
│ └───────────────────────────────────────┘ │
└───────────────────────────────────────────┘
```

**Layout (open):**

The dropdown renders directly below the input box.

```
┌───────────────────────────────────────────┐
│ ┌───────────────────────────────────────┐ │
│ │ [pvp ×] [survival ×] surv_             │ │
│ └───────────────────────────────────────┘ │
│ ┌───────────────────────────────────────┐ │
│ │ ✓ Survival (124)          ← highlighted│ │
│ │   Survival Games (18)                  │ │
│ │   Surviving Together (3)               │ │
│ └───────────────────────────────────────┘ │
└───────────────────────────────────────────┘
```

**Styling:**

- Outer box: same Tailwind pattern as other inputs (`bg-gray-700 border border-gray-600 rounded`). Becomes border `emerald-500` on focus-within.
- Chips: `bg-emerald-600/30 text-emerald-200 border-emerald-600/50`, small `×` button on the right.
- Input: transparent background, flexes to fill remaining space on the same row as the chips (wrap with `flex flex-wrap gap-1`).
- Dropdown panel: `bg-gray-800 border border-gray-700 rounded max-h-64 overflow-y-auto`, `mt-1`.
- Dropdown row (selected): `bg-emerald-600/20 text-emerald-200` with a checkmark icon on the left.
- Dropdown row (unselected): `text-gray-300 hover:bg-gray-700`, no icon.
- Each row shows `display_name (count)`.

## Behavior

**Open/close:**

- Dropdown opens when the input is focused or the outer box is clicked.
- Dropdown closes when a `mousedown` occurs outside the component. Uses a ref + a `document.addEventListener("mousedown", ...)` added on mount, removed on unmount.
- Selecting a tag does not close the dropdown, so multiple tags can be selected in one interaction.

**Filtering:**

- When the input is empty, every tag in `filters.tags` is shown.
- When the input has text, show every tag whose `display_name` or `name` contains the typed text (case-insensitive substring match). No fuzzy matching.
- When filtering produces zero matches, render a single muted row: `No tags found`.

**Selection:**

- Clicking a dropdown row toggles that tag in the comma-separated `params.tags` string.
  - If the tag was not selected, it is appended.
  - If the tag was selected, it is removed.
- Clicking a chip's `×` removes the tag from `params.tags`.
- Toggling a tag never clears the typed search text.
- Selected tags still appear in the dropdown, rendered with the "selected" styling and a checkmark.

## Data flow

No API or backend changes.

- `SearchFilters.jsx` continues to own `params.tags` (comma-separated string) and passes it down.
- `TagCombobox` receives:
  - `tags`: the `filters.tags` array from `/api/filters/` — each item has `{ name, display_name, count }`.
  - `selectedNames`: array of selected tag `name`s (parsed from `params.tags`).
  - `onChange(nextNames)`: callback that receives the updated array of selected names. `SearchFilters` joins with `,` and calls its existing `set("tags", ...)`.
- The current behavior of omitting `tags` from the query when empty is preserved (`params.tags = undefined` when no selection).

## Files

**New:**

- `front/src/components/TagCombobox.jsx` — the component described above.

**Modified:**

- `front/src/components/SearchFilters.jsx` — replace lines 147–172 (the `{/* Tags */}` block) with a `<TagCombobox ... />`. Remove the 30-tag `.slice(0, 30)` and the inline checkbox loop. Parse/join `params.tags` at this boundary.

**Unchanged:**

- `front/src/api/client.js`
- `back/core/views.py`, `back/core/models.py`, any backend tests — the API contract (`?tags=name1,name2`) is unchanged.

## Testing

- **Backend:** `back/core/tests/test_api.py::test_filter_by_tag` and `::test_filter_by_multiple_tags` already cover single- and multi-tag filtering through the same query string the UI will produce. No new backend tests.
- **Frontend:** no existing component-level tests in the project. None added here. Manual verification: load the search page, confirm dropdown opens on focus, typing filters, clicking toggles, chips remove, and the server list updates.
- Before and after the change, run `cd back && source venv/Scripts/activate && python manage.py test core.tests fetcher.tests` (per `CLAUDE.md`).

## Open questions

None.
