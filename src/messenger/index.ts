import type { MessengerAdapter } from "./base.js";

// Lazy imports to avoid loading all platform SDKs at startup
const adapterLoaders: Record<string, () => Promise<MessengerAdapter>> = {
  async discord() {
    const { DiscordAdapter } = await import("./discord-adapter.js");
    return new DiscordAdapter();
  },
  async slack() {
    const { SlackAdapter } = await import("./slack-adapter.js");
    return new SlackAdapter();
  },
  async telegram() {
    const { TelegramAdapter } = await import("./telegram-adapter.js");
    return new TelegramAdapter();
  },
};

async function createSingle(platform: string): Promise<MessengerAdapter> {
  const p = platform.trim().toLowerCase();
  const loader = adapterLoaders[p];
  if (!loader) throw new Error(`Unsupported messenger platform: ${p}`);
  return loader();
}

/** Create a single adapter (first configured platform). */
export async function createAdapter(platform?: string): Promise<MessengerAdapter> {
  const raw = platform || process.env.MESSENGER || "discord";
  const first = raw.split(",")[0].trim();
  return createSingle(first);
}

/** Create adapters for all configured platforms. */
export async function createAdapters(platforms?: string): Promise<MessengerAdapter[]> {
  const raw = platforms || process.env.MESSENGER || "discord";
  const names = raw.split(",").map((p) => p.trim().toLowerCase()).filter(Boolean);
  const seen = new Set<string>();
  const unique: string[] = [];
  for (const n of names) {
    if (!seen.has(n)) {
      seen.add(n);
      unique.push(n);
    }
  }
  return Promise.all(unique.map(createSingle));
}
