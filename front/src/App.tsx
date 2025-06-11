import { useEffect, useState } from "react";
import ServerList from "./components/ServerList";
import type { Server } from "./types/Server";


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
    <div className="max-w-4xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Minecraft Server Explorer</h1>

      {serverFetchError ? (
        <p className="text-red-600">{serverFetchError}</p>
      ) : (
        <ServerList servers={servers} loading={loading} onViewDetails={handleViewDetails} />
      )}
    </div>
  );
}
