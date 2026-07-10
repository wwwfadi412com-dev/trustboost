# TrustBoost - E-E-A-T Citation Injector

An AI-powered SaaS tool that scans articles, identifies unverified claims, searches the web for credible statistics/studies, and injects them automatically to boost Google E-E-A-T scores.

## Built With
- Python & Streamlit
- Google Gemini 1.5 Flash
- DuckDuckGo Search & Newspaper4k

## Local setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Put your Gemini key in `.streamlit/secrets.toml`.
3. Run:
   ```bash
   streamlit run main.py
   ```
