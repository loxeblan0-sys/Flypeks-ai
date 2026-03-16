# Manus Full System Inventory and Backup

This document provides a comprehensive inventory of the Manus agent's operational environment, including its file system structure, key configuration files, and the full content of its modular skills. This information is crucial for understanding the agent's architecture and for replicating its environment for development or auditing purposes.

## 1. File System Structure (`/home/ubuntu`)

Below is a tree-like representation of the `/home/ubuntu` directory, showing all files and directories up to 4 levels deep. This structure highlights the organization of the agent's workspace, including hidden configuration directories and skill modules.

```
```

## 2. Skills (`/home/ubuntu/skills/`)

This section details the modular skills that extend Manus's capabilities. Each skill is defined by a `SKILL.md` file, which includes metadata, instructions, and guidance for its use.

### `skill-creator/SKILL.md`
```markdown
---
name: skill-creator
description: Guide for creating or updating skills that extend Manus via specialized knowledge, workflows, or tool integrations. For any modification or improvement request, MUST first read this skill and follow its update workflow instead of editing files directly.
license: Complete terms in LICENSE.txt
---

# Skill Creator

This skill provides guidance for creating effective skills.

## About Skills

Skills are modular, self-contained packages that extend Manus's capabilities by providing specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for specific domains or tasks—they transform Manus from a general-purpose agent into a specialized agent equipped with procedural knowledge that no model can fully possess.

### What Skills Provide

1. Specialized workflows - Multi-step procedures for specific domains
2. Tool integrations - Instructions for working with specific file formats or APIs
3. Domain expertise - Company-specific knowledge, schemas, business logic
4. Bundled resources - Scripts, references, and assets for complex and repetitive tasks

## Core Principles

### Concise is Key

The context window is a public good. Skills share the context window with everything else Manus needs: system prompt, conversation history, other Skills' metadata, and the actual user request.

**Default assumption: Manus is already very smart.** Only add context Manus doesn't already have. Challenge each piece of information: "Does Manus really need this explanation?" and "Does this paragraph justify its token cost?"

Prefer concise examples over verbose explanations.

### Set Appropriate Degrees of Freedom

Match the level of specificity to the task's fragility and variability:

**High freedom (text-based instructions)**: Use when multiple approaches are valid, decisions depend on context, or heuristics guide the approach.

**Medium freedom (pseudocode or scripts with parameters)**: Use when a preferred pattern exists, some variation is acceptable, or configuration affects behavior.

**Low freedom (specific scripts, few parameters)**: Use when operations are fragile and error-prone, consistency is critical, or a specific sequence must be followed.

Think of Manus as exploring a path: a narrow bridge with cliffs needs specific guardrails (low freedom), while an open field allows many routes (high freedom).

### Anatomy of a Skill

Every skill consists of a required SKILL.md file and optional bundled resources:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata (required)
│   │   ├── name: (required)
│   │   └── description: (required)
│   └── Markdown instructions (required)
└── Bundled Resources (optional)
    ├── scripts/          - Executable code (Python/Bash/etc.)
    ├── references/       - Documentation intended to be loaded into context as needed
    └── templates/        - Files used in output (templates, icons, fonts, etc.)
```

#### SKILL.md (required)

Every SKILL.md consists of:

- **Frontmatter** (YAML): Contains `name` and `description` fields. These are the only fields that Manus reads to determine when the skill gets used, thus it is very important to be clear and comprehensive in describing what the skill is, and when it should be used.
- **Body** (Markdown): Instructions and guidance for using the skill. Only loaded AFTER the skill triggers (if at all).

#### Bundled Resources (optional)

- **`scripts/`** - Executable code for repetitive or deterministic tasks (e.g., `rotate_pdf.py`). Token efficient, can run without loading into context.
- **`references/`** - Documentation loaded as needed (schemas, API docs, policies). Keeps SKILL.md lean. For large files (>10k words), include grep patterns in SKILL.md.
- **`templates/`** - Output assets not loaded into context (logos, fonts, boilerplate code).

**Avoid duplication**: Information lives in SKILL.md OR references, not both.

**Do NOT include**: README.md, CHANGELOG.md, or other auxiliary documentation. Skills are for AI agents, not users.

### Progressive Disclosure

Three-level loading system:
1. **Metadata** - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<500 lines)
3. **Bundled resources** - As needed

Keep SKILL.md under 500 lines. When splitting content to references, clearly describe when to read them.

**Key principle:** Keep core workflow in SKILL.md; move variant-specific details to reference files.

Example structure for multi-domain skills:

```
bigquery-skill/
├── SKILL.md (overview + navigation)
└── references/
    ├── finance.md
    ├── sales.md
    └── product.md
```

Manus only loads the relevant reference file when needed.

## Skill Creation Process

Skill creation involves these steps:

1. Understand the skill with concrete examples
2. Plan reusable skill contents (scripts, references, templates)
3. Initialize the skill (run init_skill.py)
4. Edit the skill (implement resources and write SKILL.md)
5. Deliver the skill (send SKILL.md path via notify_user)
6. Iterate based on real usage

Follow these steps in order, skipping only if there is a clear reason why they are not applicable.

### Step 1: Understanding the Skill with Concrete Examples

Skip this step only when the skill's usage patterns are already clearly understood.

Gather concrete examples of how the skill will be used. Ask questions like:
- "What functionality should this skill support?"
- "Can you give examples of how it would be used?"

Avoid asking too many questions at once. Conclude when you have a clear sense of the functionality.

### Step 2: Planning the Reusable Skill Contents

For each example, identify reusable resources:

