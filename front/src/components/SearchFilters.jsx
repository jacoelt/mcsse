import { useState } from 'react'
import LogRangeSlider from './LogRangeSlider'
import TagCombobox from './TagCombobox'

const LOG_STEPS = [0, 10, 100, 1000, 10000, 100000]
const UPDATED_WITHIN_OPTIONS = [
  { value: '1', label: 'Last 24 hours' },
  { value: '7', label: 'Last 7 days' },
  { value: '30', label: 'Last 30 days' },
  { value: '90', label: 'Last 90 days' },
  { value: '180', label: 'Last 180 days' },
  { value: '365', label: 'Last year' },
  { value: '0', label: 'Any time' },
]

export default function SearchFilters({ filters, params, onChange, onReset }) {
  const [collapsed, setCollapsed] = useState(false)

  function set(key, value) {
    onChange({ ...params, [key]: value || undefined })
  }

  function setRange(minKey, maxKey, { min, max }) {
    onChange({ ...params, [minKey]: min, [maxKey]: max })
  }

  return (
    <div className="bg-gray-800 border border-gray-700 rounded-lg">
      <button
        onClick={() => setCollapsed(!collapsed)}
        className="w-full px-4 py-3 flex items-center justify-between text-sm font-semibold text-gray-300 lg:hidden"
      >
        Filters
        <svg className={`w-4 h-4 transition-transform ${collapsed ? '' : 'rotate-180'}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      <div className={`${collapsed ? 'hidden' : ''} lg:block p-4 space-y-4`}>
        {/* Search */}
        <div>
          <label className="block text-xs font-medium text-gray-400 mb-1">Search</label>
          <input
            type="text"
            value={params.q || ''}
            onChange={e => set('q', e.target.value)}
            placeholder="Server name..."
            className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-1.5 text-sm text-gray-200 placeholder-gray-500 focus:outline-none focus:border-emerald-500"
          />
        </div>

        {/* Version */}
        <div>
          <label className="block text-xs font-medium text-gray-400 mb-1">Version</label>
          <select
            value={params.version || ''}
            onChange={e => set('version', e.target.value)}
            className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-1.5 text-sm text-gray-200 focus:outline-none focus:border-emerald-500"
          >
            <option value="">All versions</option>
            {filters.versions?.map(v => (
              <option key={v.version} value={v.version}>
                {v.version} ({v.count})
              </option>
            ))}
          </select>
        </div>

        {/* Edition */}
        <div>
          <label className="block text-xs font-medium text-gray-400 mb-1">Edition</label>
          <div className="space-y-1">
            {['java', 'bedrock', 'both'].map(ed => (
              <label key={ed} className="flex items-center gap-2 text-sm text-gray-300 cursor-pointer">
                <input
                  type="radio"
                  name="edition"
                  checked={params.edition === ed}
                  onChange={() => set('edition', params.edition === ed ? undefined : ed)}
                  className="accent-emerald-500"
                />
                <span className="capitalize">{ed === 'both' ? 'Java & Bedrock' : ed}</span>
              </label>
            ))}
            {params.edition && (
              <button onClick={() => set('edition', undefined)} className="text-xs text-gray-500 hover:text-gray-300">
                Clear
              </button>
            )}
          </div>
        </div>

        <LogRangeSlider
          label="Online Players"
          steps={LOG_STEPS}
          minValue={params.players_min}
          maxValue={params.players_max}
          onCommit={range => setRange('players_min', 'players_max', range)}
        />

        <LogRangeSlider
          label="Max Player Slots"
          steps={LOG_STEPS}
          minValue={params.max_players_min}
          maxValue={params.max_players_max}
          onCommit={range => setRange('max_players_min', 'max_players_max', range)}
        />

        <LogRangeSlider
          label="Votes"
          steps={LOG_STEPS}
          minValue={params.votes_min}
          maxValue={params.votes_max}
          onCommit={range => setRange('votes_min', 'votes_max', range)}
        />

        {/* Last Updated */}
        <div>
          <label className="block text-xs font-medium text-gray-400 mb-1">Last updated</label>
          <select
            value={params.updated_within_days ?? '7'}
            onChange={e => set('updated_within_days', e.target.value)}
            className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-1.5 text-sm text-gray-200 focus:outline-none focus:border-emerald-500"
          >
            {UPDATED_WITHIN_OPTIONS.map(opt => (
              <option key={opt.value} value={opt.value}>{opt.label}</option>
            ))}
          </select>
        </div>

        {/* Country */}
        <div>
          <label className="block text-xs font-medium text-gray-400 mb-1">Country</label>
          <select
            value={params.country || ''}
            onChange={e => set('country', e.target.value)}
            className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-1.5 text-sm text-gray-200 focus:outline-none focus:border-emerald-500"
          >
            <option value="">All countries</option>
            {filters.countries?.map(c => (
              <option key={c.country} value={c.country}>
                {c.country} ({c.count})
              </option>
            ))}
          </select>
        </div>

        <TagCombobox
          tags={filters.tags || []}
          selectedNames={params.tags ? params.tags.split(',').filter(Boolean) : []}
          onChange={names => set('tags', names.length > 0 ? names.join(',') : undefined)}
        />

        {/* Sort */}
        <div>
          <label className="block text-xs font-medium text-gray-400 mb-1">Sort by</label>
          <select
            value={params.sort || '-online_players'}
            onChange={e => set('sort', e.target.value)}
            className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-1.5 text-sm text-gray-200 focus:outline-none focus:border-emerald-500"
          >
            <option value="-online_players">Players (high to low)</option>
            <option value="online_players">Players (low to high)</option>
            <option value="-votes">Votes (high to low)</option>
            <option value="votes">Votes (low to high)</option>
            <option value="-max_players">Max slots (high to low)</option>
            <option value="name">Name (A-Z)</option>
            <option value="-name">Name (Z-A)</option>
            <option value="-created_at">Newest first</option>
            <option value="created_at">Oldest first</option>
          </select>
        </div>

        {/* Reset */}
        <button
          onClick={onReset}
          className="w-full text-sm text-gray-400 hover:text-gray-200 py-1"
        >
          Reset filters
        </button>
      </div>
    </div>
  )
}
