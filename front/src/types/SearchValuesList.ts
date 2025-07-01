import type { Country } from "../helpers/countries";
import type { Edition } from "./Edition";
import type { ServerTag } from "./ServerTag";
import type { Status } from "./Status";

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
  statuses: Status[];
  tags: ServerTag[];
  maxVotes: number;
  maxOnlinePlayers: number;
  maxMaxPlayers: number;
}