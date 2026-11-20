from ddgs import DDGS


def search_web(query: str, max_results: int=5) -> list[dict]:
    """
    search the internet and return the normalized results 
    """

    if not query.strip():
        raise ValueError("Search query cann't be empty!!")

    results = DDGS().text(
        query,
        max_results = max_results
    )

    findings = []

    for result in results: 
        findings.append({
            "title": result.get("title", ""),
            "content": result.get("body",""),
            "source": result.get("href",""),
        })

    return findings

if __name__ == "__main__":

    query = "Electric vehicle growth in India"

    results = search_web(query)
    
    for index, result in enumerate(results, start=1):

        print(f"result: {index}")
        print(f"Title: {result["title"]}")
        print(f"Content: {result["content"]}")
        print(f"Source: {result["source"]}\n\n")