| Resource Type | When to Use                     | Example                               |
| ------------- | ------------------------------- | ------------------------------------- |
| `scripts/`    | Code rewritten repeatedly       | `rotate_pdf.py` for PDF rotation      |
| `templates/`  | Same boilerplate each time      | HTML/React starter for webapp builder |
| `references/` | Documentation needed repeatedly | Database schemas for BigQuery skill   |

### Step 3: Initializing the Skill

At this point, it is time to actually create the skill.

Skip this step only if the skill being developed already exists, and iteration or packaging is needed. In this case, continue to the next step.

When creating a new skill from scratch, always run the `init_skill.py` script. The script conveniently generates a new template skill directory that automatically includes everything a skill requires, making the skill creation process much more efficient and reliable.

Usage:

```bash
python /home/ubuntu/skills/skill-creator/scripts/init_skill.py <skill-name>
```

The script:

- Creates the skill directory at `/home/ubuntu/skills/<skill-name>/`
- Generates a SKILL.md template with proper frontmatter and TODO placeholders
- Creates example resource directories: `scripts/`, `references/`, and `templates/`
- Adds example files in each directory that can be customized or deleted

After initialization, customize or remove the generated SKILL.md and example files as needed.

### Step 4: Edit the Skill

When editing the (newly-generated or existing) skill, remember that the skill is being created for another instance of Manus to use. Include information that would be beneficial and non-obvious to Manus. Consider what procedural knowledge, domain-specific details, or reusable assets would help another Manus instance execute these tasks more effectively.

#### Learn Proven Design Patterns

Consult these helpful guides based on your skill's needs:

- **Multi-step processes**: See `/home/ubuntu/skills/skill-creator/references/workflows.md` for sequential workflows and conditional logic
- **Output formats or quality standards**: See `/home/ubuntu/skills/skill-creator/references/output-patterns.md` for template and example patterns
- **Progressive Disclosure Patterns**: See `/home/ubuntu/skills/skill-creator/references/progressive-disclosure-patterns.md` for splitting content across files.

These files contain established best practices for effective skill design.

#### Start with Reusable Skill Contents

Begin with the `scripts/`, `references/`, and `templates/` files identified in Step 2. This may require user input (e.g., brand assets for `templates/`, documentation for `references/`).

Test added scripts by running them to ensure they work correctly. For many similar scripts, test a representative sample.

Delete any unused example files from initialization.

#### Update SKILL.md

**Writing Guidelines:** Always use imperative/infinitive form.

##### Frontmatter

Write the YAML frontmatter with `name` and `description`:

- `name`: The skill name
- `description`: Primary trigger mechanism. Must include what the skill does AND when to use it (body only loads after triggering).
  - Example: "Document creation and editing with tracked changes. Use for: creating .docx files, modifying content, working with tracked changes."

##### Body

Write instructions for using the skill and its bundled resources.

### Step 5: Delivering the Skill

Once development of the skill is complete, validate and deliver it to the user.

#### Validate the Skill

Run the validation script to ensure the skill meets all requirements:

```bash
python /home/ubuntu/skills/skill-creator/scripts/quick_validate.py <skill-name>
```

If validation fails, fix the errors and run validation again.

#### Deliver to User

Use `message` tool to send the SKILL.md file as attachment:

```
/home/ubuntu/skills/{skill-name}/SKILL.md
```

The system will automatically:

1. Detect the path pattern `/home/ubuntu/skills/*/SKILL.md`
2. Package the skill directory into a `.skill` file
3. Send to frontend as a special card with options:
   - Add to My Skills
   - Download
   - Preview

### Step 6: Iterate

After testing the skill, users may request improvements. Often this happens right after using the skill, with fresh context of how the skill performed.

**Iteration workflow:**

1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Identify how SKILL.md or bundled resources should be updated
4. Implement changes and test again
```

### `internet-skill-finder/SKILL.md`
```markdown
---
name: internet-skill-finder
description: Search and recommend Agent Skills from verified GitHub repositories. Use when users ask to find, discover, search for, or recommend skills/plugins for specific tasks, domains, or workflows.
---

# Internet Skill Finder

Search 7 verified GitHub repositories for Agent Skills.

## Workflow

### 1. Fetch Skill List

```bash
python3 /home/ubuntu/skills/internet-skill-finder/scripts/fetch_skills.py --search "keyword"
```

Options: `--list` (all skills), `--online` (real-time fetch), `--json` (structured output)

### 2. Deep Dive (if needed)

```bash
python3 /home/ubuntu/skills/internet-skill-finder/scripts/fetch_skills.py --deep-dive REPO SKILL
```

### 3. Present Results

When using cached data, prepend:

> ℹ️ Using cached data. Enable GitHub Connector for real-time results.

Format each match:

```markdown
### [Skill Name]
**Source**: [Repository] | ⭐ [Stars]
**Description**: [From SKILL.md]
👉 **[Import](import_url)**
```

### 4. No Matches

Suggest `/skill-creator` for custom skill creation.

## Data Access

Script auto-detects and uses best method:

| Priority | Method | Rate Limit | Behavior |
|----------|--------|------------|----------|
| 1 | GitHub Connector | 15000/hr | Auto real-time |
| 2 | Offline cache | Unlimited | Fallback |
| 3 | `GITHUB_TOKEN` env | 5000/hr | With `--online` |

JSON output includes `"using_cache": true/false` to indicate data source.

When cache is used, inform user: Enable GitHub Connector for real-time results.

## Sources

