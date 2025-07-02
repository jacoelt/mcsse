import { Button, Dialog, DialogActions, DialogContent, DialogTitle, Typography } from "@mui/material";


interface TosDialogProps {
  isVisible: boolean;
  setIsVisible: (isVisible: boolean) => void;
}

export default function TosDialog({ isVisible, setIsVisible }: TosDialogProps) {
  return (
    <Dialog
      open={isVisible}
      onClose={() => setIsVisible(false)}
      maxWidth="md"
      fullWidth
      scroll="paper"
    >
      <DialogTitle>
        Terms of Service
      </DialogTitle>

      <DialogContent>
        <Typography variant="body2" gutterBottom>
          Last updated: June 5, 2025
        </Typography>

        <Typography variant="h6" gutterBottom>
          1. Acceptance of Terms
        </Typography>
        <Typography variant="body1" gutterBottom>
          By accessing or using our service, you agree to be bound by these Terms
          of Service. If you do not agree to all the terms, then you may not
          access the service.
        </Typography>

        <Typography variant="h6" gutterBottom>
          2. Description of Service
        </Typography>
        <Typography variant="body1" gutterBottom>
          Our platform provides a searchable directory of Minecraft servers
          collected from various public sources. We are not affiliated with any
          listed server unless explicitly stated.
        </Typography>

        <Typography variant="h6" gutterBottom>
          3. User Conduct
        </Typography>
        <Typography variant="body1" gutterBottom>
          You agree not to use the service for any unlawful or abusive purposes.
          You must not interfere with or disrupt the service or servers connected
          to it.
        </Typography>

        <Typography variant="h6" gutterBottom>
          4. Content Disclaimer
        </Typography>
        <Typography variant="body1" gutterBottom>
          We do not control or moderate the content on the listed Minecraft
          servers. Server descriptions, tags, and any external content are the
          sole responsibility of their respective owners.
        </Typography>

        <Typography variant="h6" gutterBottom>
          5. Intellectual Property
        </Typography>
        <Typography variant="body1" gutterBottom>
          All trademarks, logos, and brand names are the property of their
          respective owners. We do not claim ownership over third-party content
          displayed on this platform.
        </Typography>

        <Typography variant="h6" gutterBottom>
          6. Termination
        </Typography>
        <Typography variant="body1" gutterBottom>
          We reserve the right to suspend or terminate access to the service at
          any time, without notice, for conduct that we believe violates these
          Terms or is harmful to other users of the service.
        </Typography>

        <Typography variant="h6" gutterBottom>
          7. Changes to Terms
        </Typography>
        <Typography variant="body1" gutterBottom>
          We may update these Terms from time to time. Continued use of the
          service after any changes constitutes your acceptance of the new Terms.
        </Typography>

        <Typography variant="h6" gutterBottom>
          8. Contact
        </Typography>
        <Typography variant="body1">
          If you have any questions about these Terms, please contact us using the link on the website.
        </Typography>
      </DialogContent>
      <DialogActions>
        <Button onClick={() => setIsVisible(false)} autoFocus>
          Close
        </Button>
      </DialogActions>
    </Dialog>
  )
}