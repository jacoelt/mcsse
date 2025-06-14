import { useState } from "react";
import type { Server } from "../types/Server";
import type { ServerTag } from "../types/ServerTag";
import { CancelOutlined, CheckCircleOutlined, ContentCopy, HelpOutline } from "@mui/icons-material";
import { Box, Card, CardActionArea, CardMedia, Chip, Icon, IconButton, Stack, Tooltip, Typography } from "@mui/material";
import { getCountry } from "../helpers/countries";


type ServerListItemProps = {
  server: Server;
  onViewDetails: (server: Server) => void;
};

export default function ServerListItem({ server, onViewDetails }: ServerListItemProps) {
  const [copied, setCopied] = useState(false);

  const country = getCountry(server.country);

  const handleCopy = (event: Event) => {
    event.stopPropagation();
    event.preventDefault();
    navigator.clipboard.writeText(server.ip_address).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };


  const statusIcons = {
    online: <CheckCircleOutlined />,
    offline: <CancelOutlined />,
    unknown: <HelpOutline />,
  };

  return (
    <Card sx={{ display: 'flex', direction: 'column', padding: 2, marginBottom: 2, cursor: 'pointer' }} onClick={() => onViewDetails(server)}>
      <CardActionArea>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <Box>
            <Typography variant="h5" sx={{ fontWeight: 'bold' }}>
              {server.name || "Unknown Server"}
            </Typography>
            <Typography variant="h6" title={country.name}>{country.flag}</Typography>
          </Box>
          <Box>
            <Typography variant="body1" sx={{ marginRight: 1 }}>
              {server.ip_address}
            </Typography>
            <Tooltip
                open={copied}
                disableFocusListener
                disableHoverListener
                disableTouchListener
                title="Copied!"
                slotProps={{
                  popper: {
                    disablePortal: true,
                  },
                }}
              >
              <IconButton
                // Stop Ripple Effect
                onTouchStart={(event) => event.stopPropagation()}
                onMouseDown={(event) => event.stopPropagation()}
                onClick={handleCopy}
                sx={{ cursor: 'pointer', color: copied ? 'green' : 'inherit' }}
              >
                {copied ? <CheckCircleOutlined /> : <ContentCopy />}
              </IconButton>
            </Tooltip>

          </Box>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Icon sx={{ color: server.status === 'online' ? 'green' : server.status === 'offline' ? 'red' : 'gray' }}>
              {statusIcons[server.status] || <HelpOutline />}
            </Icon>
            <Typography variant="body2" sx={{ marginLeft: 1 }}>
              {server.status.charAt(0).toUpperCase() + server.status.slice(1)}
            </Typography>
          </Box>
          <Box>
            <Typography variant="body2" sx={{ color: 'text.secondary' }}>
              {server.version || "Unknown Version"}
              {server.edition === "java" ? " (Java)" : server.edition === "bedrock" ? " (Bedrock)" : " (Java + Bedrock)"}
            </Typography>
          </Box>
        </Box>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Stack sx={{ display: 'flex', direction: 'column' }}>
            <CardMedia component="img" image={server.banner || "/default-banner.png"} alt={server.name} sx={{ width: 460, height: 50, objectFit: 'cover', borderRadius: 1, marginTop: 1 }} />
            <Stack direction="row">
              {server.tags.sort((a: ServerTag, b:ServerTag) => a.relevance - b.relevance).map((tag: ServerTag) =>
                <Chip color="primary" size="small" label={tag.name} key={tag.name} sx={{ margin: '2px' }} />
              )}
            </Stack>
          </Stack>
          <Box>
            <Typography variant="body2" sx={{ color: 'text.secondary', marginTop: 1 }}>
              {server.motd || "No MOTD available"}
            </Typography>
          </Box>
          <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end' }}>
            <Typography variant="body2" sx={{ color: 'text.secondary' }}>
              Players: {server.players_online}/{server.max_players}
            </Typography>
            <Typography variant="body2" sx={{ color: 'text.secondary' }}>
              Votes: {server.total_votes}
            </Typography>
          </Box>
        </Box>
      </CardActionArea>
    </Card>
  );
}
