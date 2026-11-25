
from tools.web_search import search_web
from agents.evidence_extractor import extract_research_findings


def test_evidence_extractor():

    topic = "Electric vehicle growth in India"

    print("\n[1] Searching the web...")

    results = search_web(topic, max_results=5)

    print(f"Retrieved: {len(results)} results")

    assert results, "Search returned no results"

    print("\n[2] Extracting findings with Groq...")

    findings = extract_research_findings(topic, results)

    print(f"Extracted: {len(findings)} findings")

    for finding in findings:
        print("\n", finding)

    assert findings, "No valid findings extracted"

    for finding in findings:
        assert finding["source"].startswith("https://")
        assert finding["category"] in [
            "opportunity",
            "challenge",
            "trend"
        ]

    print("\n[SUCCESS] Evidence extraction test passed!")


if __name__ == "__main__":
    test_evidence_extractor()
