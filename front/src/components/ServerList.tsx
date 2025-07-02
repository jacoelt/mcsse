import type { Server } from "../types/Server";
import ServerListEmptyState from "./ServerListEmptyState";
import ServerListItem from "./ServerListItem";
import InfiniteScroll from "react-infinite-scroll-component";
import { CircularProgress, Stack, Typography } from "@mui/material";

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
      loader={
        <Stack direction="row" sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', marginTop: 4 }}>
          <CircularProgress /> Loading more servers...
        </Stack>
      }
      endMessage={
        <Typography variant="body1" sx={{ textAlign: 'center', marginTop: 4, color: 'text.secondary' }}>
          {
            loading
              ? (<><CircularProgress /> Loading more servers...</>)
              : "No more servers to display."
          }
        </Typography>
      }
      height="calc(100vh - 200px)"
      style={{ overflowY: 'auto', ...sx }}
    >
      {!loading && servers.length === 0 ? (
        <ServerListEmptyState />
      ) : (
        servers.map((server) => (
          <ServerListItem key={server.id} server={server} onViewDetails={onViewDetails} />
        ))
      )}
    </InfiniteScroll>
  );
}