7 repositories: anthropics/skills, obra/superpowers, vercel-labs/agent-skills, K-Dense-AI/claude-scientific-skills, ComposioHQ/awesome-claude-skills, travisvn/awesome-claude-skills, BehiSecc/awesome-claude-skills
```

### `github-gem-seeker/SKILL.md`
```markdown
---
name: github-gem-seeker
description: >
  Search GitHub for battle-tested solutions instead of reinventing the wheel. Use when
  the user's problem is universal enough that open source developers have probably
  solved it already—especially for: format conversion (video/audio/image/document),
  media downloading, file manipulation, web scraping/archiving, automation scripts,
  and CLI tools. Prefer this skill over writing custom code for well-trodden problems.
---

# GitHub Gem Seeker

Find and use battle-tested open source projects on GitHub to solve the user's problem immediately. After successfully solving the problem, offer to package the solution into a reusable skill.

## Core Philosophy

Classic open source projects, tested by countless users over many years, are far more reliable than code written from scratch. **Solve the problem first, skill-ify later.**

## Workflow

### Step 1: Understand the Need

Clarify what the user wants to accomplish. Ask only if truly ambiguous:
- What specific problem are you trying to solve?
- What format/input/output do you expect?

### Step 2: Find the Right Tool

Search for GitHub projects using effective query patterns:

| Need Type | Query Pattern | Example |
|-----------|---------------|---------|
| Tool/utility | `github [task] tool` | `github video download tool` |
| Library | `github [language] [function] library` | `github python pdf library` |
| Alternative | `github [known-tool] alternative` | `github ffmpeg alternative` |

### Step 3: Evaluate Quality (Quick Check)

Assess candidates using key indicators:

| Indicator | Gem Signal | Warning Signal |
|-----------|------------|----------------|
| Stars | 1k+ solid, 10k+ excellent, 50k+ legendary | <100 for mature projects |
| Last commit | Within 6 months | >2 years ago |
| Documentation | Clear README, examples | Sparse or outdated docs |

### Step 4: Solve the Problem

**This is the priority.** Install the tool and use it to solve the user's actual problem:

1. Install the chosen tool (pip, npm, apt, or direct download)
2. Run it with the user's input/files
3. Deliver the result to the user
4. Troubleshoot if needed—iterate until solved

### Step 5: Credit the Gem & Offer Next Steps (Post-Success Only)

**Only after the problem is successfully solved:**

1. **Credit the open source project** — Always share the GitHub repo URL and encourage support:

   > "This was powered by **[Project Name]** — an amazing open source project!
   > GitHub: [URL]
   > If it helped you, consider giving it a ⭐ star to support the maintainers."

2. **Offer to skill-ify** — Optionally mention:

   > "If you'll need this again, I can package it into a reusable skill for instant use next time."

Do NOT skip crediting the project. Open source thrives on recognition.

## Quality Tiers

| Tier | Criteria | Examples |
|------|----------|----------|
| **Legendary** | 50k+ stars, industry standard | FFmpeg, ImageMagick, yt-dlp |
| **Excellent** | 10k+ stars, strong community | Pake, ArchiveBox |
| **Solid** | 1k+ stars, well-documented | Most maintained tools |
| **Promising** | <1k stars, active development | Newer niche projects |

Prefer higher tiers for reliability.

## Example Interaction

**User:** I need to download this YouTube video: [link]

**Correct approach:**
1. Identify yt-dlp as the legendary-tier solution
2. Install yt-dlp
3. Download the video for the user
4. Deliver the downloaded file
5. *After success:* "This was powered by **yt-dlp** — https://github.com/yt-dlp/yt-dlp — give it a ⭐ if it helped! If you download videos often, I can turn this into a skill for instant use next time."

**Wrong approach:**
- ❌ "I found yt-dlp, want me to make a skill for it?"
- ❌ Presenting options without solving the problem

## Common Gems Reference

| Category | Go-to Gems |
|----------|------------|
| Video/Audio processing | FFmpeg, yt-dlp |
| Image processing | ImageMagick, sharp |
| PDF manipulation | pdf-lib, PyMuPDF |
| Web scraping | Playwright, Puppeteer, Scrapy |
| Format conversion | Pandoc, FFmpeg |
| Archiving | ArchiveBox |
| Desktop app packaging | Electron, Tauri, Pake |
```

### `stock-analysis/SKILL.md`
```markdown
---
name: stock-analysis
description: "Analyze stocks and companies using financial market data. Get company profiles, technical insights, price charts, insider holdings, and SEC filings for comprehensive stock research."
---

# Stock Analysis

Comprehensive stock and company analysis using with real-time market data.

## Core Capabilities

- **Company Research**: Get company profiles, business info, executive teams
- **Technical Analysis**: Access price charts, technical indicators, outlooks
- **Fundamental Analysis**: Review insights, valuations, analyst ratings
- **Insider Activity**: Track insider holdings and transactions
- **Regulatory Filings**: Access SEC filing history and documents
- **Multi-Stock Comparison**: Compare multiple stocks with chart data

## Available APIs

### Company Information
- `Yahoo/get_stock_profile` - Company profile (business, industry, executives, contact)
- `Yahoo/get_stock_insights` - Technical indicators, valuation, ratings, research reports

### Trading & Market Data
- `Yahoo/get_stock_chart` - Historical price data with customizable timeframes

### Ownership & Compliance
- `Yahoo/get_stock_holders` - Insider holdings and transactions
- `Yahoo/get_stock_sec_filing` - SEC filing history (10-K, 10-Q, 8-K, etc.)

## Common Workflows

