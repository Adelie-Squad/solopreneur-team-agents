import fs from "fs";
import path from "path";
import { getRoutinesDir } from "../util/paths.js";

export interface RoutineConfig {
  id: string;
  name: string;
  cron: string; // node-cron format
  channel: string;
  emoji: string;
  memoryTargets: string[];
}

export const ROUTINES: RoutineConfig[] = [
  {
    id: "morning-brief",
    name: "Morning Brief",
    cron: "0 6 * * *",
    channel: "daily-brief",
    emoji: "📋",
    memoryTargets: [],
  },
  {
    id: "signal-scan",
    name: "Signal Scan",
    cron: "0 12 * * *",
    channel: "signals",
    emoji: "🔍",
    memoryTargets: ["signals.jsonl"],
  },
  {
    id: "experiment-check",
    name: "Experiment Check",
    cron: "0 16 * * *",
    channel: "experiments",
    emoji: "🧪",
    memoryTargets: ["experiments.jsonl"],
  },
  {
    id: "daily-log",
    name: "Daily Log",
    cron: "0 22 * * *",
    channel: "daily-brief",
    emoji: "📝",
    memoryTargets: ["decisions.jsonl"],
  },
  {
    id: "weekly-review",
    name: "Weekly Review",
    cron: "0 20 * * 0",
    channel: "weekly-review",
    emoji: "📊",
    memoryTargets: ["decisions.jsonl"],
  },
];

/** Load routine prompt from routines/{id}.md */
export function loadRoutinePrompt(routineId: string): string {
  const promptFile = path.join(getRoutinesDir(), `${routineId}.md`);
  if (fs.existsSync(promptFile)) {
    return fs.readFileSync(promptFile, "utf-8");
  }
  return `# ${routineId}\n\nPrompt file missing: routines/${routineId}.md`;
}
