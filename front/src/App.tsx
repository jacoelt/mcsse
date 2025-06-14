import { useEffect, useState } from "react";
import ServerList from "./components/ServerList";
import type { Server } from "./types/Server";
import { Box, Typography } from "@mui/material";
import Footer from "./components/Footer";
import SearchBar from "./components/SearchBar";
import AdBox from "./components/AdBox";


const API_HOST = import.meta.env.VITE_API_HOST


export default function App() {
  const [servers, setServers] = useState<Server[]>([]);
  const [loading, setLoading] = useState(true);
  const [serverFetchError, setServerFetchError] = useState<string | null>(null);

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

  const handleViewDetails = (server: Server) => {
    alert(`Joining ${server.name} at ${server.ip_address}...`);
  };

  return (
    <Box>
      <Box>
        <SearchBar />
        <Box>
          <Box>
            <Typography variant="h3">Minecraft Server Explorer</Typography>
            <Typography variant="subtitle1">Explore and join Minecraft servers easily!</Typography>
          </Box>
          <Box>
            {serverFetchError ? (
              <p className="text-red-600">{serverFetchError}</p>
            ) : (
              <ServerList servers={servers} loading={loading} onViewDetails={handleViewDetails} />
            )}
          </Box>
        </Box>
        <AdBox />
      </Box>
      <Footer />
    </Box>
  );
}