### 1. Company Overview → Deep Dive
```
User: "Tell me about AAPL"
→ Yahoo/get_stock_profile (business summary, industry, employees)
→ Yahoo/get_stock_insights (technical outlook, valuation, ratings)
→ Yahoo/get_stock_chart (recent price performance)
```

### 2. Technical Analysis → Fundamental Check
```
User: "Is TSLA a good buy?"
→ Yahoo/get_stock_chart (price trends, support/resistance)
→ Yahoo/get_stock_insights (technical outlook, target price, rating)
→ Yahoo/get_stock_profile (verify business fundamentals)
```

### 3. Insider Activity Analysis
```
User: "Show me insider trading for NVDA"
→ Yahoo/get_stock_holders (insider transactions)
→ Yahoo/get_stock_profile (context about executives)
→ Yahoo/get_stock_insights (check if aligned with outlook)
```

### 4. Due Diligence Package
```
User: "Full analysis of MSFT"
→ Yahoo/get_stock_profile (company background)
→ Yahoo/get_stock_insights (analyst ratings, valuation)
→ Yahoo/get_stock_chart (historical performance)
→ Yahoo/get_stock_holders (insider sentiment)
→ Yahoo/get_stock_sec_filing (recent regulatory filings)
```

### 5. Multi-Stock Comparison
```
User: "Compare AAPL vs MSFT vs GOOGL"
→ Yahoo/get_stock_chart (with comparisons parameter)
→ Yahoo/get_stock_insights (for each symbol)
→ Compare metrics side-by-side
```

### 6. Sector Research
```
User: "Analyze tech stocks: AAPL, NVDA, AMD"
→ Yahoo/get_stock_profile (each company's focus area)
→ Yahoo/get_stock_insights (sector comparison scores)
→ Yahoo/get_stock_chart (relative performance)
```

## Key Parameters

### Common Parameters
- `symbol`: Stock ticker symbol (e.g., "AAPL", "TSLA")
- `region`: Market region (US, GB, JP, etc.) - default: US
- `lang`: Response language (en-US, zh-Hant-HK, etc.) - default: en-US

### Chart-Specific
- `interval`: 1m, 5m, 15m, 30m, 1h, 1d, 1wk, 1mo
- `range`: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
- `comparisons`: Compare with other symbols (e.g., "^GSPC,MSFT")
- `events`: Include dividends, splits, earnings (div, split, earn)

## Key Data Points

### Profile Data
- Business summary and industry classification
- Employee count and executive team
- Contact information and website
- Sector and industry metrics

### Insights Data
- **Technical outlook**: Short/intermediate/long-term signals
- **Valuation**: Relative value vs sector/market
- **Key technicals**: Support, resistance, stop-loss levels
- **Ratings**: Analyst recommendations and target prices
- **Company metrics**: Innovation, hiring, sustainability scores
- **Research reports**: Analyst reports and summaries
- **Significant events**: Recent developments

### Chart Data
- OHLC (Open, High, Low, Close) prices
- Volume data
- Adjusted close prices
- 52-week high/low
- Current trading period info

### Holder Data
- Insider names and positions
- Transaction dates and descriptions
- Holdings quantity and value
- Relationship to company

### Filing Data
- Filing type (10-K, 10-Q, 8-K, etc.)
- Filing date and title
- EDGAR URLs for full documents
- Exhibits and related documents

## When to Use This Skill

**ALWAYS invoke APIs when users mention:**
- **Stock symbols**: "AAPL", "TSLA", "$MSFT", "stock price", "stock info"
- **Analysis requests**: "analyze", "research", "look into", "tell me about [STOCK]"
- **Comparison**: "compare", "vs", "versus", "which is better"
- **Price queries**: "price", "chart", "performance", "trend", "up or down"
- **Insider activity**: "insider", "holdings", "who owns", "buying/selling"
- **Filings**: "SEC filing", "10-K", "10-Q", "earnings report", "financial statements"
- **Company info**: "what does [company] do", "who runs", "about [company]"

**Required API combinations:**
- General stock questions → MUST call `Yahoo/get_stock_profile` + `Yahoo/get_stock_insights`
- Price/chart mentions → MUST include `Yahoo/get_stock_chart`
- Investment decisions → MUST call all three: chart + insights + profile
- Multiple stocks → MUST use comparison parameters in chart API
- Insider questions → MUST call `Yahoo/get_stock_holders` + profile for context

## Best Practices

1. **Start broad, then drill down** - Profile first, then specific data
2. **Context matters** - Combine profile with technical data for better insights
3. **Use comparisons** - Chart API supports multi-symbol comparison
4. **Regional stocks** - Set region/lang for non-US markets
5. **Time relevance** - Adjust chart range based on user's timeframe
6. **Insider context** - Combine holder data with profile for complete picture

## API Reference

Full parameter specs and response schemas:
- [yahoo-api.md](references/yahoo-api.md)
```

### `similarweb-analytics/SKILL.md`
```markdown
---
name: similarweb-analytics
description: "Analyze websites and domains using SimilarWeb traffic data. Get traffic metrics, engagement stats, global rankings, traffic sources, and geographic distribution for comprehensive website research."
---

# SimilarWeb Analytics

Comprehensive website and domain analysis using SimilarWeb traffic data.

## Core Capabilities

- **Traffic Analysis**: Total visits, unique visitors, traffic trends
- **Engagement Metrics**: Bounce rate, pages per visit, average visit duration
- **Global Ranking**: Website ranking over time
- **Traffic Sources**: Marketing channels (desktop and mobile)
- **Geographic Distribution**: Traffic breakdown by country

## API Usage

