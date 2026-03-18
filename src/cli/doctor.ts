import fs from "fs";
import path from "path";
import { execSync } from "child_process";
import chalk from "chalk";
import { loadEnv, loadProducts } from "../util/config.js";

function check(label: string, ok: boolean, hint?: string): boolean {
  if (ok) {
    console.log(` ${chalk.green("✓")} ${label}`);
  } else {
    console.log(` ${chalk.red("✗")} ${label}${hint ? chalk.dim(` — ${hint}`) : ""}`);
  }
  return ok;
}

function commandExists(cmd: string): boolean {
  try {
    execSync(`which ${cmd} 2>/dev/null || where ${cmd} 2>nul`, { stdio: "ignore" });
    return true;
  } catch {
    return false;
  }
}

export async function doctorCommand(): Promise<void> {
  console.log(chalk.bold("\nSolo Founder Agents — Doctor\n"));

  let issues = 0;

  // 1. Runtime
  console.log(chalk.dim("Runtime:"));
  const nodeVer = parseInt(process.versions.node);
  if (!check("Node.js >= 18", nodeVer >= 18, `found v${process.versions.node}`)) issues++;
  if (!check("Docker", commandExists("docker"), "https://docs.docker.com/desktop/")) issues++;
  if (!check("git", commandExists("git"))) issues++;
  if (!check("Claude Code CLI", commandExists("claude"), "npm install -g @anthropic-ai/claude-code")) issues++;

  // 2. Configuration
  console.log(chalk.dim("\nConfiguration:"));
  const envExists = fs.existsSync(".env");
  if (!check(".env file", envExists, "Run: solo-agents init")) issues++;

  if (envExists) {
    const env = loadEnv();
    const messenger = env.MESSENGER || "discord";
    if (!check("MESSENGER set", !!env.MESSENGER, "Set MESSENGER in .env")) issues++;

    if (messenger.includes("discord")) {
      const hasToken = !!env.DISCORD_TOKEN && !env.DISCORD_TOKEN.includes("your-");
      if (!check("DISCORD_TOKEN", hasToken, "Set a valid Discord bot token")) issues++;
    }
    if (messenger.includes("slack")) {
      const hasBotToken = !!env.SLACK_BOT_TOKEN && !env.SLACK_BOT_TOKEN.includes("your-");
      const hasAppToken = !!env.SLACK_APP_TOKEN && !env.SLACK_APP_TOKEN.includes("your-");
      if (!check("SLACK_BOT_TOKEN", hasBotToken, "Set a valid Slack bot token")) issues++;
      if (!check("SLACK_APP_TOKEN", hasAppToken, "Set a valid Slack app token")) issues++;
    }
    if (messenger.includes("telegram")) {
      const hasToken = !!env.TELEGRAM_BOT_TOKEN && !env.TELEGRAM_BOT_TOKEN.includes("your-");
      if (!check("TELEGRAM_BOT_TOKEN", hasToken, "Set a valid Telegram bot token")) issues++;
      if (!check("TELEGRAM_CHAT_ID", !!env.TELEGRAM_CHAT_ID && env.TELEGRAM_CHAT_ID !== "your-chat-id")) issues++;
    }

    const reposPath = env.REPOS_BASE_PATH || "";
    if (!check("REPOS_BASE_PATH exists", !!reposPath && fs.existsSync(reposPath), `Path: ${reposPath}`)) issues++;
  }

  // 3. Project structure
  console.log(chalk.dim("\nProject structure:"));
  if (!check("core/products.json", fs.existsSync("core/products.json"), "Run: solo-agents init")) issues++;
  if (!check("agents/", fs.existsSync("agents"), "Run: solo-agents init")) issues++;
  if (!check("routines/", fs.existsSync("routines"), "Run: solo-agents init")) issues++;

  const products = loadProducts();
  if (!check(`Products registered (${products.length})`, products.length > 0, "Run: solo-agents init")) issues++;

  // 4. Summary
  console.log();
  if (issues === 0) {
    console.log(chalk.green.bold("✓ All checks passed. System is ready.\n"));
  } else {
    console.log(chalk.yellow(`⚠ ${issues} issue(s) found. Fix them and run again.\n`));
  }
}
