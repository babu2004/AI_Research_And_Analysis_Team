class ResearchState(TypedDict):
    topic: str                          # User research topic
    task_plan: List[str]                # Tasks decomposed by Supervisor
    research_findings: List[dict]       # Research results [{content, source}]
    analysis_insights: dict             # Analysis results {opportunities, challenges, trends}
    data_results: dict                  # Data calculation results
    final_report: str                   # Final report (Markdown)
    next_agent: str                     # Next node for routing
    error_log: List[str]                # Error records
    iteration_count: int                # Iteration count, prevents infinite loops