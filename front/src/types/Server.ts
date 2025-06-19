import type { ServerTag } from "./ServerTag";


export type Server = {
  id: string;
  ip_address_java: string;
  ip_address_bedrock: string;
  name: string;
  version: string;
  players_online: number;
  max_players: number;
  description: string;
  banner: string;
  added_at: string; // ISO date string
  status: "online" | "offline" | "unknown";
  total_votes: number;
  country: string;
  tags: ServerTag[];
  edition: "java" | "bedrock" | "both";
  website: string;
  discord: string;
  languages: string[];
};