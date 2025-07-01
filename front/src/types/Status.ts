
export type Status = {
  value: "online";
  label: "Online";
} | {
  value: "offline";
  label: "Offline";
} | {
  value: "unknown";
  label: "Unknown";
}