import { useEffect, useState } from "react";
import ServerList from "./components/ServerList";
import type { Server } from "./types/Server";
import { Box, Typography } from "@mui/material";
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

  useEffect(() => {
    handleSearch({});
  }, []);

  const handleLoadMore = async () => {
    if (loading) return; // Prevent loading more while already loading
    setCurrentPage(prevPage => prevPage + 1); // Increment current page
    handleSearch(searchParams, currentPage + 1);
  }

  const searchValuesList: SearchValuesList = {
    versions: ["1.20", "1.19", "1.18"],
    editions: [
      { value: "java", label: "Java" },
      { value: "bedrock", label: "Bedrock" },
      { value: "both", label: "Java & Bedrock" },
    ],
    countries: [
      getCountry("US"),
      getCountry("CA"),
      getCountry("GB"),
      getCountry("FR"),
      getCountry("DE"),
      getCountry("JP"),
      getCountry("AU"),
    ],
    languages: ["en", "es", "fr", "de", "ru", "zh", "ja", "ko", "pt", "it"],
    tags: [
      { name: "Survival", description: "Survival mode servers", relevance: 10 },
      { name: "Creative", description: "Creative mode servers", relevance: 10 },
      { name: "Minigames", description: "Servers with various minigames", relevance: 30 },
      { name: "PvP", description: "Player vs Player combat servers", relevance: 30 },
      { name: "Roleplay", description: "Roleplaying servers", relevance: 30 },
      { name: "Vanilla", description: "Vanilla Minecraft servers", relevance: 10 },
    ],
    dates: [
      { label: "Last 7 days", value: 7 },
      { label: "Last month", value: 30 },
      { label: "Last 3 months", value: 90 },
      { label: "Last 6 months", value: 180 },
      { label: "Last year", value: 365 },
      { label: "Last 5 years", value: 1825 },
      { label: "All time", value: -1 }, // -1 for all time
    ],
    statuses: ["Online", "Offline", "Unknown"],
    maxVotes: 10000,
  };

  return (
    <Box>
      <Box>
        <SearchBar valuesList={searchValuesList} initialSearch={searchParams} handleSearch={handleSearch} />
        <Box>
          <Box>
            <Typography variant="h3">Minecraft Server Explorer</Typography>
            <Typography variant="subtitle1">Explore and join Minecraft servers easily!</Typography>
          </Box>
          <Box>
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
          </Box>
        </Box>
        <AdBox />
      </Box>
      <Footer />
    </Box>
  );
}
