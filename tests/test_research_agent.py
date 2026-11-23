
from agents.research_agent import research_node


def test_research_node():

    state = {
        "topic": "Electric vehicle growth in India",
        "task_plan": ["research", "analysis", "data", "report"],
        "research_findings": [],
        "analysis_insights": {},
        "data_results": {},
        "final_report": "",
        "next_agent": "research",
        "error_log": [],
        "iteration_count": 0,
        "task_status": {
            "research": "pending",
            "analysis": "pending",
            "data": "pending",
            "report": "pending"
        },
        "workflow_status": "running"
    }

    result = research_node(state)

    print("\n[RESEARCH FINDINGS]")
    for finding in result.get("research_findings", []):
        print(finding)

    assert result["task_status"]["research"] == "completed"
    assert len(result["research_findings"]) > 0

    print("\n[SUCCESS] Research Agent test passed!")


if __name__ == "__main__":
    test_research_node()
