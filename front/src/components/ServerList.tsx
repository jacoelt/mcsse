import type { Server } from "../types/Server";
import ServerListEmptyState from "./ServerListEmptyState";
import ServerListItem from "./ServerListItem";
import ServerListItemSkeleton from "./ServerListItemSkeleton";

type ServerListItem = {
  servers: Server[];
  loading: boolean;
  onViewDetails: (server: Server) => void;
};

export default function ServerList ({servers, loading, onViewDetails}: ServerListItem) {
  return (
      <div className="max-w-4xl mx-auto p-4">
        <h1 className="text-2xl font-bold mb-4">Minecraft Server Explorer</h1>

        {loading ? (
          <div className="space-y-4">
            {Array.from({ length: 4 }).map((_, index) => (
              <ServerListItemSkeleton key={index} />
            ))}
          </div>
        ) : servers.length === 0 ? (
          <ServerListEmptyState />
        ) : (
          <div className="space-y-4">
            {servers.map((server) => (
              <ServerListItem key={server.ip_address} server={server} onViewDetails={onViewDetails} />
            ))}
          </div>
        )}
      </div>
    );
}