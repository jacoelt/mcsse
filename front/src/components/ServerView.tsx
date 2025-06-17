import { Dialog, DialogTitle } from "@mui/material";
import type { Server } from "../types/Server";


export interface ServerViewProps {
  server?: Server;
  isOpened: boolean;
}


export function ServerView({ server, isOpened }: ServerViewProps) {

  return (
    // If no server is provided, return null or a placeholder
    !server ? null :
    <Dialog open={isOpened}>
      <DialogTitle>{server.name}</DialogTitle>


    </Dialog>
  )
}
