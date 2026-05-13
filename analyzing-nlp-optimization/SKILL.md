# Analyzing NLP Optimization

> Part of [The Atelier](https://alejandromeyerhans.com/atelier/) by Alejandro Meyerhans
> **Standalone** · Search Intelligence

Analyzes the NLP optimization of any page using the Google Natural Language API. Extracts entity salience, content categories, and sentiment — the same signals Google's systems read.

## Quick Start

1. Download this folder into your agent's skills directory
2. Set up a Google Cloud project with the Natural Language API enabled
3. Add your API key to your `.env` file: `GOOGLE_NLP_API_KEY=AIzaSy...`
4. Tell your agent: *"Analyze the NLP optimization of https://example.com/page"*

## Prerequisites

- Google Cloud Project with **Cloud Natural Language API** enabled
- API key in `.env`: `GOOGLE_NLP_API_KEY=AIzaSy...your_key_here`
  - Create: Google Cloud Console → APIs & Services → Credentials → + CREATE CREDENTIALS → API key
- Python packages: `requests`, `beautifulsoup4`, `python-dotenv`

## Workflow

- [ ] **1. Identify the Target URL.** Confirm the URL to analyze.
- [ ] **2. Check Environment.** Install packages: `pip install requests beautifulsoup4 python-dotenv`
- [ ] **3. Run Analysis Script.** Execute `scripts/analyze_nlp.py --url "<URL>" --output "nlp_report.md"`
    - For raw text: `--text "<TEXT>"` or `--text_file "<path>"`
- [ ] **4. Review the Report.** Note Content Categories (confidence scores) and Top Entities (salience scores).
- [ ] **5. Formulate SEO Actionables.** Summarize what Google thinks the page is about and what entities to target.
- [ ] **6. Present Findings.** Output the synthesized action plan.

## Degrees of Freedom

* **Entity Extraction**: Focus on entities with **salience > 0.01**. Ignore generic entities unless core to the topic.
* **Content Cleaning**: The script extracts main article body. If extraction is poor, use your browser tool to get the text and pass via `--text_file`.

## Error Handling

- `GOOGLE_NLP_API_KEY not found` → Add key to `.env` file
- API 403 → Check key restrictions or enable Natural Language API in Cloud Console
- URL 403 Forbidden → Use browser tool to read page, save to text file, pass via `--text_file`