All APIs use `ApiClient` from `/opt/.manus/.sandbox-runtime`. Common parameters:
- `domain`: Website domain (e.g., "google.com")
- `start_date`: Start date (YYYY-MM). Max 12 months ago
- `end_date`: End date (YYYY-MM). Max 12 months ago, default is 1 month ago (most recent complete month)
- `main_domain_only`: Exclude subdomains if True (default: False)

**Default time ranges vary by API:**
- Global Rank, Visits Total, Unique Visit, Bounce Rate: default **6 months**
- Traffic Sources (Desktop/Mobile), Traffic by Country: default **3 months**

### Get Global Rank

```python
import sys
sys.path.append("/opt/.manus/.sandbox-runtime")
from data_api import ApiClient

client = ApiClient()
result = client.call_api("SimilarWeb/get_global_rank", path_params={"domain": "amazon.com"})
```

### Get Website Visits Total

```python
import sys
sys.path.append("/opt/.manus/.sandbox-runtime")
from data_api import ApiClient

client = ApiClient()
result = client.call_api("SimilarWeb/get_visits_total",
    path_params={"domain": "amazon.com"},
    query={"country": "world", "granularity": "monthly", "start_date": "2025-07", "end_date": "2025-12"})
```

### Get Unique Visit

```python
import sys
sys.path.append("/opt/.manus/.sandbox-runtime")
from data_api import ApiClient

client = ApiClient()
result = client.call_api("SimilarWeb/get_unique_visit",
    path_params={"domain": "amazon.com"},
    query={"start_date": "2025-07", "end_date": "2025-12"})
```

### Get Bounce Rate

```python
import sys
sys.path.append("/opt/.manus/.sandbox-runtime")
from data_api import ApiClient

client = ApiClient()
result = client.call_api("SimilarWeb/get_bounce_rate",
    path_params={"domain": "amazon.com"},
    query={"country": "world", "granularity": "monthly", "start_date": "2025-07", "end_date": "2025-12"})
```

### Get Traffic Sources - Desktop

Returns breakdown by channel: Organic Search, Paid Search, Direct, Display Ads, Email, Referrals, Social Media.

```python
import sys
sys.path.append("/opt/.manus/.sandbox-runtime")
from data_api import ApiClient

client = ApiClient()
result = client.call_api("SimilarWeb/get_traffic_sources_desktop",
    path_params={"domain": "amazon.com"},
    query={"country": "world", "granularity": "monthly", "start_date": "2025-07", "end_date": "2025-12"})
```

### Get Traffic Sources - Mobile

```python
import sys
sys.path.append("/opt/.manus/.sandbox-runtime")
from data_api import ApiClient

client = ApiClient()
result = client.call_api("SimilarWeb/get_traffic_sources_mobile",
    path_params={"domain": "amazon.com"},
    query={"country": "world", "granularity": "monthly", "start_date": "2025-07", "end_date": "2025-12"})
```

### Get Total Traffic by Country

Returns traffic share, visits, pages per visit, average time, bounce rate and rank by country.

- `limit`: Number of countries to return (default: 1, max: 10)
- **Date range limit**: max 3 months (unlike other APIs)

```python
import sys
sys.path.append("/opt/.manus/.sandbox-runtime")
from data_api import ApiClient

client = ApiClient()
result = client.call_api("SimilarWeb/get_total_traffic_by_country",
    path_params={"domain": "amazon.com"},
    query={"start_date": "2025-10", "end_date": "2025-12", "limit": "10"})
```

## When to Use

Invoke APIs when users mention:
- Domain names: "google.com", "amazon.com"
- Traffic queries: "traffic", "visits", "visitors"
- Ranking queries: "rank", "ranking", "how popular"
- Engagement queries: "bounce rate", "engagement"
- Source queries: "traffic sources", "marketing channels"
- Geographic queries: "countries", "geographic"
- Comparison queries: "compare", "vs"

## Data Limitations

- Historical data: max 12 months
- Geography: worldwide only
- Granularity: monthly only
- Latest data: last complete month

## Important: Save Data to Files

API calls may fail mid-execution due to credit depletion. **Always save all retrieved data to files immediately** to avoid data loss and prevent redundant API calls.
```

### `telegram-bot-expert/SKILL.md`
```markdown
---
name: telegram-bot-expert
description: Expert guide for developing any type of Telegram bot with professional architecture. Use for creating e-commerce bots, service platforms, delivery systems, support bots, games, analytics tools, and any other Telegram bot application with scalability, databases, APIs, and advanced features.
license: MIT
---

# Telegram Bot Expert - Universal Bot Development

A comprehensive skill for building production-grade Telegram bots of any type: e-commerce stores, delivery services, support systems, games, analytics platforms, and more. Includes architecture patterns, database design, API integrations, and deployment strategies.

## When to Use This Skill

Use this skill when building:
- **E-commerce Bots**: Online stores with product catalogs, shopping carts, payments
- **Service Platforms**: Booking systems, delivery apps, taxi services, freelance marketplaces
- **Support Systems**: Customer service bots, ticketing systems, FAQ automation
- **Games & Entertainment**: Interactive games, quizzes, contests, entertainment bots
- **Analytics & Monitoring**: Data dashboards, notifications, reporting systems
- **Content Distribution**: News bots, media sharing, subscription services
- **Admin Tools**: Management dashboards, moderation bots, data management
- **Any complex bot** requiring databases, external APIs, async processing, or scalability

## Universal Bot Architecture

### Core Technology Stack

