import type { Country } from "../helpers/countries";
import type { Edition } from "./Edition";
import type { ServerTag } from "./ServerTag";

export type DateDelta = {
  label: string;
  value: number; // Value in days
}

export type SearchValuesList = {
  versions: string[];
  editions: Edition[];
  countries: Country[];
  languages: string[];
  dates: DateDelta[];
  statuses: ("Online" | "Offline" | "Unknown")[];
  tags: ServerTag[];
  maxVotes: number;
}