"""Production Python quickstart calling all 7 church_of_loujess Apify Actors."""
from __future__ import annotations

import os
import requests

APIFY_TOKEN = os.environ.get("APIFY_TOKEN", "YOUR_APIFY_API_TOKEN")


def run_actor_sync(actor_slug: str, payload: dict) -> list[dict]:
    """Call an Apify Actor synchronously at 256MB RAM and return its dataset items."""
    url = f"https://api.apify.com/v2/acts/church_of_loujess~{actor_slug}/run-sync-get-dataset-items"
    resp = requests.post(
        url,
        params={"token": APIFY_TOKEN, "memory": 256},
        json=payload,
        timeout=90,
    )
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    # 1. YouTube Transcript + AI/RAG Chunks
    yt_items = run_actor_sync(
        "youtube-transcript-rag-scraper",
        {"videoUrls": ["https://www.youtube.com/watch?v=M7lc1UVf-VE"], "enableRagChunks": True},
    )
    print(f"[1] YouTube Transcript Chunks: {len(yt_items[0].get('ragChunks', []))}")

    # 2. YouTube Channel Email & Social Leads
    ch_items = run_actor_sync(
        "youtube-channel-email-leads-scraper",
        {"channelUrls": ["https://www.youtube.com/@GoogleDevelopers"], "crawlExternalDomains": True},
    )
    print(f"[2] YouTube Channel Leads: {ch_items[0].get('channelName')} -> Socials: {list(ch_items[0].get('socials', {}).keys())}")

    # 3. Google Trends Fast Scraper
    tr_items = run_actor_sync(
        "google-trends-fast-scraper",
        {"searchTerms": ["MCP server", "AI agents"], "geo": "US", "timeRange": "today 3-m"},
    )
    print(f"[3] Google Trends Series Extracted: {len(tr_items)}")

    # 4. Google News Decoded URLs + Full Article Markdown
    gn_items = run_actor_sync(
        "google-news-scraper-fast",
        {"queries": ["OpenAI"], "maxItemsPerQuery": 3, "extractFullArticle": True},
    )
    print(f"[4] Google News Decoded Articles: {len(gn_items)} (First URL: {gn_items[0].get('url')})")

    # 5. Website Email, Phone, DNS/MX & Tech Stack Finder
    wb_items = run_actor_sync(
        "website-email-phone-finder",
        {"urls": ["https://apify.com"], "maxPagesPerDomain": 3},
    )
    print(f"[5] Website Enrichment MX Provider: {wb_items[0].get('dnsMx', {}).get('provider')}")

    # 6. Fast Website Content & AI/RAG Markdown Crawler
    cr_items = run_actor_sync(
        "fast-website-content-crawler",
        {"startUrls": [{"url": "https://crawlee.dev"}], "maxPagesPerCrawl": 2},
    )
    print(f"[6] Website RAG Pages Crawled: {len(cr_items)}")

    # 7. Yahoo Finance Real-Time Stock Quotes, Financials & AI Tear-Sheet
    yf_items = run_actor_sync(
        "yahoo-finance-scraper",
        {"tickers": ["AAPL", "NVDA"], "period": "1mo", "interval": "1d", "includeFinancials": True},
    )
    print(f"[7] Yahoo Finance Tickers: {[x.get('ticker') for x in yf_items]}")