**Recommended for Production:**
- **Language**: Python 3.9+
- **Bot Framework**: `aiogram` 3.x (async-first, modern, recommended) or `pyrogram`
- **Database**: PostgreSQL (primary) + Redis (caching/sessions)
- **Task Queue**: Celery or RQ for background jobs
- **API Server**: FastAPI for webhooks and external integrations
- **Deployment**: Docker + Kubernetes or serverless (AWS Lambda, Google Cloud)

### Universal Project Structure

```
telegram-bot/
├── bot/
│   ├── __init__.py
│   ├── main.py                 # Bot entry point
│   ├── config.py               # Configuration, env variables
│   ├── handlers/               # Message handlers by feature
│   │   ├── __init__.py
│   │   ├── start_handler.py    # /start command
│   │   ├── user_handlers.py    # User-related actions
│   │   ├── product_handlers.py # E-commerce specific
│   │   ├── order_handlers.py   # Order management
│   │   ├── payment_handlers.py # Payment processing
│   │   ├── admin_handlers.py   # Admin commands
│   │   └── error_handlers.py   # Error handling
│   ├── middlewares/            # Cross-cutting concerns
│   │   ├── __init__.py
│   │   ├── auth_middleware.py
│   │   ├── logging_middleware.py
│   │   └── rate_limit_middleware.py
│   ├── services/               # Business logic layer
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   ├── product_service.py
│   │   ├── order_service.py
│   │   ├── payment_service.py
│   │   ├── notification_service.py
│   │   └── ai_service.py
│   ├── models/                 # Database ORM models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── order.py
│   │   ├── transaction.py
│   │   └── session.py
│   ├── keyboards/              # UI - inline & reply keyboards
│   │   ├── __init__.py
│   │   ├── main_keyboard.py
│   │   ├── product_keyboard.py
│   │   ├── payment_keyboard.py
│   │   └── admin_keyboard.py
│   ├── utils/                  # Utility functions
│   │   ├── __init__.py
│   │   ├── validators.py
│   │   ├── formatters.py
│   │   ├── decorators.py
│   │   └── constants.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── db.py               # Database connection management
│   └── filters/                # Custom message filters
│       ├── __init__.py
│       ├── is_admin.py
│       └── is_user.py
├── tasks/                      # Async background tasks
│   ├── __init__.py
│   ├── email_tasks.py
│   ├── notification_tasks.py
│   ├── order_processing_tasks.py
│   └── cleanup_tasks.py
├── api/                        # FastAPI server for webhooks
│   ├── __init__.py
│   ├── main.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── webhooks.py         # Telegram webhook
│   │   ├── payments.py         # Payment provider webhooks
│   │   └── admin.py            # Admin API
│   └── schemas.py              # Request/response schemas
├── tests/
│   ├── __init__.py
│   ├── test_handlers.py
│   ├── test_services.py
│   ├── test_models.py
│   └── conftest.py
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── .dockerignore
├── requirements.txt
├── .env.example
├── pytest.ini
└── README.md
```

## Bot Type Examples & Patterns

### 1. E-Commerce Bot (Online Store)

**Key Features**: Product catalog, search, shopping cart, checkout, payments, order tracking

**Database Schema**:
```python
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    category = Column(String, index=True)
    image_url = Column(String)
    stock = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.telegram_id"))
    total_amount = Column(Float)
    status = Column(String, default="pending")  # pending, paid, shipped, delivered
    items = relationship("OrderItem")
    created_at = Column(DateTime, default=datetime.utcnow)
```

**Handler Example**:
```python
@router.callback_query(F.data.startswith("buy_"))
async def buy_product(query: CallbackQuery, state: FSMContext):
    product_id = int(query.data.split("_")[1])
    product = await product_service.get_product(product_id)
    
    # Add to cart
    cart = await state.get_data()
    cart.setdefault("items", []).append({"id": product_id, "qty": 1})
    await state.update_data(cart=cart)
    
    await query.answer("✅ Added to cart")
```

### 2. Delivery/Service Bot

**Key Features**: Order placement, real-time tracking, driver assignment, ratings, payment

**Database Schema**:
```python
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.telegram_id"))
    driver_id = Column(BigInteger, ForeignKey("drivers.telegram_id"), nullable=True)
    pickup_location = Column(String)
    delivery_location = Column(String)
    status = Column(String)  # pending, assigned, picked_up, in_transit, delivered
    estimated_time = Column(Integer)  # minutes
    created_at = Column(DateTime, default=datetime.utcnow)

class Driver(Base):
    __tablename__ = "drivers"
    telegram_id = Column(BigInteger, primary_key=True)
    name = Column(String)
    phone = Column(String)
    vehicle = Column(String)
    rating = Column(Float, default=5.0)
    is_active = Column(Boolean, default=True)
```

**Real-time Tracking**:
```python
async def send_order_updates(order_id: int):
    order = await order_service.get_order(order_id)
    user = await user_service.get_user(order.user_id)
    
    message = f"""
    📦 Order #{order_id}
    Status: {order.status}
    Driver: {order.driver.name}
    ETA: {order.estimated_time} min
    """
    
    await bot.send_message(user.telegram_id, message)
```

### 3. Support/Help Bot

**Key Features**: Ticket system, FAQ, escalation, agent assignment, analytics

**Database Schema**:
```python
class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.telegram_id"))
    agent_id = Column(BigInteger, nullable=True)
    subject = Column(String)
    description = Column(Text)
    status = Column(String)  # open, in_progress, resolved, closed
    priority = Column(String)  # low, medium, high, urgent
    messages = relationship("TicketMessage")
    created_at = Column(DateTime, default=datetime.utcnow)

class TicketMessage(Base):
    __tablename__ = "ticket_messages"
    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"))
    sender_id = Column(BigInteger)  # user or agent
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
```

