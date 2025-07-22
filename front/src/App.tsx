import { useEffect, useState } from "react";
import ServerList from "./components/ServerList";
import type { Server } from "./types/Server";
import { Drawer, IconButton, Stack, Typography, useMediaQuery, useTheme } from "@mui/material";
import Footer from "./components/footer/Footer";
import SearchBar from "./components/SearchBar";
import AdBox from "./components/AdBox";
import type { SearchParams } from "./types/SearchParams";
import type { SearchValuesList } from "./types/SearchValuesList";
import { getCountry } from "./helpers/countries";
import { ServerView } from "./components/ServerView";
import { SearchOutlined } from "@mui/icons-material";


const API_HOST = import.meta.env.VITE_API_HOST


const initialValuesList: SearchValuesList = {
  versions: [],
  editions: [
    { label: "Java", value: "java" },
    { label: "Bedrock", value: "bedrock" },
    { label: "Java & Bedrock", value: "both" },
  ],
  countries: [],
  languages: [],
  dates: [
    { label: "Last 24 hours", value: 1 },
    { label: "Last 7 days", value: 7 },
    { label: "Last month", value: 30 },
    { label: "Last 3 months", value: 90 },
    { label: "Last 6 months", value: 180 },
    { label: "Last year", value: 365 },
    { label: "Last 5 years", value: 1825 },
    { label: "All time", value: -1 },
  ],
  statuses: [
    { label: "Online", value: "online" },
    { label: "Offline", value: "offline" },
    { label: "Unknown", value: "unknown" },
  ],
  tags: [],
  maxVotes: 1_000_000,
  maxOnlinePlayers: 1_000_000,
  maxMaxPlayers: 1_000_000,
}


export default function App() {
  const [servers, setServers] = useState<Server[]>([]);
  const [loading, setLoading] = useState(true);
  const [serverFetchError, setServerFetchError] = useState<string | null>(null);
  const [currentViewedServer, setCurrentViewedServer] = useState<Server | null>(null);
  const [searchParams, setSearchParams] = useState<SearchParams>({});
  const [currentPage, setCurrentPage] = useState(1);
  const [searchValuesLists, setSearchValuesLists] = useState<SearchValuesList>(initialValuesList);
  const [isSearchValuesListLoading, setIsSearchValuesListLoading] = useState(false);
  const [isSearchBarVisible, setIsSearchBarVisible] = useState(false);

  const theme = useTheme();
  const isLargeScreen = useMediaQuery(theme.breakpoints.up("lg"));

  const pageSize = 10;
  const searchBarWidth = 500;

  const handleSearch = async (search: SearchParams, page?: number) => {
    setIsSearchBarVisible(false);
    setSearchParams(search);
    if (page === undefined) {
      setServers([]); // Clear server list for new search
      setCurrentPage(1); // Reset current page to 1
    }

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
    setIsSearchValuesListLoading(true);
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
        countries: data.countries.map((country: string) => getCountry(country)),
        languages: data.languages,
        dates: data.dates,
        statuses: data.statuses,
        tags: data.tags,
        maxVotes: data.max_votes,
        maxOnlinePlayers: data.max_online_players,
        maxMaxPlayers: data.max_max_players,
      })

      setIsSearchValuesListLoading(false);

    } catch (err) {
      console.error("Error fetching values list:", err);
    }
  }

  useEffect(() => {
    fetchValuesLists();
    handleSearch({});
  }, []);

  return (
    <Stack direction="column" spacing={2} sx={{ width: "100vw", height: "100vh", overflow: "hidden" }}>
      <Stack spacing={3}
        sx={{
          display: "flex",
          flexDirection: "row",
          width: "100%",
          height: "100vh",
          overflow: "hidden",
          position: "relative",
        }}
      >

        {!isLargeScreen && (
          <IconButton
            onClick={() => setIsSearchBarVisible(true)}
            sx={{
              position: "fixed",
              top: 16,
              left: 16,
              zIndex: 1000,
              backgroundColor: "white",
              boxShadow: 2,
              borderRadius: "50%",
            }}
          >
            <SearchOutlined />
          </IconButton>
        )}

        <Drawer
          anchor="left"
          open={isLargeScreen || isSearchBarVisible}
          onClose={() => setIsSearchBarVisible(false)}
          variant={isLargeScreen ? "persistent" : "temporary"}
          sx={{
            width: `${searchBarWidth}px`,
            flexShrink: 0,
            "& .MuiDrawer-paper": {
              width: `${searchBarWidth}px`,
              boxSizing: "border-box",
            },

          }}
        >
          <Typography variant="h4" sx={{ padding: 2, textAlign: "center" }}>
            Search Servers
          </Typography>
          <SearchBar
            valuesList={searchValuesLists}
            isLoading={isSearchValuesListLoading}
            initialSearch={searchParams}
            handleSearch={(search) => { handleSearch(search) }}
          />
        </Drawer>
        <Stack
          sx={{
            display: "flex",
            flexDirection: "column",
            width: isLargeScreen ? `calc(100% - ${searchBarWidth}px - 100px)` : `calc(100% - 100px)`,
          }}
        >
          <Typography variant="h3" sx={{ display: "flex", justifyContent: "center" }}>Minecraft Server Explorer</Typography>
          <Typography variant="subtitle1" sx={{ display: "flex", justifyContent: "center" }}>Explore and join Minecraft servers easily!</Typography>

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
        </Stack>
        <AdBox sx={{ width: "100px" }} />
      </Stack>
      <Footer
        sx={{
          position: "fixed",
          bottom: 0,
          left: 0,
          right: 0,
          backgroundColor: "white",
          padding: 2,
          height: "40px",
        }}
      />
    </Stack>
  );
}
