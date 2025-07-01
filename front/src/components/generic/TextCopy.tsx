import { CheckCircleOutlined, ContentCopy } from "@mui/icons-material";
import { Icon, Stack, Tooltip, Typography } from "@mui/material";
import { useState } from "react";


export default function TextCopy({ text, tooltip, textToCopy, sx }: { text: string, textToCopy?: string, tooltip?: string, sx?: React.CSSProperties }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = (event: React.MouseEvent) => {
    event.stopPropagation();
    event.preventDefault();
    navigator.clipboard.writeText(textToCopy || text).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  return (
    <Tooltip title={tooltip} placement="top">
      <Stack
        direction="row"
        sx={{ cursor: 'pointer', lineHeight: 1, ...sx }}

        // Stop Ripple Effect
        onTouchStart={(event) => event.stopPropagation()}
        onMouseDown={(event) => event.stopPropagation()}
        onClick={handleCopy}
      >
        <Typography variant="body1" sx={{ marginRight: 1 }}>
          {text}
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
          <Icon sx={{ color: copied ? 'green' : 'inherit', width: '24px', height: '24px' }}>
            {copied ? <CheckCircleOutlined /> : <ContentCopy />}
          </Icon>
        </Tooltip>
      </Stack>
    </Tooltip>
  );

}