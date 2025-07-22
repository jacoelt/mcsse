import { Button, InputAdornment, Stack, TextField } from "@mui/material";
import type { SearchParams } from "../types/SearchParams";
import { Replay, SearchOutlined } from "@mui/icons-material";
import SelectMultiple from "./generic/SelectMultiple";
import { useState } from "react";
import type { SearchValuesList } from "../types/SearchValuesList";
import { SelectSimple } from "./generic/SelectSimple";
import { RangeSliderLog } from "./generic/RangeSliderLog";
import { DateDeltaSelector } from "./generic/DateDeltaSelector";
// import { getLanguageFromCode } from "../helpers/languages";


interface SearchBarProps {
  valuesList: SearchValuesList
  isLoading: boolean;
  initialSearch: SearchParams;
  handleSearch: (search: SearchParams) => void;
  sx?: React.CSSProperties;
}

export default function SearchBar({ valuesList, isLoading, initialSearch, handleSearch, sx }: SearchBarProps) {

  const [currentSearch, setCurrentSearch] = useState<SearchParams>(initialSearch);

  return (
    <Stack direction="column" spacing={5} sx={{ padding: 3, paddingRight: 6, ...sx }}>
      <TextField
        variant="outlined"
        label="Search Server name or IP"
        value={currentSearch.query || ""}
        onChange={(e) => {
          const query = e.target.value.trim();
          setCurrentSearch((prev) => ({ ...prev, query }));
        }}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            handleSearch(currentSearch);
            e.preventDefault();
          }
        }}
        slotProps={{
          input: {
            startAdornment: (
              <InputAdornment position="start">
                <SearchOutlined />
              </InputAdornment>
            ),
          },
        }}
      />

      <SelectMultiple
        label="Version"
        isLoading={isLoading}
        itemList={valuesList.versions.map((version) => ({ value: version }))}
        onChange={(selection: string[]) => {
          setCurrentSearch((prev) => ({ ...prev, versions: selection }));
        }}
        selection={currentSearch.versions || []}
      />

      <SelectSimple
        label="Edition"
        itemList={valuesList.editions}
        onChange={(selection) => {
          setCurrentSearch((prev) => ({ ...prev, edition: selection }));
        }}
        selection={currentSearch.edition || "both"}
      />

      <RangeSliderLog
        label="Online Players"
        min={0}
        max={valuesList.maxOnlinePlayers}
        onChange={(value) => {
          if (Array.isArray(value)) {
            setCurrentSearch((prev) => ({
              ...prev,
              players_online_min: value[0],
              players_online_max: value[1],
            }));
          }
        }}
        value={[
          currentSearch.players_online_min === undefined ? 0 : currentSearch.players_online_min,
          currentSearch.players_online_max === undefined ? valuesList.maxOnlinePlayers : currentSearch.players_online_max
        ]}
      />

      <RangeSliderLog
        label="Max Players"
        min={0}
        max={valuesList.maxMaxPlayers}
        onChange={(value) => {
          if (Array.isArray(value)) {
            setCurrentSearch((prev) => ({
              ...prev,
              max_players_min: value[0],
              max_players_max: value[1],
            }));
          }
        }}
        value={[
          currentSearch.max_players_min === undefined ? 0 : currentSearch.max_players_min,
          currentSearch.max_players_max === undefined ? valuesList.maxMaxPlayers : currentSearch.max_players_max
        ]}
      />

      <DateDeltaSelector
        label="Date Added"
        onChange={(value) => {
          setCurrentSearch((prev) => ({ ...prev, days_prior: value }));
        }}
        valueList={valuesList.dates}
        value={currentSearch.days_prior || valuesList.dates[valuesList.dates.length - 1].value} // Default to the last item in the list
      />

      <SelectMultiple
        label="Server Status"
        isLoading={isLoading}
        itemList={valuesList.statuses}
        onChange={(selection: string[]) => {
          setCurrentSearch((prev) => ({ ...prev, statuses: selection as ("online" | "offline" | "unknown")[] }));
        }}
        selection={currentSearch.statuses || []}
      />

      <RangeSliderLog
        label="Total Votes"
        min={0}
        max={valuesList.maxVotes}
        onChange={(value) => {
          if (Array.isArray(value)) {
            setCurrentSearch((prev) => ({
              ...prev,
              total_votes_min: value[0],
              total_votes_max: value[1],
            }));
          }
        }}
        value={[
          currentSearch.total_votes_min === undefined ? 0 : currentSearch.total_votes_min,
          currentSearch.total_votes_max === undefined ? valuesList.maxVotes : currentSearch.total_votes_max
        ]}
      />

      <SelectMultiple
        label="Country"
        isLoading={isLoading}
        itemList={valuesList.countries.map((country) => (
          {
            value: country.code,
            label: `${country.flag} ${country.name}`,
            chip: `${country.flag} ${country.code}`,
            tooltip: country.name,
          }
        ))}
        onChange={(selection: string[]) => {
          setCurrentSearch((prev) => ({ ...prev, countries: selection }));
        }}
        selection={currentSearch.countries || []}
      />

      {/* No language is available from the minecraft server list we fetch
      <SelectMultiple
        label="Languages"
        itemList={valuesList.languages.map((language) => (
          {
            value: language,
            label: getLanguageFromCode(language),
          }
        ))}
        onChange={(selection: string[]) => {
          setCurrentSearch((prev) => ({ ...prev, languages: selection }));
        }}
        selection={currentSearch.languages || []}
      /> */}

      <SelectMultiple
        label="Tags"
        isLoading={isLoading}
        itemList={valuesList.tags.map((tag) => ({ value: tag.name, tooltip: tag.description }))}
        onChange={(selection: string[]) => {
          setCurrentSearch((prev) => ({ ...prev, tags: selection }));
        }}
        selection={currentSearch.tags || []}
      />

      <Stack direction="row" justifyContent="center" spacing={4}>
        <Button
          variant="outlined"
          color="secondary"
          startIcon={<Replay />}
          onClick={() => setCurrentSearch({} as SearchParams)}
        >
          Reset Filters
        </Button>

        <Button
          variant="contained"
          color="primary"
          startIcon={<SearchOutlined />}
          onClick={() => handleSearch(currentSearch)}
        >
          Search
        </Button>
      </Stack>
    </Stack>
  )
}