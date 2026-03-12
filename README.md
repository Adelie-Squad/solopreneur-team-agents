# Solo Founder Agents

> A 24/7 AI assistant system for solo founders. Operates product-specific agents using Claude Code.

Running a company alone doesn't mean working alone. Solo Founder Agents gives you a full virtual team — 23 specialized AI agents organized into 4 teams — that operates around the clock via your favorite messenger, scheduled routines, and CLI tools. Just talk to it like you'd talk to a co-founder, and the right specialist picks up.

**Supports:** Discord | Slack | Telegram — choose during setup.

---

## What This Is

A self-hosted AI operations system that turns Claude Code into a **team of domain experts** for your startup. Instead of one generic chatbot, you get:

- A **Strategy team** that validates PMF hypotheses, scopes features, and analyzes data
- A **Growth team** that writes copy, plans GTM, and runs paid campaigns
- An **Experience team** that conducts user research, designs UX flows, and builds UI systems
- An **Engineering team** that architects systems, writes code, manages infra, and collects data

Each agent carries 200+ lines of domain-specific expertise — not generic instructions, but structured frameworks, quality checklists, and handoff protocols that mirror how real teams operate.

---

## Why This Exists

Solo founders face a structural disadvantage: every decision — strategy, design, marketing, engineering — falls on one person. AI can help, but a single chat thread doesn't scale. You end up re-explaining context, losing decisions, and doing shallow work across too many domains.

This system solves that by giving each domain its own specialist agent, persistent memory, and structured workflows — so you can think at the strategic level while your agents handle the execution depth.

---

## Key Features

### 23 Agents, 4 Teams, 1 Command

Send a message in your messenger. The system analyzes your intent across 60+ keywords and routes it to the right specialist. No manual selection needed.

```
You: "Analyze our signup funnel drop-off"
→ Routes to Data Analyst (Strategy team)

You: "Write a launch announcement for Product Hunt"
→ Routes to Content Writer (Growth team)
```

### Multi-Platform Messenger Support

Pick the platform that fits your workflow:

| Platform | Best For | Key Advantage |
|----------|----------|---------------|
| **Discord** | Channel-based teams | Auto-creates channels, rich category organization |
| **Slack** | Workspace integration | Socket Mode, native workspace feel |
| **Telegram** | Lightweight / mobile | Simple setup, works anywhere |

Set `MESSENGER=discord|slack|telegram` in `.env` or select during `setup.py`. All platforms share the same agent routing, routines, and memory system.

### 3-Layer Context Isolation

The system prevents context bleeding across products and projects:

```
Layer 0: Universal     → Owner profile, principles, voice (shared everywhere)
Layer 1: Product       → Briefs, memory, signals (per-product)
Layer 2: Project       → Agents, experiments, status (per-project)
```

Each product gets its own workspace. Agents working on Product A never see Product B's data.

### Persistent Memory That Compounds

Routines run on schedule, extract structured data, and append to JSONL memory files. Over time, your agents build a growing knowledge base of signals, experiments, and decisions — so every interaction gets smarter.

### Multi-Session Team Orchestration

For complex projects (PMF validation, feature launches, rebranding), the Orchestrator breaks work into phases and coordinates multiple team sessions running in parallel:

```
Phase 1: Research    → User Researcher + Desk Researcher + Idea Refiner (parallel)
Phase 2: Planning    → PMF Planner + Feature Planner
Phase 3: Design      → UX Designer → UI Designer (sequential)
Phase 4: Build       → Architect → Frontend + Backend (parallel)
```

Agents hand off context to each other via a structured **Handoff Protocol** — summary, artifacts, key decisions, open questions — so nothing gets lost between stages.

### 24/7 Automated Routines

Five scheduled routines run daily without intervention:

