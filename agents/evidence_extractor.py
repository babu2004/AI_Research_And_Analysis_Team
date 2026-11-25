
import json
from llm.provider import client


def extract_research_findings(
    topic: str,
    search_results: list[dict]
) -> list[dict]:

    if not search_results:
        raise ValueError("No search results provided.")

    evidence = []

    for index, result in enumerate(search_results, start=1):
        evidence.append({
            "id": index,
            "title": result["title"][:200],
            "content": result["content"][:700],
            "source": result["source"]
        })

    prompt = f"""
You are an evidence extraction assistant.

Research topic: {topic}

Search results:
{json.dumps(evidence, ensure_ascii=False)}

Extract at most 3 important findings supported by these results.

Return JSON in this exact structure:
{{
    "findings": [
        {{
            "claim": "Short factual claim",
            "explanation": "Brief supporting explanation",
            "category": "opportunity",
            "source_id": 1
        }}
    ]
}}

Rules:
- Use only information in the supplied search results.
- Never invent statistics, dates, or facts.
- Every finding must reference a valid source_id.
- Category must be opportunity, challenge, or trend.
- Keep claims and explanations concise.
- Do not repeat the same finding.
- Return an empty findings list if evidence is insufficient.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "Extract evidence and return valid JSON only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        max_tokens=3000,
        response_format={"type": "json_object"}
    )

    raw_output = response.choices[0].message.content
    parsed = json.loads(raw_output)

    extracted_findings = parsed.get("findings", [])

    validated_findings = []

    for finding in extracted_findings:

        source_id = finding.get("source_id")

        if not isinstance(source_id, int):
            continue

        if source_id < 1 or source_id > len(evidence):
            continue

        if finding.get("category") not in [
            "opportunity", "challenge", "trend"
        ]:
            continue

        claim = finding.get("claim", "").strip()
        explanation = finding.get("explanation", "").strip()

        if not claim or not explanation:
            continue

        source = evidence[source_id - 1]

        validated_findings.append({
            "claim": claim,
            "explanation": explanation,
            "category": finding["category"],
            "source": source["source"],
            "source_title": source["title"]
        })

    return validated_findings
