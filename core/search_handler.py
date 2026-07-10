from duckduckgo_search import DDGS


class SearchHandler:
    def __init__(self):
        self.ddgs = DDGS()

    def search(self, query: str, max_results: int = 3) -> list[dict]:
        try:
            results = self.ddgs.text(query, region="wt-wt", max_results=max_results)
            return [
                {
                    "title": result.get("title", ""),
                    "url": result.get("href", ""),
                    "snippet": result.get("body", ""),
                }
                for result in results
                if result.get("href")
            ]
        except Exception as exc:
            print(f"Search Error: {exc}")
            return []
