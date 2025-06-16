import { Box } from "@mui/material";
import type { Server } from "../types/Server";
import ServerListEmptyState from "./ServerListEmptyState";
import ServerListItemSkeleton from "./ServerListItemSkeleton";
import ServerListItem from "./ServerListItem";

type ServerListProps = {
  servers: Server[];
  loading: boolean;
  onViewDetails: (server: Server) => void;
};

export default function ServerList ({servers, loading, onViewDetails}: ServerListProps) {
  return (
      <Box>
        {loading ? (
          <div className="space-y-4">
            {Array.from({ length: 4 }).map((_, index) => (
              <ServerListItemSkeleton key={index} />
            ))}
          </div>
        ) : servers.length === 0 ? (
          <ServerListEmptyState />
        ) : (
          servers.map((server) => (
            <ServerListItem key={server.ip_address} server={server} onViewDetails={onViewDetails} />
          ))
        )}
      </Box>
    );
}