import type { Country } from "../helpers/countries";
import type { Edition } from "./Edition";
import type { ServerTag } from "./ServerTag";

export type DateDelta = {
  label: string;
  value: string; // relative time like "1d" for 1 day
}

export type SearchValuesList = {
  versions: string[];
  editions: Edition[];
  countries: Country[];
  dates: DateDelta[];
  statuses: ("Online" | "Offline" | "Unknown")[];
  tags: ServerTag[];
  maxVotes: number;
}