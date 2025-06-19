import { useEffect, useState } from "react";
import ServerList from "./components/ServerList";
import type { Server } from "./types/Server";
import { Box, Typography } from "@mui/material";
import Footer from "./components/Footer";
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

  const initialSearch: SearchParams = {}
  // Get initial search params from URL
  const handleSearch = (search: SearchParams) => {
    alert(`Searching for: ${JSON.stringify(search)}`);
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
    tags: [
      { name: "Survival", description: "Survival mode servers", relevance: 10 },
      { name: "Creative", description: "Creative mode servers", relevance: 10 },
      { name: "Minigames", description: "Servers with various minigames", relevance: 30 },
      { name: "PvP", description: "Player vs Player combat servers", relevance: 30 },
      { name: "Roleplay", description: "Roleplaying servers", relevance: 30 },
      { name: "Vanilla", description: "Vanilla Minecraft servers", relevance: 10 },
    ],
    dates: [
      { label: "Last 7 days", value: "7d" },
      { label: "Last month", value: "1m" },
      { label: "Last 3 months", value: "3m" },
      { label: "Last 6 months", value: "6m" },
      { label: "Last year", value: "1y" },
      { label: "Last 5 years", value: "5y" },
      { label: "All time", value: "" },
    ],
    statuses: ["Online", "Offline", "Unknown"],
    maxVotes: 10000,
  };

  useEffect(() => {
    const fetchServers = async () => {
      try {
        const res = await fetch(`${API_HOST}/api/servers`);
        if (!res.ok) throw new Error("Failed to fetch servers");
        const data = await res.json();
        setServers(data);
      } catch (err) {
        setServerFetchError((err as Error).message);
      } finally {
        setLoading(false);
      }
    };

    fetchServers();
  }, []);

  return (
    <Box>
      <Box>
        <SearchBar valuesList={searchValuesList} initialSearch={initialSearch} handleSearch={handleSearch} />
        <Box>
          <Box>
            <Typography variant="h3">Minecraft Server Explorer</Typography>
            <Typography variant="subtitle1">Explore and join Minecraft servers easily!</Typography>
          </Box>
          <Box>
            {serverFetchError ? (
              <p className="text-red-600">{serverFetchError}</p>
            ) : (
              <ServerList servers={servers} loading={loading} onViewDetails={setCurrentViewedServer} />
            )}

            <ServerView server={currentViewedServer} onClose={() => {setCurrentViewedServer(null)}} />
          </Box>
        </Box>
        <AdBox />
      </Box>
      <Footer />
    </Box>
  );
}
