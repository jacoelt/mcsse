import { useState, useRef, useEffect } from 'react'

export default function TagCombobox({ tags, selectedNames, onChange }) {
  const [query, setQuery] = useState('')
  const [open, setOpen] = useState(false)
  const rootRef = useRef(null)
  const selectedSet = new Set(selectedNames)
  const selectedTags = tags.filter(t => selectedSet.has(t.name))

  useEffect(() => {
    function handleMouseDown(e) {
      if (rootRef.current && !rootRef.current.contains(e.target)) {
        setOpen(false)
      }
    }
    document.addEventListener('mousedown', handleMouseDown)
    return () => document.removeEventListener('mousedown', handleMouseDown)
  }, [])

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

  const q = query.trim().toLowerCase()
  const filteredTags = q === ''
    ? tags
    : tags.filter(t =>
        t.display_name.toLowerCase().includes(q) ||
        t.name.toLowerCase().includes(q)
      )

  return (
    <div ref={rootRef} onClick={() => setOpen(true)}>
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
                  onClick={e => {
                    e.stopPropagation()
                    removeTag(tag.name)
                  }}
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
              onFocus={() => setOpen(true)}
              placeholder={selectedTags.length === 0 ? 'Search tags...' : ''}
              className="flex-1 min-w-[6rem] bg-transparent text-sm text-gray-200 placeholder-gray-500 focus:outline-none"
            />
          </div>
        </div>

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
      </div>
    </div>
  )
}
