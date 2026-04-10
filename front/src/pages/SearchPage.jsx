import { useState, useEffect, useCallback, useRef } from 'react'
import { useSearchParams } from 'react-router-dom'
import { fetchServers, fetchFilters } from '../api/client'
import SearchFilters from '../components/SearchFilters'
import ServerCard from '../components/ServerCard'
import AdSpace from '../components/AdSpace'

const PAGE_SIZE = 20
const FILTER_KEYS = [
  'q', 'version', 'edition', 'players_min', 'players_max',
  'max_players_min', 'max_players_max', 'votes_min', 'votes_max',
  'country', 'tags', 'sort',
]

function paramsFromSearch(searchParams) {
  const p = {}
  for (const key of FILTER_KEYS) {
    const val = searchParams.get(key)
    if (val) p[key] = val
  }
  return p
}

export default function SearchPage() {
  const [searchParams, setSearchParams] = useSearchParams()
  const [params, setParams] = useState(() => paramsFromSearch(searchParams))
  const [servers, setServers] = useState([])
  const [totalCount, setTotalCount] = useState(0)
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(false)
  const [hasMore, setHasMore] = useState(true)
  const [filters, setFilters] = useState({ versions: [], countries: [], tags: [] })
  const observerRef = useRef(null)
  const sentinelRef = useRef(null)

  // Load filter options once
  useEffect(() => {
    fetchFilters().then(setFilters).catch(() => {})
  }, [])

  // Sync params to URL
  useEffect(() => {
    const cleaned = {}
    for (const [k, v] of Object.entries(params)) {
      if (v !== undefined && v !== '') cleaned[k] = v
    }
    setSearchParams(cleaned, { replace: true })
  }, [params, setSearchParams])

  // Reset results when params change
  useEffect(() => {
    setServers([])
    setPage(1)
    setHasMore(true)
  }, [params])

  // Fetch servers
  useEffect(() => {
    let cancelled = false
    setLoading(true)

    const queryParams = { ...params, page, page_size: PAGE_SIZE }
    // Remove undefined/empty
    for (const k of Object.keys(queryParams)) {
      if (queryParams[k] === undefined || queryParams[k] === '') delete queryParams[k]
    }

    fetchServers(queryParams)
      .then(data => {
        if (cancelled) return
        setServers(prev => page === 1 ? data.results : [...prev, ...data.results])
        setTotalCount(data.count)
        setHasMore(page * PAGE_SIZE < data.count)
      })
      .catch(() => {
        if (!cancelled) setHasMore(false)
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })

    return () => { cancelled = true }
  }, [params, page])

  // Infinite scroll observer
  useEffect(() => {
    if (observerRef.current) observerRef.current.disconnect()

    observerRef.current = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting && hasMore && !loading) {
        setPage(p => p + 1)
      }
    }, { threshold: 0.1 })

    if (sentinelRef.current) {
      observerRef.current.observe(sentinelRef.current)
    }

    return () => observerRef.current?.disconnect()
  }, [hasMore, loading])

  const handleReset = useCallback(() => {
    setParams({})
  }, [])

  return (
    <div className="flex gap-6">
      {/* Filters sidebar */}
      <div className="w-full lg:w-64 shrink-0">
        <SearchFilters
          filters={filters}
          params={params}
          onChange={setParams}
          onReset={handleReset}
        />
      </div>

      {/* Results */}
      <div className="flex-1 min-w-0">
        <div className="flex items-center justify-between mb-4">
          <p className="text-sm text-gray-400">
            {totalCount.toLocaleString()} server{totalCount !== 1 ? 's' : ''} found
          </p>
        </div>

        <div className="space-y-3">
          {servers.map(server => (
            <ServerCard key={server.id} server={server} />
          ))}
        </div>

        {loading && (
          <div className="flex justify-center py-8">
            <div className="w-6 h-6 border-2 border-emerald-400 border-t-transparent rounded-full animate-spin" />
          </div>
        )}

        {!loading && servers.length === 0 && (
          <div className="text-center py-12 text-gray-500">
            No servers found matching your filters.
          </div>
        )}

        {/* Infinite scroll sentinel */}
        <div ref={sentinelRef} className="h-4" />
      </div>

      {/* Ad space */}
      <AdSpace />
    </div>
  )
}