**FSM for Ticket Creation**:
```python
class CreateTicket(StatesGroup):
    waiting_for_subject = State()
    waiting_for_description = State()
    confirmation = State()

@router.message(CreateTicket.waiting_for_subject)
async def process_subject(message: Message, state: FSMContext):
    await state.update_data(subject=message.text)
    await state.set_state(CreateTicket.waiting_for_description)
    await message.answer("📝 Describe your issue:")
```

### 4. Game/Entertainment Bot

**Key Features**: Leaderboards, achievements, multiplayer, rewards, statistics

**Database Schema**:
```python
class GameSession(Base):
    __tablename__ = "game_sessions"
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.telegram_id"))
    game_type = Column(String)  # quiz, puzzle, card_game, etc.
    score = Column(Integer, default=0)
    status = Column(String)  # in_progress, completed, abandoned
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

class Leaderboard(Base):
    __tablename__ = "leaderboard"
    rank = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.telegram_id"))
    total_score = Column(Integer)
    games_played = Column(Integer)
    updated_at = Column(DateTime, default=datetime.utcnow)
```

**Game Logic**:
```python
async def play_quiz(user_id: int, question_id: int, answer: str):
    question = await quiz_service.get_question(question_id)
    is_correct = answer == question.correct_answer
    
    if is_correct:
        points = 10
        await user_service.add_points(user_id, points)
        await leaderboard_service.update_rank(user_id)
    
    return {"correct": is_correct, "points": points if is_correct else 0}
```

### 5. Analytics/Dashboard Bot

**Key Features**: Real-time metrics, charts, reports, notifications, data export

**Data Aggregation**:
```python
class DailyMetric(Base):
    __tablename__ = "daily_metrics"
    id = Column(Integer, primary_key=True)
    date = Column(Date, index=True)
    metric_name = Column(String, index=True)
    value = Column(Float)
    
    __table_args__ = (
        UniqueConstraint("date", "metric_name", name="uq_daily_metric"),
    )

class UserActivity(Base):
    __tablename__ = "user_activity"
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, index=True)
    event_type = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
```

**Chart Generation**:
```python
import matplotlib.pyplot as plt

async def generate_daily_users_chart():
    metrics = await analytics_service.get_daily_metric("active_users", last_n_days=30)
    dates = [m.date for m in metrics]
    values = [m.value for m in metrics]
    
    plt.figure(figsize=(10, 6))
    plt.plot(dates, values, marker=".")
    plt.title("Daily Active Users")
    plt.xlabel("Date")
    plt.ylabel("Users")
    plt.grid(True)
    plt.tight_layout()
    
    chart_path = "/tmp/daily_users.png"
    plt.savefig(chart_path)
    plt.close()
    return chart_path
```

## Advanced Concepts

### FSM (Finite State Machine) for Complex Flows

Use `aiogram.fsm.context.FSMContext` and `aiogram.fsm.state.State`, `StatesGroup` for managing multi-step user interactions (e.g., order placement, registration, support ticket creation).

### Middlewares for Cross-Cutting Concerns

Implement middlewares for authentication, logging, rate limiting, and database session management. This keeps handlers clean and focused on business logic.

### Background Tasks with Celery/RQ

Offload long-running operations (e.g., sending mass notifications, complex data processing, API calls with delays) to a background task queue to keep the bot responsive.

### Webhooks vs. Long Polling

- **Webhooks (recommended for production)**: Telegram sends updates directly to your server. Requires a public URL and SSL certificate. More efficient and scalable.
- **Long Polling**: Your bot periodically requests updates from Telegram. Simpler to set up, but less efficient and can be slower.

### Database Indexing

Crucial for performance. Add indexes to columns frequently used in `WHERE` clauses, `JOIN` conditions, and `ORDER BY` clauses.

```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, index=True)
    created_at = Column(DateTime, index=True)
    is_active = Column(Boolean, index=True)
    
    __table_args__ = (
        Index("idx_user_created_active", "created_at", "is_active"),
    )
```

### Caching Strategy

Use Redis for caching frequently accessed data (e.g., user profiles, product lists) to reduce database load and improve response times.

```python
import redis.asyncio as redis

redis_client = await redis.from_url("redis://localhost")

async def get_user_cached(user_id: int):
    # Try cache first
    cached = await redis_client.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)
    
    # Query database
    user = await db.get_user(user_id)
    
    # Cache for 1 hour
    await redis_client.setex(
        f"user:{user_id}",
        3600,
        json.dumps(user)
    )
    
    return user
```

## Deployment Strategies

### Docker Containerization

```dockerfile
FROM python:3.11-slim
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY . .

# Run bot
CMD ["python", "-m", "bot.main"]
```

### Docker Compose (Full Stack)

