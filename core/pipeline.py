from core.ai_handler import GeminiHandler
from core.scraper_handler import ScraperHandler
from core.search_handler import SearchHandler
from utils.text_cleaner import clean_input_text, truncate_text


class TrustBoostPipeline:
    def __init__(self):
        self.ai = GeminiHandler()
        self.search = SearchHandler()
        self.scraper = ScraperHandler()

    def process_article(self, article_text: str) -> dict:
        article_text = truncate_text(clean_input_text(article_text))

        # 1. استخراج الادعاءات.
        claims = self.ai.extract_claims(article_text)
        if not claims:
            return {
                "success": False,
                "message": "No claims found that need citations. Article looks solid!",
            }

        modified_claims = []

        # 2 و3 و4. معالجة كل ادعاء على حدة.
        for claim in claims:
            queries = self.ai.generate_search_queries(claim)
            found_fact = ""
            source_url = ""

            for query in queries:
                search_results = self.search.search(query)
                for result in search_results:
                    scraped_text = self.scraper.extract_text(result["url"])
                    if scraped_text:
                        found_fact = scraped_text
                        source_url = result["url"]
                        break
                if found_fact:
                    break

            if found_fact and source_url:
                new_claim = self.ai.inject_citation(claim, found_fact, source_url)
                if new_claim:
                    modified_claims.append(
                        {
                            "original": claim,
                            "modified": new_claim,
                            "source": source_url,
                        }
                    )

        # 5. استبدال الادعاءات في المقال الأصلي.
        final_article = article_text
        for item in modified_claims:
            if item["original"] in final_article:
                final_article = final_article.replace(
                    item["original"], item["modified"], 1
                )

        return {
            "success": True,
            "original_article": article_text,
            "final_article": final_article,
            "citations_added": len(modified_claims),
            "details": modified_claims,
        }
