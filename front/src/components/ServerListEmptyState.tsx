import { ServerOff } from "lucide-react";

export default function ServerListEmptyState() {
  return (
    <div className="text-center text-gray-500 py-12">
      <ServerOff className="mx-auto w-10 h-10 mb-2" />
      <p className="text-lg font-medium">Aucun serveur trouvé</p>
      <p className="text-sm">Réessaie plus tard ou ajuste tes filtres.</p>
    </div>
  );
}