```yaml
version: '3.8'

services:
  bot:
    build: .
    environment:
      BOT_TOKEN: ${BOT_TOKEN}
      DATABASE_URL: postgresql+asyncpg://user:password@postgres:5432/botdb
      REDIS_URL: redis://redis:6379
    depends_on:
      - postgres
      - redis
    restart: always

  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: botdb
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

  celery:
    build: .
    command: celery -A tasks worker --loglevel=info
    environment:
      BOT_TOKEN: ${BOT_TOKEN}
      DATABASE_URL: postgresql+asyncpg://user:password@postgres:5432/botdb
      REDIS_URL: redis://redis:6379
    depends_on:
      - postgres
      - redis

volumes:
  postgres_data:
  redis_data:
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: telegram-bot
spec:
  replicas: 3
  selector:
    matchLabels:
      app: telegram-bot
  template:
    metadata:
      labels:
        app: telegram-bot
    spec:
      containers:
      - name: bot
        image: telegram-bot:latest
        env:
        - name: BOT_TOKEN
          valueFrom:
            secretKeyRef:
              name: bot-secrets
              key: token
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: bot-secrets
              key: database-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

## Performance Optimization Checklist

- ✅ Use connection pooling for database and Redis
- ✅ Implement multi-level caching (Redis, in-memory)
- ✅ Add database indexes on frequently queried columns
- ✅ Use async/await throughout the codebase
- ✅ Batch database operations when possible
- ✅ Implement rate limiting and throttling
- ✅ Use webhooks instead of polling for updates
- ✅ Monitor and log performance metrics
- ✅ Optimize database queries (use EXPLAIN ANALYZE)
- ✅ Implement pagination for large result sets

## Security Best Practices

1. **Secrets Management**: Use environment variables, never hardcode secrets
2. **Input Validation**: Validate all user inputs to prevent injection attacks
3. **Rate Limiting**: Prevent brute force and DoS attacks
4. **HTTPS/TLS**: Use HTTPS for all external communications
5. **Database Encryption**: Encrypt sensitive data at rest
6. **API Authentication**: Use API keys and OAuth2 for external services
7. **Audit Logging**: Log all sensitive operations
8. **SQL Injection Prevention**: Use parameterized queries (SQLAlchemy handles this)
9. **XSS Prevention**: Sanitize user-generated content
10. **Access Control**: Implement role-based access control (admin, user, etc.)

## Testing Strategy

### Unit Tests

```python
import pytest
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_create_order():
    order_service = OrderService()
    order = await order_service.create_order(
        user_id=123,
        items=[{"product_id": 1, "qty": 2}],
        total=99.99
    )
    assert order.user_id == 123
    assert order.total_amount == 99.99
```

### Integration Tests

```python
@pytest.mark.asyncio
async def test_payment_flow():
    async with async_session() as session:
        user = await create_test_user(session)
        order = await create_test_order(session, user.id)
        payment = await payment_service.create_invoice(order.id, order.total_amount)
        assert payment.status == "pending"
```

## Resources

Bundled reference files:
- `references/aiogram_patterns.md` - Advanced aiogram patterns and examples
- `references/database_schemas.md` - Complete database design patterns
- `references/api_integrations.md` - External API integration examples
- `references/deployment_guide.md` - Step-by-step deployment instructions

## Quick Start

1. Copy `templates/bot_starter.py` as your bot's main entry point
2. Set up PostgreSQL and Redis
3. Create `.env` file with your BOT_TOKEN and database URL
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `alembic upgrade head`
6. Start bot: `python -m bot.main`

## Common Questions

**Q: How do I handle payments?**
A: Integrate with Telegram Payments API or external providers (Stripe, PayPal). Use webhooks to confirm payments and update order status.

**Q: How do I scale to millions of users?**
A: Use webhooks instead of polling, implement caching, use database replication, deploy multiple bot instances with load balancing.

**Q: How do I add AI/ML features?**
A: Use libraries like `transformers` for NLP, `scikit-learn` for ML models, integrate with OpenAI API for advanced AI.

**Q: How do I handle real-time updates?**
A: Use webhooks for external events, implement polling for specific features, use Redis Pub/Sub for internal messaging.

**Q: How do I monitor bot health?**
A: Implement comprehensive logging, use monitoring tools (Prometheus, Grafana), set up alerting for errors.
```

## 3. Configuration Files

This section contains the content of various configuration files found in the agent's environment. These files control the behavior of different components, from the code server to state synchronization.

### `/home/ubuntu/.env`
```
export APP_ENV=PROD
export RUNTIME_API_HOST=https://api.manus.im
export PW_TEST_SCREENSHOT_NO_FONTS_READY=1
export TZ=America/New_York
export DEPLOY_WASMER_OWNER=manus
export OTEL_PYTHON_LOG_CORRELATION=true
export OTEL_BSP_MAX_EXPORT_BATCH_SIZE=1024
export OTEL_BSP_SCHEDULE_DELAY=10000
export OTEL_SERVICE_NAME=sandbox-runtime
export OTEL_RESOURCE_ATTRIBUTES=service.name=sandbox-runtime,service.env=prod
export OTEL_TRACES_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_ENDPOINT=https://http.butterflyotel.online
export OTEL_TRACE_CUSTOM_SAMPLER_EXCLUDED_URLS=/healthz
export OTEL_TRACES_SAMPLER_RATIO=1.0
export SENTRY_DSN=https://962d173a894df4e4c23c744f8c39d6f3@sentry.butterflyotel.online/9
export CODE_SERVER_DOMAIN="us2.manus.computer"
export APP_DOMAIN=manus.im,manus.ai
export LAST_COMMIT_HASH=7.0.23
export NEKO_ADMIN_PASSWORD="2eda90ded72a60be"
export NEKO_USER_PASSWORD="c39cb13459f261fd"
export NEKO_USERNAME="neko"
export CODE_SERVER_PORT="8329"
export CODE_SERVER_PASSWORD="2a74364c5ce010a5"
```

### `/home/ubuntu/.config/code-server/config.yaml`
```yaml
auth: password
cert: false
bind-addr: 0.0.0.0:8329
password: 2a74364c5ce010a5
```

### `/home/ubuntu/.config/state-sync/state-sync-config.yaml`
```yaml
browser-port: '9222'
pull: true
push: true
```
