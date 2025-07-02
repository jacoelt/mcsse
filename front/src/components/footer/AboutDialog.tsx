import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Box,
} from "@mui/material";

interface AboutDialogProps {
  isVisible: boolean;
  setIsVisible: (isVisible: boolean) => void;
}

export default function AboutDialog({ isVisible, setIsVisible }: AboutDialogProps) {
  return (
    <Dialog
      open={isVisible}
      onClose={() => setIsVisible(false)}
      maxWidth="sm"
      fullWidth
      scroll="paper"
    >
      <DialogTitle>About This Project</DialogTitle>
      <DialogContent>
        <Box mb={2}>
          <Typography variant="body1" gutterBottom>
            This site is a community-driven search engine for Minecraft servers.
            My goal is to make it easier to discover, compare, and explore the
            best servers — without the clutter or limitations of traditional
            listings.
          </Typography>
          <Typography variant="body1" gutterBottom>
            Server data is collected from public sources and refreshed regularly.
            I aim to provide accurate and up-to-date information, but please
            report any issues or outdated listings using the contact form.
          </Typography>
          <Typography variant="body1" gutterBottom>
            This project is independent and not affiliated with Mojang or
            Microsoft.
          </Typography>
        </Box>
        <Typography variant="body2" color="textSecondary">
          Made with ❤️ by Minecraft players, for Minecraft players.
        </Typography>
      </DialogContent>
      <DialogActions>
        <Button onClick={() => setIsVisible(false)} autoFocus>
          Close
        </Button>
      </DialogActions>
    </Dialog>
  );
}
