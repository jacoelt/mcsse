import { Typography } from "@mui/material";

export default function ServerListEmptyState() {
  return (
    <Typography variant="body1" sx={{ textAlign: 'center', marginTop: 4, color: 'text.secondary' }}>
      No servers found. Try adjusting your search criteria or check back later.
    </Typography>
  );
}
