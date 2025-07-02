import { Chip, Dialog, DialogTitle, Grid, IconButton, Stack, Tooltip, Typography } from "@mui/material";
import type { Server } from "../types/Server";
import TextCopy from "./generic/TextCopy";
import { Close, InfoOutline, OpenInNew } from "@mui/icons-material";
import { getLanguagesFromCode } from "../helpers/languages";
import { getCountry } from "../helpers/countries";


export interface ServerViewProps {
  server: Server | null;
  onClose: () => void; // Optional: if you want to handle closing the dialog
}


export function ServerView({ server, onClose }: ServerViewProps) {

  const countryObj = server?.country ? getCountry(server.country) : null;

  const dataTableLabelWidth = 6;

  return (
    // If no server is provided, return null
    !server ? <></> :
      <Dialog
        open={!!server}
        fullWidth maxWidth="md"
        onClose={onClose}
        scroll="paper"
      >
        <DialogTitle>
          <Typography variant="h4" component="p" sx={{ fontWeight: 'bold' }}>
            {server.name}
          </Typography>
        </DialogTitle>
        <IconButton
          aria-label="close"
          onClick={onClose}
          sx={(theme) => ({
            position: 'absolute',
            right: 8,
            top: 8,
            color: theme.palette.grey[500],
          })}
        >
          <Close />
        </IconButton>
        <Grid container spacing={2} sx={{ padding: 2 }}>
          <Grid size={4} container spacing={2}>

            {server.ip_address_java && (
              <Grid size={12}>
                <TextCopy text="Java IP" tooltip={server.ip_address_java} textToCopy={server.ip_address_java} />
              </Grid>
            )}

            {server.ip_address_bedrock && (
              <Grid size={12}>
                <TextCopy text="Bedrock IP" tooltip={server.ip_address_bedrock} textToCopy={server.ip_address_bedrock} />
              </Grid>
            )}

            {server.website && (
              <Grid size={12}>
                <Tooltip title={server.website} placement="top">
                  <Typography
                    variant="body1"
                    sx={{ cursor: 'pointer' }}
                    onClick={() => window.open(server.website, "_blank")}
                  >
                    Website
                    <OpenInNew sx={{ marginLeft: 1 }} />
                  </Typography>
                </Tooltip>
              </Grid>
            )}

            {server.discord && (
              <Grid size={12}>
                <Tooltip title={server.discord} placement="top">
                  <Typography
                    variant="body1"
                    sx={{ cursor: 'pointer' }}
                    onClick={() => window.open(server.discord, "_blank")}
                  >
                    Discord
                    <OpenInNew sx={{ marginLeft: 1 }} />
                  </Typography>
                </Tooltip>
              </Grid>
            )}

            <Grid size={dataTableLabelWidth}>
              <Typography variant="body1">Version</Typography>
            </Grid>
            <Grid size={12 - dataTableLabelWidth}>
              <Typography variant="body1">{server.versions || "Unknown Version"}</Typography>
            </Grid>

            <Grid size={dataTableLabelWidth}>
              <Typography variant="body1">Status</Typography>
            </Grid>
            <Grid size={12 - dataTableLabelWidth}>
              <Typography variant="body1" sx={{ color: server.status === 'online' ? 'green' : server.status === 'offline' ? 'red' : 'gray' }}>
                {server.status.charAt(0).toUpperCase() + server.status.slice(1)}
              </Typography>
            </Grid>

            <Grid size={dataTableLabelWidth}>
              <Typography variant="body1">Country</Typography>
            </Grid>
            <Grid size={12 - dataTableLabelWidth}>
              {countryObj ? (
                <Tooltip title={countryObj.name} placement="top">
                  <Typography variant="body1">
                    {countryObj.flag}
                  </Typography>
                </Tooltip>
              ) : (
                <Typography variant="body1">N/A</Typography>
              )}
            </Grid>

            <Grid size={dataTableLabelWidth}>
              <Typography variant="body1">Languages</Typography>
            </Grid>
            <Grid size={12 - dataTableLabelWidth}>
              <Typography variant="body1">
                {server.languages ? getLanguagesFromCode(server.languages) : "N/A"}
              </Typography>
            </Grid>

            <Grid size={dataTableLabelWidth}>
              <Typography variant="body1">Players</Typography>
            </Grid>
            <Grid size={12 - dataTableLabelWidth}>
              <Typography variant="body1">
                {server.players_online || "??"} / {server.max_players || "??"}
              </Typography>
            </Grid>

            <Grid size={dataTableLabelWidth}>
              <Typography variant="body1">
                Total Votes
                <Tooltip title="Total number of votes this server has received accross different voting websites" placement="top">
                  <InfoOutline fontSize="small" />
                </Tooltip>
              </Typography>
            </Grid>
            <Grid size={12 - dataTableLabelWidth}>
              <Typography variant="body1">
                {server.total_votes || "??"}
              </Typography>
            </Grid>

            <Grid size={dataTableLabelWidth}>
              <Typography variant="body1">Added on</Typography>
            </Grid>
            <Grid size={12 - dataTableLabelWidth}>
              <Typography variant="body1">
                {new Date(server.added_at).toISOString().split('T')[0]}
              </Typography>
            </Grid>
          </Grid>

          <Grid size={8} direction="column">
            {server.banner && (
              <img
                src={server.banner}
                alt={server.name}
              />
            )}

            <Typography variant="body1" sx={{ marginTop: 2, whiteSpace: 'pre-line' }}>
              {server.description || "No description available"}
            </Typography>

            <Stack direction="row" sx={{ marginTop: 2 }}>
              {server.tags.sort((a, b) => a.relevance - b.relevance).map((tag) => (
                <Tooltip key={tag.name} title={tag.description || ""}>
                  <Chip
                    color="primary"
                    size="small"
                    label={tag.name}
                    sx={{ margin: '2px' }}
                  />
                </Tooltip>
              ))}
            </Stack>
          </Grid>
        </Grid>

      </Dialog>
  )
}
