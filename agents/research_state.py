from typing import TypedDict


class ResearchState(TypedDict):
    # User input
    topic: str

    # Supervisor
    task_plan: list[str]
    task_status: dict[str, str]
    next_agent: str

    # Research Agent
    research_findings: list[dict]

    # Analysis Agent
    analysis_insights: dict

    # Data Agent
    data_results: dict

    # Report Agent
    final_report: str

    # Workflow management
    error_log: list[str]
    iteration_count: int
    workflow_status: str


