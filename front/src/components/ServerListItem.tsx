import { Copy, Check, HelpCircle, XCircle } from "lucide-react";
import { useState } from "react";
import type { Server } from "../types/Server";
import type { ServerTag } from "../types/ServerTag";


type ServerListItemProps = {
  server: Server;
  onViewDetails: (server: Server) => void;
};

export default function ServerListItem({ server, onViewDetails }: ServerListItemProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(server.ip_address).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  const statusColors = {
    online: "text-green-600",
    offline: "text-red-500",
    unknown: "text-gray-400",
  };

  const statusIcons = {
    online: <Check className="w-4 h-4 mr-1" />,
    offline: <XCircle className="w-4 h-4 mr-1" />,
    unknown: <HelpCircle className="w-4 h-4 mr-1" />,
  };

  return (
    <div className="flex items-start p-4 rounded-2xl shadow-md bg-white gap-4 hover:shadow-lg transition-shadow">
      <img
        src={server.banner}
        alt={`${server.name} logo`}
        className="w-16 h-16 rounded-xl object-cover mt-1"
      />

      <div className="flex-1 space-y-1">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-semibold text-gray-900">{server.name}</h2>
          <span className="text-sm bg-gray-200 text-gray-700 px-2 py-0.5 rounded-md">
            v{server.version}
          </span>
        </div>

        <p className="text-sm text-gray-600 line-clamp-2">{server.motd}</p>

        <div className="flex items-center gap-2 text-sm text-gray-700">
          <img
            src={`https://flagcdn.com/24x18/${server.country}.png`}
            alt={server.country}
            className="w-5 h-auto rounded-sm"
          />
          <div className="flex items-center gap-1">
            <span>{server.ip_address}</span>
            <button onClick={handleCopy} className="text-gray-500 hover:text-gray-700">
              <Copy className="w-4 h-4" />
            </button>
            {copied && <span className="text-xs text-green-600 ml-1">Copied!</span>}
          </div>
        </div>

        <div className="flex items-center text-sm mt-1">
          <div className={`flex items-center ${statusColors[server.status]}`}>
            {statusIcons[server.status]}
            <span className="capitalize">{server.status}</span>
          </div>
          <span className="ml-4 text-gray-500">
            {server.players_online} / {server.max_players} players
          </span>
        </div>

        <div className="flex flex-wrap gap-2 mt-2">
          {server.tags.sort((a:ServerTag, b:ServerTag) => a.relevance - b.relevance).map((tag) => (
            <span
              key={tag.name}
              className="text-xs bg-blue-100 text-blue-800 px-2 py-0.5 rounded-full"
              title={tag.description}
            >
              {tag.name}
            </span>
          ))}
        </div>
      </div>

      <button
        onClick={() => onViewDetails(server)}
        className="bg-green-600 hover:bg-green-700 text-white font-medium px-4 py-2 rounded-xl h-fit mt-1"
      >
        Join
      </button>
    </div>
  );
}
