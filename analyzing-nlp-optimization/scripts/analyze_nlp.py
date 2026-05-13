"""
Analyze NLP Optimization
========================
Calls the Google Cloud Natural Language REST API to extract entities
and classify content from a given URL or text file.

Authentication: Reads GOOGLE_NLP_API_KEY from the nearest .env file.
"""

import argparse
import json
import os
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
NLP_ENTITY_URL = "https://language.googleapis.com/v1/documents:analyzeEntities"
NLP_CLASSIFY_URL = "https://language.googleapis.com/v1/documents:classifyText"

# Credentials live in the shared config folder
_CREDENTIALS_ENV = Path(__file__).resolve().parents[3] / "config" / "credentials" / ".env"


def get_api_key():
    """Loads the API key from the credentials .env file."""
    load_dotenv(_CREDENTIALS_ENV)
    key = os.getenv("GOOGLE_NLP_API_KEY")
    if not key:
        print(f"ERROR: GOOGLE_NLP_API_KEY not found in {_CREDENTIALS_ENV}")
        print("Add this line to that file:  GOOGLE_NLP_API_KEY=your_key_here")
        sys.exit(1)
    return key


# ---------------------------------------------------------------------------
# Content fetching
# ---------------------------------------------------------------------------
def fetch_main_content(url):
    """Fetches the URL and attempts to extract the main article text."""
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/115.0.0.0 Safari/537.36"
            )
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        sys.exit(1)

    soup = BeautifulSoup(response.content, "html.parser")

    # Strip noisy elements
    for tag in soup(["script", "style", "nav", "footer", "header", "aside", "noscript"]):
        tag.extract()

    main_content = soup.find("main") or soup.find("article")
    if main_content:
        return main_content.get_text(separator=" ", strip=True)
    return soup.get_text(separator=" ", strip=True)


# ---------------------------------------------------------------------------
# Google NLP REST calls
# ---------------------------------------------------------------------------
def _call_nlp(endpoint, payload, api_key):
    """Low-level helper to POST to a Google NLP endpoint."""
    resp = requests.post(
        endpoint,
        params={"key": api_key},
        headers={"Content-Type": "application/json"},
        json=payload,
        timeout=30,
    )
    if resp.status_code != 200:
        print(f"API Error ({resp.status_code}): {resp.text}")
        sys.exit(1)
    return resp.json()


def analyze_entities(text, api_key):
    """Calls analyzeEntities and returns the list of entity dicts."""
    payload = {
        "document": {"type": "PLAIN_TEXT", "content": text},
        "encodingType": "UTF8",
    }
    data = _call_nlp(NLP_ENTITY_URL, payload, api_key)
    return data.get("entities", [])


def classify_text(text, api_key):
    """Calls classifyText and returns the list of category dicts."""
    if len(text.split()) < 20:
        return []
    payload = {"document": {"type": "PLAIN_TEXT", "content": text}}
    try:
        data = _call_nlp(NLP_CLASSIFY_URL, payload, api_key)
        return data.get("categories", [])
    except SystemExit:
        print("Warning: Classification failed (text may be too short or unsupported).")
        return []


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------
ENTITY_TYPE_MAP = {
    0: "UNKNOWN", 1: "PERSON", 2: "LOCATION", 3: "ORGANIZATION",
    4: "EVENT", 5: "WORK_OF_ART", 6: "CONSUMER_GOOD", 7: "OTHER",
    9: "PHONE_NUMBER", 10: "ADDRESS", 11: "DATE", 12: "NUMBER", 13: "PRICE",
}


def generate_report(entities, categories, output_path, source):
    """Writes a Markdown report summarising the NLP analysis."""
    # Sort all entities by salience, take the top 30 (or more if above 0.01)
    sorted_ents = sorted(entities, key=lambda x: x["salience"], reverse=True)
    
    # Always include at least the top 30, plus any with salience > 0.01
    top_n = sorted_ents[:30]
    high_salience = [e for e in sorted_ents[30:] if e.get("salience", 0) > 0.01]
    display_ents = top_n + high_salience

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# NLP Optimization Report\n\n")
        f.write(f"**Source**: {source}\n\n")

        # --- Categories ---
        f.write("## 1. Content Categories (Classification)\n\n")
        if categories:
            for cat in categories:
                f.write(f"- **{cat['name']}** (Confidence: {cat['confidence']:.2f})\n")
        else:
            f.write("No categories were identified for this text.\n")

        # --- Entities table ---
        f.write("\n## 2. Top Entities by Salience\n\n")
        f.write("| Salience | Entity Name | Type | Wikipedia |\n")
        f.write("|----------|-------------|------|-----------|\n")

        for ent in display_ents:
            etype = ENTITY_TYPE_MAP.get(ent.get("type", 0), "OTHER")
            wiki = ""
            metadata = ent.get("metadata", {})
            if "wikipedia_url" in metadata:
                wiki = f"[link]({metadata['wikipedia_url']})"
            f.write(f"| {ent['salience']:.4f} | {ent['name']} | {etype} | {wiki} |\n")

    print(f"Report saved to {output_path}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Analyze NLP optimization of a page via Google Cloud Natural Language API."
    )
    parser.add_argument("--url", help="URL of the page to analyze")
    parser.add_argument("--text", help="Raw text string to analyze")
    parser.add_argument("--text_file", help="Path to a text file to analyze")
    parser.add_argument("--output", default="nlp_report.md", help="Output report path (default: nlp_report.md)")
    args = parser.parse_args()

    # --- Resolve input ---
    source = ""
    text = ""
    if args.url:
        print(f"Fetching content from {args.url} ...")
        text = fetch_main_content(args.url)
        source = args.url
    elif args.text_file:
        print(f"Reading {args.text_file} ...")
        with open(args.text_file, "r", encoding="utf-8") as fh:
            text = fh.read()
        source = f"File: {args.text_file}"
    elif args.text:
        text = args.text
        source = "Provided raw text"
    else:
        parser.print_help()
        sys.exit(1)

    if not text.strip():
        print("Error: extracted text is empty.")
        sys.exit(1)

    # --- Authenticate ---
    api_key = get_api_key()

    # --- Analyze ---
    print(f"Sending {len(text):,} characters to Google NLP API ...")
    entities = analyze_entities(text, api_key)
    categories = classify_text(text, api_key)

    # --- Report ---
    generate_report(entities, categories, args.output, source)
    print("Done.")


if __name__ == "__main__":
    main()
