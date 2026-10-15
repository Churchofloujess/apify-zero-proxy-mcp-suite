"""LangChain / RAG Document Loader wrapper for church_of_loujess Apify Actors."""
from __future__ import annotations

import os
from typing import Any
import requests

APIFY_TOKEN = os.environ.get("APIFY_TOKEN", "YOUR_APIFY_API_TOKEN")


def fetch_rag_documents(actor_slug: str, payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Run a church_of_loujess Apify Actor at 256MB and convert ragChunks into LangChain-compatible Document dicts."""
    url = f"https://api.apify.com/v2/acts/church_of_loujess~{actor_slug}/run-sync-get-dataset-items"
    resp = requests.post(
        url,
        params={"token": APIFY_TOKEN, "memory": 256},
        json=payload,
        timeout=90,
    )
    resp.raise_for_status()
    items = resp.json()

    documents: list[dict[str, Any]] = []
    for item in items:
        chunks = item.get("ragChunks") or []
        if chunks:
            for chunk in chunks:
                text = chunk.get("markdown") or chunk.get("text") or ""
                documents.append(
                    {
                        "page_content": text,
                        "metadata": {
                            "source": item.get("url") or item.get("videoUrl") or item.get("ticker") or actor_slug,
                            "title": item.get("title") or item.get("channelName") or item.get("ticker"),
                            "actor": f"church_of_loujess/{actor_slug}",
                            "chunk_index": chunk.get("chunkIndex", 0),
                        },
                    }
                )
        elif item.get("aiSummaryMarkdown") or item.get("markdown"):
            documents.append(
                {
                    "page_content": item.get("aiSummaryMarkdown") or item.get("markdown"),
                    "metadata": {
                        "source": item.get("url") or item.get("ticker") or actor_slug,
                        "actor": f"church_of_loujess/{actor_slug}",
                    },
                }
            )
    return documents


if __name__ == "__main__":
    docs = fetch_rag_documents(
        "yahoo-finance-scraper",
        {"tickers": ["NVDA"], "period": "1mo", "includeFinancials": True, "includeAiSummary": True},
    )
    print(f"Loaded {len(docs)} RAG document(s). Preview:\n{docs[0]['page_content'][:500]}")
