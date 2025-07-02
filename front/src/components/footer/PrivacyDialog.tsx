import { Button, Dialog, DialogActions, DialogContent, DialogTitle, Typography } from "@mui/material";

interface PrivacyDialogProps {
    isVisible: boolean;
    setIsVisible: (isVisible: boolean) => void;
}

export default function PrivacyDialog({ isVisible, setIsVisible }: PrivacyDialogProps) {
    return (
        <Dialog
            open={isVisible}
            onClose={() => setIsVisible(false)}
            maxWidth="md"
            fullWidth
            scroll="paper"
        >
            <DialogTitle>
                Privacy Policy
            </DialogTitle>

            <DialogContent>
                <Typography variant="h6" gutterBottom>
                    1. Introduction
                </Typography>
                <Typography variant="body1" gutterBottom>
                    This Privacy Policy explains how we collect, use, and protect your
                    personal information when you use our website.
                </Typography>

                <Typography variant="h6" gutterBottom>
                    2. Acceptance of Privacy Policy
                </Typography>
                <Typography variant="body1" gutterBottom>
                    By accessing or using this service, you acknowledge that you have read,
                    understood, and agree to be bound by this Privacy Policy. If you do not agree
                    with any part of it, please discontinue use of the service.
                </Typography>

                <Typography variant="h6" gutterBottom>
                    3. Data Collection
                </Typography>
                <Typography variant="body1" gutterBottom>
                    We do not collect any personal data unless you voluntarily provide it
                    (e.g. via a contact form). The data we process is limited to anonymous
                    analytics and publicly available information about Minecraft servers.
                </Typography>

                <Typography variant="h6" gutterBottom>
                    4. Cookies & Analytics
                </Typography>
                <Typography variant="body1" gutterBottom>
                    We may use cookies or similar technologies to understand how users
                    interact with our site. This data is anonymized and used for performance
                    monitoring and user experience improvements.
                    We currently do not use any non-essential cookies or third-party tracking
                    services. Only essential cookies required for the functioning of the website
                    (such as session management) may be used. These cookies do not collect
                    personally identifiable information and are not used for analytics or
                    advertising purposes.
                </Typography>

                <Typography variant="h6" gutterBottom>
                    5. Third-Party Services
                </Typography>
                <Typography variant="body1" gutterBottom>
                    We may use third-party services such as analytics providers. These
                    services may collect anonymized usage data in accordance with their own
                    privacy policies.
                </Typography>

                <Typography variant="h6" gutterBottom>
                    6. Data Retention
                </Typography>
                <Typography variant="body1" gutterBottom>
                    We retain collected data only as long as necessary to provide and
                    improve our services. You can request deletion of your data at any time.
                </Typography>

                <Typography variant="h6" gutterBottom>
                    7. Your Rights
                </Typography>
                <Typography variant="body1" gutterBottom>
                    You have the right to access, correct, or request deletion of any
                    personal data we may hold about you. We are committed to complying with
                    applicable data protection laws.
                </Typography>

                <Typography variant="h6" gutterBottom>
                    8. Changes to This Policy
                </Typography>
                <Typography variant="body1" gutterBottom>
                    We may update this Privacy Policy from time to time. Any significant
                    changes will be announced on this page.
                </Typography>

                <Typography variant="h6" gutterBottom>
                    9. Contact
                </Typography>
                <Typography variant="body1">
                    If you have any questions about this Privacy Policy, please contact us
                    using the link on the website.
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