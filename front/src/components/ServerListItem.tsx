import type { Server } from "../types/Server";
import type { ServerTag } from "../types/ServerTag";
import { CancelOutlined, CheckCircleOutlined, HelpOutline } from "@mui/icons-material";
import { Card, CardActionArea, CardMedia, Chip, Grid, Icon, Stack, Typography } from "@mui/material";
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
    <Card sx={{ display: 'flex', direction: 'column', margin: 2, cursor: 'pointer' }} onClick={() => onViewDetails(server)}>
      <CardActionArea sx={{ padding: 2, height: '170px' }}>
        <Grid container sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <Grid size={5} container direction="row">
            <Grid size={11}>
              <Typography variant="h5" sx={{ fontWeight: 'bold', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }} title={server.name}>
                {server.name || "Unknown Server"}
              </Typography>
            </Grid>
            <Grid size={1}>
              <Typography variant="h6" title={country.name}>{country.flag}</Typography>
            </Grid>
          </Grid>

          <Grid size={4}>
            <Stack>
              {server.ip_address_java && (
                <TextCopy text={server.ip_address_java} tooltip="Java IP Address" />
              )}
              {server.ip_address_bedrock && (
                <TextCopy text={server.ip_address_bedrock} tooltip="Bedrock IP Address" />
              )}
            </Stack>
          </Grid>
          <Grid size={1} sx={{ display: 'flex', alignItems: 'center' }}>
            <Icon sx={{ color: server.status === 'online' ? 'green' : server.status === 'offline' ? 'red' : 'gray' }}>
              {statusIcons[server.status] || <HelpOutline />}
            </Icon>
            <Typography variant="body2" sx={{ marginLeft: 1 }}>
              {server.status.charAt(0).toUpperCase() + server.status.slice(1)}
            </Typography>
          </Grid>
          <Grid size={2}>
            <Typography variant="body2" sx={{ color: 'text.secondary' }}>
              {server.versions || "Unknown Version"}
              {server.edition === "java" ? " (Java)" : server.edition === "bedrock" ? " (Bedrock)" : " (Java + Bedrock)"}
            </Typography>
          </Grid>
        </Grid>
        <Grid container sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Grid size={5} direction="column">
            <CardMedia
              component="img"
              image={server.banner}
              alt={server.name}
              sx={{ maxWidth: "450px", maxHeight: "60px", borderRadius: 1, marginTop: 1 }}
            />
            <Stack direction="row" sx={{ flexWrap: 'wrap', marginTop: 1 }}>
              {server.tags.sort((a: ServerTag, b: ServerTag) => a.relevance - b.relevance).map((tag: ServerTag) =>
                <Chip color="primary" size="small" label={tag.name} key={tag.name} sx={{ margin: '2px' }} />
              )}
            </Stack>
          </Grid>
          <Grid size={4} sx={{ overflow: 'hidden', textOverflow: 'ellipsis', maxHeight: '75px', flexGrow: 1, marginLeft: 2 }}>
            <Typography variant="body2" sx={{ color: 'text.secondary', marginTop: 1, whiteSpace: 'pre-line' }}>
              {server.description || "No description available"}
            </Typography>
          </Grid>
          <Grid size={2} direction="column" sx={{ textAlign: 'left', marginLeft: 2 }}>
            <Typography variant="body2" sx={{ color: 'text.secondary' }}>
              Players: {server.players_online.toLocaleString()} / {server.max_players.toLocaleString()}
            </Typography>
            <Typography variant="body2" sx={{ color: 'text.secondary' }}>
              Votes: {server.total_votes.toLocaleString()}
            </Typography>
          </Grid>
        </Grid>
      </CardActionArea>
    </Card>
  );
}
