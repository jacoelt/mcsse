import type { ServerTag } from "./ServerTag";


export type Server = {
  ip_address: string;
  name: string;
  version: string;
  players_online: number;
  max_players: number;
  motd: string;
  banner: string;
  added_at: string; // ISO date string
  status: "online" | "offline" | "unknown";
  total_votes: number;
  country: string;
  tags: ServerTag[];
};