| Time | What It Does |
|------|-------------|
| 06:00 | Morning Brief — priorities and blockers for the day |
| 12:00 | Signal Scan — market signals, competitor moves, trends |
| 16:00 | Experiment Check — status of running experiments |
| 22:00 | Daily Log — decisions made, lessons learned |
| Sun 20:00 | Weekly Review — full week retrospective |

Results are posted to your messenger channels and auto-saved to memory.

### One-Command Setup

```bash
cp .env.example .env && python setup.py
```

The wizard configures your owner profile, registers your products, generates all directory structures, initializes memory files, builds Docker, and starts services. Run it once, and you're operational.

---

## Prerequisites

| Item | Required |
|------|----------|
| [Claude Code Max Plan](https://claude.ai) | Required |
| Docker Desktop | Required |
| Python 3.10+ | Required |
| Messenger Bot Token | Required (one of the below) |
| GitHub PAT | Optional (auto-create repos) |

**Messenger tokens (pick one):**
| Platform | What You Need | Where to Get It |
|----------|--------------|-----------------|
| Discord | Bot Token | [Discord Developer Portal](https://discord.com/developers/applications) |
| Slack | Bot Token + App Token | [Slack API](https://api.slack.com/apps) (Socket Mode) |
| Telegram | Bot Token + Chat ID | [@BotFather](https://t.me/BotFather) on Telegram |

---

## Installation (3 Steps)

### 1. Clone
```bash
git clone <repo URL>
cd <repo directory>
```

### 2. Configure .env
```bash
cp .env.example .env
# Open .env and fill in the values
```

### 3. Run Setup
```bash
python setup.py
```

The setup wizard handles the following:
- Messenger platform selection (Discord / Slack / Telegram)
- Owner profile configuration → auto-reflects in `core/OWNER.md`
- Messenger token and bot setup with guided instructions
- Product/organization registration (multiple supported)
- Auto-generates product directories + CLAUDE.md + memory + messenger config
- Docker build and run

---

## Core Concept: Per-Product Isolation

When you register multiple products, each gets its own isolated workspace.

```
~/repos/
├── product-a/           ← Product A workspace
│   ├── CLAUDE.md        ← Auto-generated (Product A context)
│   ├── product/         ← Brief, weekly status
│   ├── memory/          ← Hypotheses, experiments, decisions, signals
│   │   └── routine-logs/ ← Routine execution logs
│   └── projects/        ← Per-project isolation
│       └── pmf-validation/
│           ├── CLAUDE.md
│           └── ...
├── product-b/           ← Product B workspace
│   └── ...
└── product-c/
    └── ...
```

Each product's AI agents can **only see that product's context**. Other product data is walled off.

---

## Usage

### Send Commands via Messenger

Send a message in the command channel (`#owner-command` on Discord/Slack, or direct message on Telegram). Keywords are analyzed to auto-route to the appropriate agent.

```
You: Draft landing page copy
Bot: [product-name (content-writer)] ...
```

60+ keywords → 23 agents auto-matched. Falls back to general mode if no keyword match.

### Create New Project
```bash
python cli/new_project.py
```
Interactive UI: select product → project type → agents → auto-generate directory.

### Check Status
```bash
python cli/status.py
```

### Run Routines Manually
```bash
python cli/run_routine.py                    # Interactive selection
python cli/run_routine.py signal-scan        # Run specific routine
python cli/run_routine.py -p my-product      # Specific product only
python cli/run_routine.py --all              # Run all routines sequentially
```

### Work Directly in a Project Directory
```bash
cd ~/repos/my-product/projects/pmf-validation
claude
# CLAUDE.md auto-loads with isolated context
```

---

## Automated Routine Schedule

| Time | Routine | Report Channel | Memory Storage |
|------|---------|----------------|----------------|
| 06:00 daily | Morning Brief | `#daily-brief` | - |
| 12:00 daily | Signal Scan | `#signals` | `signals.jsonl` |
| 16:00 daily | Experiment Check | `#experiments` | `experiments.jsonl` |
| 22:00 daily | Daily Log | `#daily-brief` | `decisions.jsonl` |
| Sun 20:00 | Weekly Review | `#weekly-review` | `decisions.jsonl` |

- JSON blocks in routine results are auto-extracted and appended to JSONL memory
- All routine logs are always saved to `memory/routine-logs/`
- Timezone can be changed via the `TZ` env variable in `docker-compose.yml`

---

## 3-Layer Context Architecture

```
Layer 0: Universal (core/)         → Shared across all sessions (owner profile, principles, style)
Layer 1: Product (~/repos/{slug}/) → Per-product isolation (brief, memory)
Layer 2: Project (projects/{id}/)  → Per-project isolation (agents, experiments)
```

---

## Structure

```
(this repo)
├── setup.py               ← Setup wizard
├── docker-compose.yml     ← Cross-platform execution
├── core/
│   ├── OWNER.md           ← Owner profile (auto-configured by setup.py)
│   ├── PRINCIPLES.md      ← Decision-making principles
│   ├── VOICE.md           ← Writing style
│   └── products.json      ← Auto-generated by setup.py
├── routines/              ← Routine prompts (editable)
├── src/
│   ├── bot.py             ← Messenger bot + agent routing
│   ├── scheduler.py       ← 24h routine execution + auto memory save
│   └── messenger/         ← Platform adapters (Discord, Slack, Telegram)
├── cli/
│   ├── new_project.py     ← Project creation
│   ├── status.py          ← Status dashboard
│   └── run_routine.py     ← Manual routine execution
├── orchestrator/          ← Project workflow orchestration
├── agents/                ← 23 specialized agents
│   ├── _teams/            ← Shared team knowledge
│   ├── strategy/          ← Strategy team (7 agents)
│   ├── growth/            ← Growth team (4 agents)
│   ├── experience/        ← Experience team (4 agents)
│   └── engineering/       ← Engineering team (8 agents)
└── templates/             ← PRD, handoff, status templates
```

---

## Team-Based Agents (23)

| Team | Agents | Role |
|------|--------|------|
| **Strategy** | PMF Planner, Feature Planner, Policy Architect, Data Analyst, Business Strategist, Idea Refiner, Scope Estimator | Strategy, planning, analysis |
| **Growth** | GTM Strategist, Content Writer, Brand Marketer, Paid Marketer | Marketing, branding |
| **Experience** | User Researcher, Desk Researcher, UX Designer, UI Designer | Research, design |
| **Engineering** | Creative Frontend, FDE, Architect, Backend Developer, API Developer, Data Collector, Data Engineer, Cloud Admin | Development, infrastructure |

---

## System Management

```bash
# Restart
docker compose restart

# View logs
docker compose logs -f

# Stop
docker compose down

# Rebuild after update
git pull && docker compose build && docker compose up -d
```

---

## Customizing Routines

Edit the `.md` files in the `routines/` folder. No rebuild required.

```bash
# Example: Edit Morning Brief prompt
vim routines/morning-brief.md
docker compose restart scheduler
```

---

## FAQ

**Q: How do I authenticate Claude Code?**
A: Subscribe to Claude Code Max plan, then log in once inside the Docker container.
`docker compose exec bot claude login`

**Q: How do I switch messenger platforms?**
A: Change `MESSENGER=slack` (or `telegram`) in `.env`, add the required tokens, and restart:
`docker compose restart`

**Q: How do I add a product later?**
A: Re-run `python setup.py`. Existing settings are preserved; only the new product is added.

**Q: How do I change the timezone for routines?**
A: Modify the `TZ` environment variable in `docker-compose.yml`.

**Q: Path separators on Windows?**
A: Use `/` forward slashes in `REPOS_BASE_PATH`. Docker handles the conversion.

**Q: What if agent routing is wrong?**
A: Edit the keyword-agent mapping in the `AGENT_ROUTES` dictionary in `src/bot.py`.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

MIT License
