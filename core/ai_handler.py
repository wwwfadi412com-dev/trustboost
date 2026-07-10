import json
import os

import google.generativeai as genai
import streamlit as st


class GeminiHandler:
    def __init__(self):
        # نحاول جلب المفتاح من Streamlit Secrets (سحابياً) أو من متغير البيئة (محلياً).
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
        except Exception:
            api_key = os.getenv("GEMINI_API_KEY")

        if not api_key or api_key.startswith("ضع_"):
            raise ValueError(
                "Gemini API Key not found. Please set it in secrets.toml or GEMINI_API_KEY."
            )

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def _generate(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as exc:
            st.error(f"AI Generation Error: {exc}")
            return ""

    @staticmethod
    def _parse_json_array(result_text: str, fallback: list[str]) -> list[str]:
        clean_text = result_text.strip().replace("```json", "").replace("```", "")
        try:
            value = json.loads(clean_text)
            return value if isinstance(value, list) else fallback
        except json.JSONDecodeError:
            return fallback

    def extract_claims(self, article: str) -> list[str]:
        prompt = f"""
You are an E-E-A-T SEO Expert. Read the following article.
Extract all sentences that contain claims, statistics, or facts that NEED a credible external source/citation to be trusted.
Return the result STRICTLY as a JSON array of strings. If no claims need citation, return empty array [].
Article:
{article}
"""
        return self._parse_json_array(self._generate(prompt), [])

    def generate_search_queries(self, claim: str) -> list[str]:
        prompt = f"""
Based on this claim: "{claim}"
Generate 2 concise English search queries to find scientific studies, statistics, or credible news that supports this claim.
Return as a JSON array of strings.
"""
        return self._parse_json_array(self._generate(prompt), [claim])

    def inject_citation(self, original_claim: str, fact_text: str, source_url: str) -> str:
        prompt = f"""
You are a professional content editor.
Original claim in the article: "{original_claim}"
Found fact from a credible source: "{fact_text}"
Source URL: {source_url}

Rewrite the original claim by smoothly integrating the found fact into it to support it, and append a citation at the end of the sentence in this exact format: (Source: [URL]).
Do not change the core meaning of the original claim. Return ONLY the rewritten sentence.
"""
        return self._generate(prompt)
