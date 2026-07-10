from newspaper import Article


class ScraperHandler:
    @staticmethod
    def extract_text(url: str) -> str:
        try:
            article = Article(url)
            article.download()
            article.parse()
            # نأخذ أول 1000 حرف فقط لعدم إغراق الذكاء الاصطناعي.
            return article.text[:1000]
        except Exception as exc:
            print(f"Scraping Error for {url}: {exc}")
            return ""
