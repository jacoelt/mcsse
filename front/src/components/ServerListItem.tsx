import type { Server } from "../types/Server";
import type { ServerTag } from "../types/ServerTag";
import { CancelOutlined, CheckCircleOutlined, HelpOutline } from "@mui/icons-material";
import { Box, Card, CardActionArea, CardMedia, Chip, Icon, Stack, Typography } from "@mui/material";
import { getCountry } from "../helpers/countries";
import TextCopy from "./generic/TextCopy";


interface ServerListItemProps {
  server: Server;
  onViewDetails: (server: Server) => void;
};

export default function ServerListItem({ server, onViewDetails }: ServerListItemProps) {
  const country = getCountry(server.country);

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

          <Stack>
            {server.ip_address_java && (
              <TextCopy text={server.ip_address_java} tooltip="Java IP Address" />
            )}
            {server.ip_address_bedrock && (
              <TextCopy text={server.ip_address_bedrock} tooltip="Bedrock IP Address" />
            )}
          </Stack>

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
              {server.description || "No description available"}
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
