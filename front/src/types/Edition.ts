import type { SelectItem } from "./SelectItem";

export type Edition = SelectItem & {
  label: "Java";
  value: "java";
} | {
  label: "Bedrock";
  value: "bedrock";
} | {
  label: "Java & Bedrock";
  value: "both";
}
