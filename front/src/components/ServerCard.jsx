import { Link } from 'react-router-dom'

export default function ServerCard({ server }) {
  return (
    <Link
      to={`/server/${server.id}`}
      className="block bg-gray-800 border border-gray-700 rounded-lg p-4 hover:border-emerald-500/50 transition-colors"
    >
      <div className="flex items-start gap-4">
        {server.banner_url && (
          <img
            src={server.banner_url}
            alt=""
            className="w-24 h-12 object-cover rounded hidden sm:block"
          />
        )}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <h3 className="font-semibold text-gray-100 truncate">{server.name}</h3>
            <span className={`shrink-0 w-2 h-2 rounded-full ${server.is_online ? 'bg-emerald-400' : 'bg-red-400'}`} />
          </div>

          <div className="flex flex-wrap gap-2 text-xs text-gray-400 mb-2">
            {server.game_version && (
              <span className="bg-gray-700 px-2 py-0.5 rounded">{server.game_version}</span>
            )}
            <span className="bg-gray-700 px-2 py-0.5 rounded capitalize">{server.edition}</span>
            {server.country && (
              <span className="bg-gray-700 px-2 py-0.5 rounded">{server.country}</span>
            )}
          </div>

          <div className="flex flex-wrap gap-1">
            {server.tags.slice(0, 5).map(tag => (
              <span key={tag.name} className="text-xs bg-emerald-900/40 text-emerald-300 px-2 py-0.5 rounded">
                {tag.display_name}
              </span>
            ))}
            {server.tags.length > 5 && (
              <span className="text-xs text-gray-500">+{server.tags.length - 5}</span>
            )}
          </div>
        </div>

        <div className="text-right text-sm shrink-0 space-y-1">
          <div className="text-gray-300">
            <span className="font-semibold text-emerald-400">{server.online_players.toLocaleString()}</span>
            <span className="text-gray-500">/{server.max_players.toLocaleString()}</span>
          </div>
          <div className="text-xs text-gray-500">{server.votes.toLocaleString()} votes</div>
        </div>
      </div>
    </Link>
  )
}
