import { Button, InputAdornment, Stack, TextField } from "@mui/material";
import type { SearchParams } from "../types/SearchParams";
import { SearchOutlined } from "@mui/icons-material";
import SelectMultiple from "./generic/SelectMultiple";
import React from "react";
import type { SearchValuesList } from "../types/SearchValuesList";
import { SelectSimple } from "./generic/SelectSimple";
import type { Edition } from "../types/Edition";
import { RangeSlider } from "./generic/RangeSlider";
import { DateDeltaSelector } from "./DateDeltaSelector";


interface SearchBarProps {
  valuesList: SearchValuesList
  initialSearch: SearchParams;
  handleSearch: (search: SearchParams) => void;
}

export default function SearchBar({valuesList, initialSearch, handleSearch}: SearchBarProps) {

  const [currentSearch, setCurrentSearch] = React.useState<SearchParams>(initialSearch);

  return (
    <Stack>
      <TextField variant="outlined"
        label="Search Server name or IP"
        value={currentSearch.query || ""}
        onChange={(e) => {
          const query = e.target.value.trim();
          setCurrentSearch((prev) => ({ ...prev, query }));
        }}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            handleSearch(currentSearch);
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
        itemList={valuesList.versions.map((version) => ({value: version}))}
        onChange={(selection) => {
          setCurrentSearch((prev) => ({ ...prev, versions: selection.map(item => item.value) }));
        }}
      />

      <SelectSimple sx={{ margin: 2 }} label="Edition" itemList={valuesList.editions} onChange={(selection) => {
        setCurrentSearch((prev) => ({ ...prev, edition: selection ? (selection as Edition).value : undefined }));
      }} />

      <RangeSlider
        label="Online Players"
        min={0}
        max={1000}
        onChange={(value) => {
          if (Array.isArray(value)) {
            setCurrentSearch((prev) => ({
              ...prev,
              players_online_min: value[0],
              players_online_max: value[1],
            }));
          }
        }}
      />

      <RangeSlider
        label="Max Players"
        min={0}
        max={1000}
        onChange={(value) => {
          if (Array.isArray(value)) {
            setCurrentSearch((prev) => ({
              ...prev,
              max_players_min: value[0],
              max_players_max: value[1],
            }));
          }
        }}
      />

      <DateDeltaSelector
        label="Date Added"
        onChange={(value) => {
          setCurrentSearch((prev) => ({ ...prev, date_added: value }));
        }}
        valueList={valuesList.dates}
      />

      <SelectMultiple
        label="Server Status"
        itemList={valuesList.statuses.map((status) => ({ value: status.toLowerCase(), label: status }))}
        onChange={(selection) => {
          setCurrentSearch((prev) => ({ ...prev, statuses: selection.map(item => item.value as "online" | "offline" | "unknown") }));
        }}
      />

      <RangeSlider
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
      />

      <SelectMultiple
        label="Country"
        itemList={valuesList.countries.map((country) => (
          {
            value: country.code,
            label: `${country.flag} ${country.name}`,
            chip: `${country.flag} ${country.code}`,
            tooltip: country.name,
          }
        ))}
        onChange={(selection) => {
          setCurrentSearch((prev) => ({ ...prev, countries: selection.map(item => item.value) }));
        }}
      />

      <SelectMultiple
        label="Tags"
        itemList={valuesList.tags.map((tag) => ({ value: tag.name, tooltip: tag.description }))}
        onChange={(selection) => {
          setCurrentSearch((prev) => ({ ...prev, tags: selection.map(item => item.value) }));
        }}
      />

      <Stack direction="row" justifyContent="center">
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