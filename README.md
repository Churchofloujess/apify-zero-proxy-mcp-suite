# Apify Zero-Proxy AI/RAG, Finance & B2B Lead Suite (7 MCP Tools)

[![Apify Store Profile](https://img.shields.io/badge/Apify_Store-church__of__loujess-00C853?style=for-the-badge&logo=apify)](https://apify.com/church_of_loujess)
[![MCP Ready](https://img.shields.io/badge/MCP_Server-Claude_%7C_Cursor_%7C_Windsurf-6366F1?style=for-the-badge)](./mcp/claude_desktop_config.json)
[![n8n Workflow](https://img.shields.io/badge/n8n-Ready_Workflow_Template-FF6D5A?style=for-the-badge)](./n8n/ai_market_and_lead_intelligence_workflow.json)

A production suite of **7 ultra-fast, zero-proxy Apify Actors & MCP Servers** built for **AI Agents, RAG Pipelines, Hedge Fund / Market Research, and B2B Lead Enrichment**.

Unlike legacy browser-based scrapers that require expensive residential proxies, burn `4,096 MB` of RAM per run, or break on upstream API changes, every Actor in this suite runs on **256 MB RAM** using native **HTTP/2 RPC protocols**—completing in **2–8 seconds**.

---

## Live Apify Store Actors & What Upstream Breakages They Fix

| Icon | Actor & Store Link | What It Extracts | Upstream Breakage Fixed |
| :---: | :--- | :--- | :--- |
| <img src="./assets/1_youtube_transcript_rag_icon.png" width="56" /> | **[YouTube Transcript, Chapters & AI/RAG Scraper](https://apify.com/church_of_loujess/youtube-transcript-rag-scraper)** | Full transcripts, timestamps, video metadata, chapters, `aiSummaryMarkdown` & token-bounded `ragChunks` | Uses YouTube's native **Android InnerTube RPC** (`youtubei/v1/player`) to bypass web caption blocks and cookie walls without proxies |
| <img src="./assets/2_youtube_email_leads_icon.png" width="56" /> | **[YouTube Channel Email, Socials & B2B Leads Scraper](https://apify.com/church_of_loujess/youtube-channel-email-leads-scraper)** | Verified creator/business emails, social links (Instagram/X/LinkedIn/TikTok/Discord), subscriber stats & external domain crawl | Bypasses YouTube's `aboutChannelViewModel` sign-in wall by combining InnerTube metadata with automatic external bio-link & website contact crawling |
| <img src="./assets/3_google_trends_fast_icon.png" width="56" /> | **[Google Trends Fast Scraper (No 429)](https://apify.com/church_of_loujess/google-trends-fast-scraper)** | Interest over time, regional interest by subregion/city, related rising/top queries & real-time trending searches | Replaces broken `pytrends` scrapers by performing a live session cookie pre-warm before calling Google's internal `batchexecute` & `api/explore` endpoints |
| <img src="./assets/4_google_news_fast_icon.png" width="56" /> | **[Google News Scraper Fast (Real URLs + Full Article Markdown)](https://apify.com/church_of_loujess/google-news-scraper-fast)** | Decoded publisher URLs (zero `news.google.com/rss/articles/CBMi...` links), full article text, OG images, authors & `ragChunks` | Decodes modern `AU_yqL` / `CBMi...` encrypted Google News tokens via Google's internal `Fbv4je` batchexecute RPC and extracts clean publisher Markdown |
| <img src="./assets/5_website_email_phone_finder_icon.png" width="56" /> | **[Website Email, Phone, Socials & Tech Stack Finder](https://apify.com/church_of_loujess/website-email-phone-finder)** | De-obfuscated emails (`mailto:`, `cfemail`, JSON-LD), phones, socials, live **DNS/MX mail provider verification** & 50+ tech stack signals | Async BFS crawl across `/contact`, `/about`, and `/team` pages with zero-dependency DNS/MX resolution (`Google Workspace`, `Microsoft 365`, `Cloudflare`) |
| <img src="./assets/6_fast_website_content_crawler_icon.png" width="56" /> | **[Fast Website Content & AI/RAG Markdown Crawler](https://apify.com/church_of_loujess/fast-website-content-crawler)** | Clean LLM-ready Markdown, `sitemap.xml` discovery, heading hierarchy, metadata & token-bounded `ragChunks` | Strips navigation/cookie/footer boilerplate and outputs heading-aware RAG chunks at `256 MB` RAM |
| <img src="./assets/7_yahoo_finance_scraper_icon.png" width="56" /> | **[Yahoo Finance Stock Quotes, Financials, OHLCV & AI News API](https://apify.com/church_of_loujess/yahoo-finance-scraper)** | Real-time quotes, historical OHLCV bars, full annual/quarterly **Income Statement, Balance Sheet & Cash Flow**, options chains & AI tear-sheets | Fixes Yahoo Finance's late-2024 `v10/quoteSummary` deprecation by merging `fc.yahoo.com` crumb auth with `ws/fundamentals-timeseries/v1/finance/timeseries` |

---

## 1-Click MCP Server Setup (Claude Desktop, Cursor, Windsurf)

Connect all 7 tools directly to **Claude Desktop**, **Cursor**, or **Windsurf** via Apify's official MCP server bridge (`@apify/actors-mcp-server`).

Copy [`mcp/claude_desktop_config.json`](./mcp/claude_desktop_config.json) into your `claude_desktop_config.json` or `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "loujess-ai-research-and-leads": {
      "command": "npx",
      "args": [
        "-y",
        "@apify/actors-mcp-server",
        "--actors",
        "church_of_loujess/youtube-transcript-rag-scraper,church_of_loujess/youtube-channel-email-leads-scraper,church_of_loujess/google-trends-fast-scraper,church_of_loujess/google-news-scraper-fast,church_of_loujess/website-email-phone-finder,church_of_loujess/fast-website-content-crawler,church_of_loujess/yahoo-finance-scraper"
      ],
      "env": {
        "APIFY_TOKEN": "YOUR_APIFY_API_TOKEN"
      }
    }
  }
}
```

---

## Python Quickstart (`examples/python_sdk_quickstart.py`)

```python
import requests

APIFY_TOKEN = "YOUR_APIFY_API_TOKEN"

# Example 1: Decode Google News URLs + Extract Full Article AI/RAG Markdown
resp = requests.post(
    "https://api.apify.com/v2/acts/church_of_loujess~google-news-scraper-fast/run-sync-get-dataset-items",
    params={"token": APIFY_TOKEN, "memory": 256},
    json={
        "queries": ["NVIDIA AI chips"],
        "maxItemsPerQuery": 5,
        "extractFullArticle": True,
    },
    timeout=60,
)
for article in resp.json():
    print(article["title"], "->", article["url"])  # Real publisher URL, never CBMi...

# Example 2: Yahoo Finance Real-Time Quotes, Balance Sheet, Cash Flow & AI Tear-Sheet
resp_fin = requests.post(
    "https://api.apify.com/v2/acts/church_of_loujess~yahoo-finance-scraper/run-sync-get-dataset-items",
    params={"token": APIFY_TOKEN, "memory": 256},
    json={
        "tickers": ["AAPL", "NVDA", "MSFT"],
        "period": "1mo",
        "interval": "1d",
        "includeFinancials": True,
        "includeAiSummary": True,
    },
    timeout=60,
)
for stock in resp_fin.json():
    print(stock["ticker"], stock["price_info"]["current_price"])
    print(stock["aiSummaryMarkdown"][:500])
```

---

## Importable n8n Workflow Template

Import [`n8n/ai_market_and_lead_intelligence_workflow.json`](./n8n/ai_market_and_lead_intelligence_workflow.json) directly into **n8n** to run automated B2B domain enrichment, decoded Google News monitoring, and Yahoo Finance tear-sheet generation on a schedule.

---

## License

MIT — Built by [@church_of_loujess on Apify](https://apify.com/church_of_loujess).
