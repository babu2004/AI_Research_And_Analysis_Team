
from ddgs import DDGS
from ddgs.exceptions import DDGSException
import time


def search_web(query: str, max_results: int = 5) -> list[dict]:

    if not query.strip():
        raise ValueError("Search query cannot be empty.")

    for attempt in range(1, 4):

        try:
            print(f"[WEB SEARCH] Attempt {attempt}/3")

            results = DDGS().text(
                query,
                max_results=max_results * 2
            )

            findings = []
            seen_urls = set()

            for result in results:

                title = result.get("title", "").strip()
                content = result.get("body", "").strip()
                source = result.get("href", "").strip()

                if not title or not content or not source:
                    continue

                if source in seen_urls:
                    continue

                seen_urls.add(source)

                findings.append({
                    "title": title,
                    "content": content,
                    "source": source
                })

                if len(findings) >= max_results:
                    break

            if findings:
                return findings

        except DDGSException as error:
            print(f"[WEB SEARCH WARNING] {error}")

        if attempt < 3:
            time.sleep(attempt * 2)

    raise RuntimeError("Web search failed after 3 attempts.")
