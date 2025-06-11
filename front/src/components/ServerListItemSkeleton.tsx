
export default function ServerListItemSkeleton() {
  return (
    <div className="flex items-start p-4 rounded-2xl shadow-md bg-white gap-4 animate-pulse">
      <div className="w-16 h-16 bg-gray-200 rounded-xl" />
      <div className="flex-1 space-y-2">
        <div className="flex justify-between items-center">
          <div className="w-1/2 h-5 bg-gray-200 rounded" />
          <div className="w-16 h-4 bg-gray-200 rounded" />
        </div>
        <div className="w-full h-4 bg-gray-200 rounded" />
        <div className="w-3/4 h-4 bg-gray-200 rounded" />
        <div className="flex gap-2 mt-1">
          <div className="w-20 h-4 bg-gray-200 rounded" />
          <div className="w-24 h-4 bg-gray-200 rounded" />
        </div>
        <div className="flex gap-2 mt-2">
          <div className="w-12 h-4 bg-gray-200 rounded-full" />
          <div className="w-16 h-4 bg-gray-200 rounded-full" />
          <div className="w-14 h-4 bg-gray-200 rounded-full" />
        </div>
      </div>
      <div className="w-20 h-9 bg-gray-200 rounded-xl mt-1" />
    </div>
  );
}
