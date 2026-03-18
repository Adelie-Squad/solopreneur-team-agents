import fs from "fs";
import path from "path";
import cron from "node-cron";
import { createAdapters } from "../messenger/index.js";
import { runClaude } from "../bot/claude-runner.js";
import { loadProducts, loadMessengerConfig } from "../util/config.js";
import { getReposBase } from "../util/paths.js";
import { ROUTINES, loadRoutinePrompt, type RoutineConfig } from "./routines.js";
import { saveRoutineMemory } from "./memory.js";
import type { MessengerAdapter } from "../messenger/base.js";

let adapters: MessengerAdapter[] = [];

function now(): string {
  return new Date().toLocaleString("ko-KR", { timeZone: "Asia/Seoul" }).slice(5);
}

async function runRoutineForProduct(
  routine: RoutineConfig,
  product: { name: string; slug: string }
): Promise<void> {
  const productDir = path.join(getReposBase(), product.slug);
  console.log(`[Scheduler] ${product.name} - ${routine.name} starting`);

  const prompt = loadRoutinePrompt(routine.id);
  const result = await runClaude(prompt, productDir, 180_000);

  // Auto-save to memory
  saveRoutineMemory(result, routine, productDir);

  // Save routine log
  const logDir = path.join(productDir, "memory", "routine-logs");
  fs.mkdirSync(logDir, { recursive: true });
  const timestamp = new Date().toISOString().slice(0, 16).replace(/[:-]/g, "").replace("T", "-");
  fs.writeFileSync(
    path.join(logDir, `${routine.id}-${timestamp}.md`),
    `# ${routine.name}\n\n${result}`
  );

  // Send to all connected messengers
  const title = `${routine.emoji} [${routine.name}] ${product.name} | ${now()}`;
  for (const adapter of adapters) {
    const config = loadMessengerConfig(product.slug, adapter.platform);
    const sent = await adapter.sendToChannel(config, routine.channel, result, title);
    if (sent) {
      console.log(`[Scheduler] ${product.name} - ${routine.name} → ${adapter.platform} sent`);
    } else {
      console.log(`[Scheduler] ${product.name} - No ${adapter.platform} config. Saved to file only.`);
    }
  }
}

async function runRoutine(routineId: string): Promise<void> {
  const routine = ROUTINES.find((r) => r.id === routineId);
  if (!routine) {
    console.log(`[Scheduler] Unknown routine: ${routineId}`);
    return;
  }

  const products = loadProducts();
  if (!products.length) {
    console.log("[Scheduler] No products registered");
    return;
  }

  await Promise.all(products.map((p) => runRoutineForProduct(routine, p)));
}

async function sendStartupNotification(): Promise<void> {
  const products = loadProducts();
  const msg =
    "**AI Assistant System Started**\nRoutine schedule:\n" +
    ROUTINES.map((r) => `• ${r.emoji} ${r.name}: ${r.cron}`).join("\n");

  for (const adapter of adapters) {
    for (const product of products) {
      const config = loadMessengerConfig(product.slug, adapter.platform);
      await adapter.sendToChannel(config, "daily-brief", msg);
    }
  }
}

export async function startScheduler(): Promise<void> {
  adapters = await createAdapters();
  const platforms = adapters.map((a) => a.platform);
  console.log(`[Scheduler] Using adapters: ${platforms.join(", ")}`);

  // Start notifier mode for all adapters
  for (const adapter of adapters) {
    await adapter.startNotifier();
    console.log(`[Scheduler] ${adapter.platform} notifier started`);
  }

  // Register cron jobs
  for (const routine of ROUTINES) {
    cron.schedule(routine.cron, () => runRoutine(routine.id), {
      timezone: "Asia/Seoul",
    });
    console.log(`[Scheduler] Registered: ${routine.name} (${routine.cron})`);
  }

  console.log("[Scheduler] Scheduler started");
  await sendStartupNotification();

  // Keep alive
  await new Promise<void>(() => {});
}
