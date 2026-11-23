
from agents.research_state import ResearchState
from tools.web_search import search_web


def research_node(state: ResearchState) -> dict:
    """
    Research node retrieves information for the given topic.
    """

    topic = state["topic"]

    try:
        print(f"\n[RESEARCH AGENT] Researching: {topic}")

        findings = search_web(topic, max_results=5)

        if not findings:
            raise ValueError("No search results found.")

        print(f"[RESEARCH AGENT] Retrieved {len(findings)} results.")

        return {
            "research_findings": findings,
            "task_status": {
                **state["task_status"],
                "research": "completed"
            }
        }

    except Exception as error:

        print(f"[RESEARCH AGENT ERROR] {error}")

        return {
            "error_log": state["error_log"] + [
                f"Research Agent: {str(error)}"
            ],
            "task_status": {
                **state["task_status"],
                "research": "failed"
            }
        }
