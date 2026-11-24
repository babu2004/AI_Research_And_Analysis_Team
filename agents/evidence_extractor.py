
import json

from llm.provider import client


def extract_research_findings(
    topic: str,
    search_results: list[dict]
) -> list[dict]:
    """
    Extract structured findings from search results.
    """

    if not search_results:
        raise ValueError("No search results provided.")

    evidence = []

    for index, result in enumerate(search_results, start=1):
        evidence.append({
            "id": index,
            "title": result["title"],
            "content": result["content"],
            "source": result["source"]
        })

    prompt = f"""
You are an evidence extraction assistant.

Research topic:
{topic}

Retrieved search results:
{json.dumps(evidence, ensure_ascii=False, indent=2)}

Your task:
Extract relevant findings supported by the supplied search results.

Return ONLY valid JSON using this structure:

{{
    "findings": [
        {{
            "claim": "A concise research finding",
            "explanation": "Supporting details from the retrieved content",
            "category": "opportunity/challenge/trend",
            "source_id": 1
        }}
    ]
}}

Rules:
1. Only use information present in the supplied results.
2. Never invent statistics, dates or facts.
3. Every finding must reference a valid source_id.
4. Do not combine unrelated claims.
5. If evidence is insufficient, return an empty findings list.
6. Keep findings relevant to the research topic.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "You extract evidence and return valid JSON only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        max_tokens=1500,
        response_format={"type": "json_object"}
    )

    raw_output = response.choices[0].message.content

    parsed = json.loads(raw_output)

    extracted_findings = parsed.get("findings", [])

    # Validate source references and attach original URLs.
    validated_findings = []

    for finding in extracted_findings:

        source_id = finding.get("source_id")

        if not isinstance(source_id, int):
            continue

        if source_id < 1 or source_id > len(evidence):
            continue

        if finding.get("category") not in [
            "opportunity",
            "challenge",
            "trend"
        ]:
            continue

        source = evidence[source_id - 1]

        validated_findings.append({
            "claim": finding.get("claim", ""),
            "explanation": finding.get("explanation", ""),
            "category": finding["category"],
            "source": source["source"],
            "source_title": source["title"]
        })

    return validated_findings
