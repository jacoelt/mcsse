import { useEffect, useState } from "react";
import ServerList from "./components/ServerList";
import type { Server } from "./types/Server";
import { Box, Grid, Stack, Typography } from "@mui/material";
import Footer from "./components/footer/Footer";
import SearchBar from "./components/SearchBar";
import AdBox from "./components/AdBox";
import type { SearchParams } from "./types/SearchParams";
import type { SearchValuesList } from "./types/SearchValuesList";
import { getCountry } from "./helpers/countries";
import { ServerView } from "./components/ServerView";


const API_HOST = import.meta.env.VITE_API_HOST


export default function App() {
  const [servers, setServers] = useState<Server[]>([]);
  const [loading, setLoading] = useState(true);
  const [serverFetchError, setServerFetchError] = useState<string | null>(null);
  const [currentViewedServer, setCurrentViewedServer] = useState<Server | null>(null);
  const [searchParams, setSearchParams] = useState<SearchParams>({});
  const [currentPage, setCurrentPage] = useState(1);
  const [searchValuesLists, setSearchValuesLists] = useState<SearchValuesList | null>(null);

  const pageSize = 10;

  const handleSearch = async (search: SearchParams, page?: number) => {
    setSearchParams(search);

    try {
      setLoading(true);
      setServerFetchError(null);
      setCurrentViewedServer(null);
      const res = await fetch(`${API_HOST}/api/servers`, {
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json",
        },
        method: "POST",
        body: JSON.stringify({
          ...search,
          page: page || 1,
          limit: pageSize,
        }),
      });
      if (!res.ok) throw new Error("Failed to fetch servers");
      const data = await res.json();

      if (page && page > 1) {
        // If loading more, append to existing servers
        setServers(prev => [...prev, ...data]);
      } else {
        // If initial search, replace existing servers
        setServers(data);
      }

    } catch (err) {
      setServerFetchError((err as Error).message);

    } finally {
      setLoading(false);
    }
  }

  const handleLoadMore = async () => {
    if (loading) return; // Prevent loading more while already loading
    setCurrentPage(prevPage => prevPage + 1); // Increment current page
    handleSearch(searchParams, currentPage + 1);
  }

  const fetchValuesLists = async () => {
    try {
      const res = await fetch(`${API_HOST}/api/values-lists`, {
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json",
        },
      });
      if (!res.ok) throw new Error("Failed to fetch values list");
      const data = await res.json();

      setSearchValuesLists({
        versions: data.versions,
        editions: data.editions,
        countries: data.countries.map((country: any) => ({
          ...country,
          name: getCountry(country.code),
        })),
        languages: data.languages,
        dates: data.dates,
        statuses: data.statuses,
        tags: data.tags,
        maxVotes: data.max_votes,
        maxOnlinePlayers: data.max_online_players,
        maxMaxPlayers: data.max_max_players,
      })

    } catch (err) {
      console.error("Error fetching values list:", err);
    }
  }

  useEffect(() => {
    fetchValuesLists();
    handleSearch({});
  }, []);


  return (
    <Stack direction="column" spacing={2} sx={{ padding: 2, minHeight: "100vh" }}>
      <Grid container spacing={3}>
        <Grid size={3}>
          {
            searchValuesLists &&
            <SearchBar valuesList={searchValuesLists} initialSearch={searchParams} handleSearch={handleSearch} />
          }
        </Grid>
        <Grid size={7} sx={{ display: "flex", flexDirection: "column" }}>
          <Typography variant="h3">Minecraft Server Explorer</Typography>
          <Typography variant="subtitle1">Explore and join Minecraft servers easily!</Typography>

          {serverFetchError ? (
            <p className="text-red-600">{serverFetchError}</p>
          ) : (
            <ServerList
              servers={servers}
              loading={loading}
              onViewDetails={setCurrentViewedServer}
              onLoadMore={handleLoadMore}
              hasMore={servers.length > 0 && servers.length % pageSize === 0}
            />
          )}

          <ServerView server={currentViewedServer} onClose={() => { setCurrentViewedServer(null) }} />
        </Grid>
        <Grid size={2}>
          <AdBox />
        </Grid>
      </Grid>
      <Footer />
    </Stack>
  );
}
