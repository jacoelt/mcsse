import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { fetchServer } from '../api/client'
import AdSpace from '../components/AdSpace'

export default function ServerPage() {
  const { id } = useParams()
  const [server, setServer] = useState(null)
  const [loading, setLoading] = useState(true)
  const [copied, setCopied] = useState(false)

  useEffect(() => {
    setLoading(true)
    fetchServer(id)
      .then(setServer)
      .catch(() => setServer(null))
      .finally(() => setLoading(false))
  }, [id])

  function copyIp() {
    if (!server) return
    const addr = server.port === 25565
      ? server.ip_address
      : `${server.ip_address}:${server.port}`
    navigator.clipboard.writeText(addr)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  if (loading) {
    return (
      <div className="flex justify-center py-12">
        <div className="w-8 h-8 border-2 border-emerald-400 border-t-transparent rounded-full animate-spin" />
      </div>
    )
  }

  if (!server) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-400 mb-4">Server not found.</p>
        <Link to="/" className="text-emerald-400 hover:underline">Back to search</Link>
      </div>
    )
  }

  return (
    <div className="flex gap-6">
      <div className="flex-1 min-w-0">
        <Link to="/" className="text-sm text-gray-400 hover:text-gray-200 mb-4 inline-block">
          &larr; Back to search
        </Link>

        {/* Banner */}
        {server.banner_url && (
          <img
            src={server.banner_url}
            alt=""
            className="w-full max-w-lg rounded-lg mb-4"
          />
        )}

        {/* Header */}
        <div className="flex items-start justify-between gap-4 mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-100 mb-1">{server.name}</h1>
            <div className="flex items-center gap-2">
              <span className={`w-2.5 h-2.5 rounded-full ${server.is_online ? 'bg-emerald-400' : 'bg-red-400'}`} />
              <span className="text-sm text-gray-400">
                {server.is_online ? 'Online' : 'Offline'}
              </span>
            </div>
          </div>
        </div>

        {/* IP & copy */}
        {server.ip_address && (
          <div className="bg-gray-800 border border-gray-700 rounded-lg p-4 mb-4 flex items-center gap-3">
            <span className="text-sm text-gray-400">Server IP:</span>
            <code className="text-emerald-400 font-mono">
              {server.port === 25565 ? server.ip_address : `${server.ip_address}:${server.port}`}
            </code>
            <button
              onClick={copyIp}
              className="ml-auto text-sm bg-gray-700 hover:bg-gray-600 px-3 py-1 rounded text-gray-300"
            >
              {copied ? 'Copied!' : 'Copy'}
            </button>
          </div>
        )}

        {/* Stats grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
          <StatBox label="Players" value={`${server.online_players.toLocaleString()} / ${server.max_players.toLocaleString()}`} />
          <StatBox label="Votes" value={server.votes.toLocaleString()} />
          <StatBox label="Version" value={server.game_version || 'N/A'} />
          <StatBox label="Edition" value={server.edition === 'both' ? 'Java & Bedrock' : server.edition} />
          {server.country && <StatBox label="Country" value={server.country} />}
        </div>

        {/* Tags */}
        {server.tags.length > 0 && (
          <div className="mb-6">
            <h2 className="text-sm font-medium text-gray-400 mb-2">Tags</h2>
            <div className="flex flex-wrap gap-2">
              {server.tags.map(tag => (
                <span key={tag.name} className="text-sm bg-emerald-900/40 text-emerald-300 px-3 py-1 rounded">
                  {tag.display_name}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Description */}
        {server.description && (
          <div className="mb-6">
            <h2 className="text-sm font-medium text-gray-400 mb-2">Description</h2>
            <div className="bg-gray-800 border border-gray-700 rounded-lg p-4 text-sm text-gray-300 whitespace-pre-wrap">
              {server.description}
            </div>
          </div>
        )}

        {/* Links */}
        {(server.website_url || server.discord_url) && (
          <div className="mb-6">
            <h2 className="text-sm font-medium text-gray-400 mb-2">Links</h2>
            <div className="flex gap-3">
              {server.website_url && (
                <a
                  href={server.website_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sm bg-gray-700 hover:bg-gray-600 px-4 py-2 rounded text-gray-300"
                >
                  Website
                </a>
              )}
              {server.discord_url && (
                <a
                  href={server.discord_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sm bg-indigo-900/50 hover:bg-indigo-900/70 px-4 py-2 rounded text-indigo-300"
                >
                  Discord
                </a>
              )}
            </div>
          </div>
        )}

        {/* Sources */}
        {server.sources?.length > 0 && (
          <div className="mb-6">
            <h2 className="text-sm font-medium text-gray-400 mb-2">Listed on</h2>
            <div className="flex flex-wrap gap-2">
              {server.sources.map((src, i) => (
                <a
                  key={i}
                  href={src.source_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-xs bg-gray-700 hover:bg-gray-600 px-3 py-1 rounded text-gray-400"
                >
                  {src.source_name}
                </a>
              ))}
            </div>
          </div>
        )}

        {/* Timestamps */}
        <div className="text-xs text-gray-500 space-y-1">
          <p>First indexed: {new Date(server.created_at).toLocaleDateString()}</p>
          <p>Last updated: {new Date(server.updated_at).toLocaleDateString()}</p>
          {server.last_checked && (
            <p>Last checked: {new Date(server.last_checked).toLocaleString()}</p>
          )}
        </div>
      </div>

      {/* Ad space */}
      <AdSpace />
    </div>
  )
}

function StatBox({ label, value }) {
  return (
    <div className="bg-gray-800 border border-gray-700 rounded-lg p-3 text-center">
      <div className="text-xs text-gray-500 mb-1">{label}</div>
      <div className="text-sm font-semibold text-gray-200 capitalize">{value}</div>
    </div>
  )
}
