

import type { Server } from "../types/Server";
import ServerListEmptyState from "./ServerListEmptyState";
import ServerListItemSkeleton from "./ServerListItemSkeleton";
import ServerListItem from "./ServerListItem";
import InfiniteScroll from "react-infinite-scroll-component";

interface ServerListProps {
  servers: Server[];
  loading: boolean;
  onViewDetails: (server: Server) => void;
  onLoadMore: () => void;
  hasMore: boolean;
  sx?: React.CSSProperties;
};

export default function ServerList({ servers, loading, onViewDetails, onLoadMore, hasMore, sx }: ServerListProps) {
  return (
    <InfiniteScroll
      dataLength={servers.length}
      next={onLoadMore}
      hasMore={hasMore}
      loader={<ServerListItemSkeleton />}
      endMessage={
        <p className="text-center text-gray-500">
          {loading ? "Loading more servers..." : "No more servers to display."}
        </p>
      }
      style={{ ...sx }}
    >
      {servers.length === 0 ? (
        <ServerListEmptyState />
      ) : (
        servers.map((server) => (
          <ServerListItem key={server.id} server={server} onViewDetails={onViewDetails} />
        ))
      )}
    </InfiniteScroll>
  );
}