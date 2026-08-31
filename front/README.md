# Frontend — Minecraft Server Explorer

React 19 + Vite + Tailwind CSS 4. Talks to the Django-Ninja API at `$VITE_API_HOST`.

Setup, environment variables, and how to run the backend alongside this are in the [root README](../README.md).

## Scripts

```bash
npm run dev      # dev server on :5173
npm run build    # production build into dist/
npm run preview  # serve the production build locally
npm run lint     # eslint
```

## Layout

| Path | Purpose |
|------|---------|
| `src/main.jsx` | Entry point — mounts `<App />` inside the router |
| `src/App.jsx` | Routes: `/` (search) and `/server/:id` (detail) |
| `src/api/client.js` | Axios instance + `fetchServers` / `fetchServer` / `fetchFilters` |
| `src/pages/SearchPage.jsx` | Search results with infinite scroll; owns filter state and URL sync |
| `src/pages/ServerPage.jsx` | Single-server detail view |
| `src/components/SearchFilters.jsx` | The filter sidebar |
| `src/components/TagCombobox.jsx` | Searchable tag picker with removable chips |
| `src/components/LogRangeSlider.jsx` | Dual-handle slider on a log scale (players, votes) |
| `src/components/ServerCard.jsx` | One row in the results list |
| `src/components/Layout.jsx` | Page shell — header, footer |
| `src/components/AdSpace.jsx` | Ad slot placeholder (desktop only, `xl:` and up) |

## Notes

- All filter state is mirrored into URL query params, so any search is shareable and survives a reload.
- `updated_within_days` defaults to `7` even when absent from the URL, so a "clean" search is already filtered to servers seen in the last week. Stale data therefore shows up as an empty result set rather than as old rows — worth remembering when the fetchers haven't run in a while.
- `VITE_API_HOST` is read at **build** time, not runtime — a production build bakes in whatever host was set when `vite build` ran. Rebuild after changing it.
