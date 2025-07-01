
export type SearchParams = {
  query?: string; // Text search query
  versions?: string[]; // Array of versions to filter by
  edition?: string; // Edition filter
  players_online_min?: number; // Minimum players online
  players_online_max?: number; // Maximum players online
  max_players_min?: number; // Minimum max players
  max_players_max?: number; // Maximum max players
  days_prior?: number; // Number of days prior to filter by
  statuses?: ("online" | "offline" | "unknown")[]; // Server status
  total_votes_min?: number; // Minimum total votes
  total_votes_max?: number; // Maximum total votes
  countries?: string[]; // Array of countries to filter by
  languages?: string[]; // Array of languages to filter by
  tags?: string[]; // Array of tags to filter by
  sort_by?: "name" | "players_online" | "max_players" | "added_at" | "total_votes"; // Sort by field
  sort_order?: "asc" | "desc"; // Sort order
  page?: number; // Page number for pagination
  page_size?: number; // Number of results per page
}