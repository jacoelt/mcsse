import { useState } from 'react'

const PLAYER_RANGES = [0, 10, 100, 1000, 10000, 100000]
const VOTE_RANGES = [0, 10, 100, 1000, 10000, 100000]

export default function SearchFilters({ filters, params, onChange, onReset }) {
  const [collapsed, setCollapsed] = useState(false)

  function set(key, value) {
    onChange({ ...params, [key]: value || undefined })
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

        {/* Online Players */}
        <div>
          <label className="block text-xs font-medium text-gray-400 mb-1">Online Players</label>
          <div className="flex gap-2">
            <select
              value={params.players_min ?? ''}
              onChange={e => set('players_min', e.target.value)}
              className="flex-1 bg-gray-700 border border-gray-600 rounded px-2 py-1.5 text-sm text-gray-200 focus:outline-none focus:border-emerald-500"
            >
              <option value="">Min</option>
              {PLAYER_RANGES.map(v => <option key={v} value={v}>{v.toLocaleString()}</option>)}
            </select>
            <select
              value={params.players_max ?? ''}
              onChange={e => set('players_max', e.target.value)}
              className="flex-1 bg-gray-700 border border-gray-600 rounded px-2 py-1.5 text-sm text-gray-200 focus:outline-none focus:border-emerald-500"
            >
              <option value="">Max</option>
              {PLAYER_RANGES.map(v => <option key={v} value={v}>{v.toLocaleString()}</option>)}
            </select>
          </div>
        </div>

        {/* Max Players (slots) */}
        <div>
          <label className="block text-xs font-medium text-gray-400 mb-1">Max Player Slots</label>
          <div className="flex gap-2">
            <select
              value={params.max_players_min ?? ''}
              onChange={e => set('max_players_min', e.target.value)}
              className="flex-1 bg-gray-700 border border-gray-600 rounded px-2 py-1.5 text-sm text-gray-200 focus:outline-none focus:border-emerald-500"
            >
              <option value="">Min</option>
              {PLAYER_RANGES.map(v => <option key={v} value={v}>{v.toLocaleString()}</option>)}
            </select>
            <select
              value={params.max_players_max ?? ''}
              onChange={e => set('max_players_max', e.target.value)}
              className="flex-1 bg-gray-700 border border-gray-600 rounded px-2 py-1.5 text-sm text-gray-200 focus:outline-none focus:border-emerald-500"
            >
              <option value="">Max</option>
              {PLAYER_RANGES.map(v => <option key={v} value={v}>{v.toLocaleString()}</option>)}
            </select>
          </div>
        </div>

        {/* Votes */}
        <div>
          <label className="block text-xs font-medium text-gray-400 mb-1">Votes</label>
          <div className="flex gap-2">
            <select
              value={params.votes_min ?? ''}
              onChange={e => set('votes_min', e.target.value)}
              className="flex-1 bg-gray-700 border border-gray-600 rounded px-2 py-1.5 text-sm text-gray-200 focus:outline-none focus:border-emerald-500"
            >
              <option value="">Min</option>
              {VOTE_RANGES.map(v => <option key={v} value={v}>{v.toLocaleString()}</option>)}
            </select>
            <select
              value={params.votes_max ?? ''}
              onChange={e => set('votes_max', e.target.value)}
              className="flex-1 bg-gray-700 border border-gray-600 rounded px-2 py-1.5 text-sm text-gray-200 focus:outline-none focus:border-emerald-500"
            >
              <option value="">Max</option>
              {VOTE_RANGES.map(v => <option key={v} value={v}>{v.toLocaleString()}</option>)}
            </select>
          </div>
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

        {/* Tags */}
        <div>
          <label className="block text-xs font-medium text-gray-400 mb-1">Tags</label>
          <div className="max-h-40 overflow-y-auto space-y-1">
            {filters.tags?.slice(0, 30).map(tag => {
              const activeTags = params.tags ? params.tags.split(',') : []
              const isActive = activeTags.includes(tag.name)
              return (
                <label key={tag.name} className="flex items-center gap-2 text-sm text-gray-300 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={isActive}
                    onChange={() => {
                      const next = isActive
                        ? activeTags.filter(t => t !== tag.name)
                        : [...activeTags, tag.name]
                      set('tags', next.filter(Boolean).join(','))
                    }}
                    className="accent-emerald-500"
                  />
                  {tag.display_name} ({tag.count})
                </label>
              )
            })}
          </div>
        </div>

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
