#!/usr/bin/env python3
"""
Solo Founder Agents Setup Wizard
Run: python setup.py
"""

import os
import sys
import json
import subprocess
import shutil
from pathlib import Path

# Install rich if missing
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.table import Table
    from rich import print as rprint
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich", "-q"])
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.table import Table
    from rich import print as rprint

console = Console()

# ──────────────────────────────────────────────
# Utilities
# ──────────────────────────────────────────────


def check_command(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def run(cmd: str, cwd=None, capture=True):
    result = subprocess.run(
        cmd, shell=True, cwd=cwd, capture_output=capture, text=True
    )
    return result.returncode == 0, result.stdout.strip()


def load_env() -> dict:
    env = {}
    env_file = Path(".env")
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env


def save_env(updates: dict):
    env_file = Path(".env")
    env = load_env()
    env.update(updates)
    lines = []
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            stripped = line.strip()
            if (
                stripped
                and not stripped.startswith("#")
                and "=" in stripped
            ):
                k = stripped.split("=", 1)[0].strip()
                if k in updates:
                    lines.append(f"{k}={updates[k]}")
                    updates.pop(k, None)
                else:
                    lines.append(line)
            else:
                lines.append(line)
    for k, v in updates.items():
        lines.append(f"{k}={v}")
    env_file.write_text("\n".join(lines) + "\n")


# ──────────────────────────────────────────────
# Step-by-step setup
# ──────────────────────────────────────────────


def step_welcome():
    console.print(
        Panel.fit(
            "[bold cyan]Solo Founder Agents[/bold cyan] Setup Wizard\n\n"
            "Build a 24/7 AI assistant system tailored to your products.\n"
            "Estimated time: ~5-10 minutes",
            title="Welcome",
        )
    )


def step_check_deps():
    console.print("\n[bold]-- Step 1: Environment Check --[/bold]")

    checks = {
        "Docker": check_command("docker"),
        "Python 3.10+": sys.version_info >= (3, 10),
        "git": check_command("git"),
    }

    table = Table(show_header=False, box=None)
    all_ok = True
    for name, ok in checks.items():
        status = "[green]v[/green]" if ok else "[red]x[/red]"
        table.add_row(status, name)
        if not ok:
            all_ok = False
    console.print(table)

    if not checks["Docker"]:
        console.print("\n[red]Docker is required.[/red]")
        console.print("Install: https://docs.docker.com/desktop/")
        sys.exit(1)

    return True


def step_configure():
    console.print("\n[bold]-- Step 2: Basic Configuration --[/bold]")

    if not Path(".env").exists():
        shutil.copy(".env.example", ".env")
        console.print("[dim].env file created[/dim]")

    env = load_env()
    updates = {}

    # Owner info
    if not env.get("OWNER_NAME"):
        name = Prompt.ask("Your name")
        updates["OWNER_NAME"] = name

    if not env.get("OWNER_ROLE"):
        role = Prompt.ask("Your role (e.g. developer, designer, PM)")
        updates["OWNER_ROLE"] = role

    # ── Messenger platform selection ──
    console.print("\n[bold]Select messenger platform:[/bold]")
    console.print("  [cyan]1[/cyan]. Discord  — Best for team channels, auto-creates channels")
    console.print("  [cyan]2[/cyan]. Slack    — Great for workspace integration, Socket Mode")
    console.print("  [cyan]3[/cyan]. Telegram — Lightweight, works from mobile\n")

    messenger_choice = Prompt.ask(
        "Choose platform", choices=["1", "2", "3"], default="1"
    )
    messenger_map = {"1": "discord", "2": "slack", "3": "telegram"}
    messenger = messenger_map[messenger_choice]
    updates["MESSENGER"] = messenger

    if messenger == "discord":
        _configure_discord(env, updates)
    elif messenger == "slack":
        _configure_slack(env, updates)
    elif messenger == "telegram":
        _configure_telegram(env, updates)

    # GitHub token (optional)
    current_gh = env.get("GITHUB_TOKEN", "")
    if not current_gh or current_gh == "your-github-token-here":
        want_gh = Confirm.ask(
            "\nEnable auto GitHub repo creation? (optional)"
        )
        if want_gh:
            console.print(
                "GitHub Settings → Developer settings → PAT → Fine-grained"
            )
            gh_token = Prompt.ask("GitHub Token", password=True)
            updates["GITHUB_TOKEN"] = gh_token
        else:
            updates["GITHUB_TOKEN"] = ""

    # Repos path
    default_path = str(Path.home() / "repos")
    repos_path = Prompt.ask("Project storage path", default=default_path)
    Path(repos_path).mkdir(parents=True, exist_ok=True)
    updates["REPOS_BASE_PATH"] = repos_path

    if updates:
        save_env(updates)
        console.print("[green]v .env saved[/green]")

    # Update OWNER.md
    env = load_env()
    owner_md = Path("core/OWNER.md")
    if owner_md.exists():
        owner_name = env.get("OWNER_NAME", "")
        owner_role = env.get("OWNER_ROLE", "")
        if owner_name:
            content = owner_md.read_text()
            content = content.replace(
                "- 이름: (setup.py에서 자동 설정)",
                f"- 이름: {owner_name}",
            )
            content = content.replace(
                "- 역할: (setup.py에서 자동 설정)",
                f"- 역할: {owner_role}",
            )
            owner_md.write_text(content)

    return True


def _configure_discord(env: dict, updates: dict):
    """Configure Discord bot token."""
    current_token = env.get("DISCORD_TOKEN", "")
    if not current_token or current_token == "your-discord-bot-token-here":
        console.print(
            "\n[yellow]Discord Bot Token required.[/yellow]"
        )
        console.print("1. Go to https://discord.com/developers/applications")
        console.print("2. New Application → Bot → Reset Token")
        console.print("3. Paste below\n")
        token = Prompt.ask("Discord Bot Token", password=True)
        updates["DISCORD_TOKEN"] = token


def _configure_slack(env: dict, updates: dict):
    """Configure Slack bot and app tokens."""
    current_bot = env.get("SLACK_BOT_TOKEN", "")
    if not current_bot or current_bot.startswith("xoxb-your"):
        console.print(
            "\n[yellow]Slack tokens required.[/yellow]"
        )
        console.print("1. Go to https://api.slack.com/apps → Create New App")
        console.print("2. OAuth & Permissions → Add scopes:")
        console.print("   channels:read, channels:manage, chat:write, groups:read")
        console.print("3. Install to Workspace → Copy Bot Token (xoxb-...)")
        console.print("4. Socket Mode → Enable → Generate App Token (xapp-...)\n")

        bot_token = Prompt.ask("Slack Bot Token (xoxb-...)", password=True)
        app_token = Prompt.ask("Slack App Token (xapp-...)", password=True)
        updates["SLACK_BOT_TOKEN"] = bot_token
        updates["SLACK_APP_TOKEN"] = app_token

    channel = Prompt.ask(
        "Command channel name", default="owner-command"
    )
    updates["SLACK_COMMAND_CHANNEL"] = channel


def _configure_telegram(env: dict, updates: dict):
    """Configure Telegram bot token and chat ID."""
    current_token = env.get("TELEGRAM_BOT_TOKEN", "")
    if not current_token or current_token == "your-telegram-bot-token":
        console.print(
            "\n[yellow]Telegram Bot Token required.[/yellow]"
        )
        console.print("1. Open Telegram and message @BotFather")
        console.print("2. /newbot → follow prompts → copy token")
        console.print("3. Get your chat ID from @userinfobot\n")

        token = Prompt.ask("Telegram Bot Token", password=True)
        updates["TELEGRAM_BOT_TOKEN"] = token

    current_chat = env.get("TELEGRAM_CHAT_ID", "")
    if not current_chat or current_chat == "your-chat-id":
        chat_id = Prompt.ask("Telegram Chat ID")
        updates["TELEGRAM_CHAT_ID"] = chat_id


def step_setup_products():
    console.print("\n[bold]-- Step 3: Register Products --[/bold]")
    console.print("Register the products or organizations to manage.\n")

    products = []

    while True:
        name = Prompt.ask(
            "Product/Organization name\n"
            "Press Enter when done"
        )
        if not name:
            if not products:
                console.print(
                    "[yellow]At least 1 product is required.[/yellow]"
                )
                continue
            break

        org = Prompt.ask(
            f"  GitHub org for {name} (Enter to skip)", default=""
        )

        products.append(
            {
                "name": name,
                "slug": name.lower().replace(" ", "-"),
                "github_org": org,
            }
        )

        console.print(f"[green]  v {name} registered[/green]\n")

        more = Confirm.ask("Add more products?")
        if not more:
            break

    # Save products.json
    products_file = Path("core/products.json")
    products_file.parent.mkdir(exist_ok=True)
    products_file.write_text(
        json.dumps(products, ensure_ascii=False, indent=2)
    )

    # Create directory structure for each product
    env = load_env()
    repos_path = Path(env.get("REPOS_BASE_PATH", "./repos"))
    messenger = env.get("MESSENGER", "discord")

    for product in products:
        _create_product_structure(product, repos_path, env, messenger)

    save_env({"PRODUCTS": ",".join(p["slug"] for p in products)})
    return products


def _create_product_structure(
    product: dict, repos_path: Path, env: dict, messenger: str
):
    """Create product directory structure."""
    slug = product["slug"]
    product_dir = repos_path / slug

    dirs = [
        product_dir / "product",
        product_dir / "memory",
        product_dir / "projects",
        product_dir / messenger,  # discord/, slack/, or telegram/
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    # product/brief.md
    brief_file = product_dir / "product" / "brief.md"
    if not brief_file.exists():
        brief_file.write_text(
            f"""# {product['name']} -- Product Brief

## One-line Positioning
(To be written)

## Current Stage
PMF Discovery

## Target Customer
(To be written)

## Riskiest Assumption (Current)
(To be written)

## Validation Method
(To be written)
"""
        )

    # product/weekly-state.md
    weekly_file = product_dir / "product" / "weekly-state.md"
    if not weekly_file.exists():
        weekly_file.write_text(
            f"""# {product['name']} -- This Week's Focus

## Goal This Week
(Update weekly)

## Riskiest Assumption
(The riskiest hypothesis to validate this week)

## Blockers
(Bottlenecks)
"""
        )

    # Memory JSONL schema init
    schemas = {
        "hypotheses.jsonl": '{"_schema":"hypothesis","fields":["id","statement","risk","method","status","date"]}\n',
        "experiments.jsonl": '{"_schema":"experiment","fields":["id","hypothesis_id","method","result","signal_strength","date","next_action"]}\n',
        "decisions.jsonl": '{"_schema":"decision","fields":["date","decision","alternatives","reasoning","emotion_weight"]}\n',
        "signals.jsonl": '{"_schema":"signal","fields":["date","source","type","content","relevance","action"]}\n',
    }
    for fname, schema in schemas.items():
        f = product_dir / "memory" / fname
        if not f.exists():
            f.write_text(schema)

    # CLAUDE.md
    _generate_product_claude_md(product, product_dir, env)

    # Messenger config
    _generate_messenger_config(product, product_dir, messenger)

    console.print(
        f"[green]  v {product['name']} directory created:"
        f" {product_dir}[/green]"
    )


def _generate_product_claude_md(
    product: dict, product_dir: Path, env: dict
):
    """Auto-generate product-level CLAUDE.md."""
    agents_dir = Path(__file__).parent.resolve()
    core_path = agents_dir / "core"

    content = f"""# CLAUDE.md -- {product['name']}
# Auto-generated. Feel free to edit.

## Identity
Dedicated AI team for {product['name']}.
No other products exist in this session.

## Owner Context
@{core_path}/OWNER.md
@{core_path}/PRINCIPLES.md
@{core_path}/VOICE.md

## Product Context
@./product/brief.md
@./product/weekly-state.md

## Memory (latest entries only)
@./memory/signals.jsonl

## Working Principles
1. Validate first -- behavioral data before coding
2. Single focus -- concentrate on this week's Riskiest Assumption only
3. Report -- auto-report to messenger upon task completion

## Never Do
- Mention other products (no context pollution)
- Suggest development before validation
- Suggest vague mass-targeting
"""

    claude_md = product_dir / "CLAUDE.md"
    claude_md.write_text(content)


def _generate_messenger_config(
    product: dict, product_dir: Path, messenger: str
):
    """Generate messenger-specific config file."""
    config_file = product_dir / messenger / "config.yaml"
    if config_file.exists():
        return

    slug = product["slug"]
    name = product["name"]

    if messenger == "discord":
        config_file.write_text(
            f"""# {name} Discord config
# Auto-filled after bot connects to server
product_name: {name}
product_slug: {slug}
guild_id: null
channels:
  daily_brief: null
  experiments: null
  weekly_review: null
  signals: null
  owner_command: null
  errors: null
"""
        )
    elif messenger == "slack":
        config_file.write_text(
            f"""# {name} Slack config
# Fill channel IDs after creating channels in Slack
product_name: {name}
product_slug: {slug}
channels:
  daily_brief: null
  experiments: null
  weekly_review: null
  signals: null
  owner_command: null
  errors: null
"""
        )
    elif messenger == "telegram":
        config_file.write_text(
            f"""# {name} Telegram config
# chat_id: Main chat/group ID for this product
# channels: Use separate group IDs per channel, or same chat_id for all
product_name: {name}
product_slug: {slug}
chat_id: null
channels:
  daily_brief: null
  experiments: null
  weekly_review: null
  signals: null
  owner_command: null
  errors: null
"""
        )


def step_build_docker():
    console.print("\n[bold]-- Step 4: Docker Build --[/bold]")
    console.print("This runs once. (~2-3 minutes)\n")

    ok, _ = run("docker compose build", capture=False)
    if not ok:
        console.print(
            "[red]Docker build failed."
            " Check docker-compose.yml.[/red]"
        )
        sys.exit(1)

    console.print("[green]v Docker build complete[/green]")
    return True


def step_invite_bot():
    env = load_env()
    messenger = env.get("MESSENGER", "discord")

    if messenger == "discord":
        _invite_discord_bot()
    elif messenger == "slack":
        _invite_slack_bot()
    elif messenger == "telegram":
        _invite_telegram_bot()


def _invite_discord_bot():
    console.print("\n[bold]-- Step 5: Invite Discord Bot --[/bold]")
    console.print(
        "\n[yellow]Invite your Discord bot to your server(s).[/yellow]"
    )
    console.print("\n1. Go to https://discord.com/developers/applications")
    console.print("2. Select your app → 'General Information'")
    console.print("3. Copy Application ID\n")

    app_id = Prompt.ask("Application ID")

    scopes = "bot+applications.commands"
    permissions = "8"  # Administrator
    invite_url = (
        f"https://discord.com/api/oauth2/authorize"
        f"?client_id={app_id}"
        f"&permissions={permissions}"
        f"&scope={scopes}"
    )

    console.print(f"\n[cyan]Bot invite link:[/cyan]")
    console.print(f"[link={invite_url}]{invite_url}[/link]")
    console.print(
        "\nUse this link to invite the bot to all your Discord servers."
    )

    Confirm.ask("Done inviting to all servers?")
    save_env({"DISCORD_APP_ID": app_id})


def _invite_slack_bot():
    console.print("\n[bold]-- Step 5: Slack Bot Setup --[/bold]")
    console.print(
        "\n[yellow]Make sure your Slack bot is installed to your workspace.[/yellow]"
    )
    console.print("\n1. Go to https://api.slack.com/apps → Select your app")
    console.print("2. Install App → Install to Workspace")
    console.print("3. Create channels: owner-command, daily-brief, signals, experiments, weekly-review, errors")
    console.print("4. Invite bot to each channel: /invite @YourBot\n")

    Confirm.ask("Done setting up Slack channels?")


def _invite_telegram_bot():
    console.print("\n[bold]-- Step 5: Telegram Bot Setup --[/bold]")
    console.print(
        "\n[yellow]Make sure your Telegram bot is set up.[/yellow]"
    )
    console.print("\n1. Start a conversation with your bot on Telegram")
    console.print("2. Send /start to activate it")
    console.print("3. (Optional) Create a group and add the bot for team use\n")

    Confirm.ask("Done setting up Telegram bot?")


def step_start():
    console.print("\n[bold]-- Step 6: Start System --[/bold]\n")

    ok, _ = run("docker compose up -d", capture=False)
    if not ok:
        console.print("[red]Failed to start[/red]")
        sys.exit(1)

    console.print("[green]v System started[/green]")


def step_finish(products):
    env = load_env()
    messenger = env.get("MESSENGER", "discord").capitalize()

    console.print(
        Panel.fit(
            "[bold green]Setup Complete![/bold green]\n\n"
            "[bold]What you can do now:[/bold]\n\n"
            f"- Send messages via {messenger} → agents respond\n"
            "- Create new project: [cyan]python cli/new_project.py[/cyan]\n"
            "- Check status: [cyan]python cli/status.py[/cyan]\n"
            "- Restart system: [cyan]docker compose restart[/cyan]\n"
            "- View logs: [cyan]docker compose logs -f[/cyan]\n\n"
            "[bold]Registered products:[/bold]\n"
            + "\n".join(f"  - {p['name']}" for p in products)
            + "\n\n[yellow]Note: Claude Code Max plan is required.[/yellow]\n"
            "[dim]Auth inside Docker: docker compose exec bot claude login[/dim]",
            title="Done",
        )
    )


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────


def main():
    step_welcome()
    step_check_deps()
    step_configure()
    products = step_setup_products()
    step_build_docker()
    step_invite_bot()
    step_start()
    step_finish(products)


if __name__ == "__main__":
    main()
