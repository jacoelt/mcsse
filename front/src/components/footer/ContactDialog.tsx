import { Button, Dialog, DialogActions, DialogContent, DialogTitle, Stack, TextField } from "@mui/material";
import { useState } from "react";


interface ContactDialogProps {
  isVisible: boolean;
  setIsVisible: (isVisible: boolean) => void;
}


export default function ContactDialog({ isVisible, setIsVisible }: ContactDialogProps) {

  const [subject, setSubject] = useState("");
  const [email, setEmail] = useState("");
  const [content, setContent] = useState("");

  const handleClose = () => {
    setIsVisible(false);
    setSubject("");
    setEmail("");
    setContent("");
  };

  const handleSend = () => {
    // Here you would typically send the data to your backend or an email service
    console.log("Sending contact form:", { subject, email, content });

    handleClose();
  }
  return (
    <Dialog
      open={isVisible}
      onClose={() => setIsVisible(false)}
      maxWidth="md"
      fullWidth
    >
      <DialogTitle>
          Contact Form
      </DialogTitle>
      <DialogContent>
        <Stack direction="column">
          <TextField
            variant="outlined"
            label="Subject"
            value={subject}
            onChange={(e) => {
              setSubject(e.target.value.trim());
            }}
          />

          <TextField
            variant="outlined"
            label="Your Email (optional)"
            type="email"
            value={email}
            onChange={(e) => {
              setEmail(e.target.value.trim());
            }}
          />

          <TextField
            variant="outlined"
            label="Message"
            multiline
            minRows={4}
            maxRows={10}
            value={content}
            onChange={(e) => {
              setContent(e.target.value.trim());
            }}
          />
        </Stack>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose}>Cancel</Button>
        <Button onClick={handleSend} autoFocus variant="contained">Send</Button>
      </DialogActions>

    </Dialog>
  )
}