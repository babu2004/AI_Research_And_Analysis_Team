
from ddgs import DDGS


def search_web(query: str, max_results: int = 5) -> list[dict]:
    """
    Search the web and return clean, unique results.
    """

    if not query.strip():
        raise ValueError("Search query cannot be empty.")

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

    return findings


if __name__ == "__main__":

    results = search_web(
        "Electric vehicle growth in India",
        max_results=5
    )

    for index, result in enumerate(results, start=1):
        print(f"\n--- Result {index} ---")
        print("Title:", result["title"])
        print("Content:", result["content"])
        print("Source:", result["source"])
