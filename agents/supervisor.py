from agents.research_state import ResearchState

def create_task_plan(state: ResearchState):
    """
    Initialize the task plan for the research workflow
    """

    task_plan = [
        "research",
        "analysis",
        "data",
        "report"
    ]

    task_status = {
        "research": "pending",
        "analysis": "pending",
        "data": "pending",
        "report": "pending"
    }

    return {
        "task_plan": task_plan,
        "task_status": task_status,
        "next_agent": "research",
        "iteration_count": 0,
        "workflow_status": "running"
    }

def supervisor_router(state: ResearchState):
    """
    Decide which agent should execute next.
    """
    task_status = state["task_status"]

    if state["iteration_count"] >= 10:
        return {
            "next_agent": "end",
            "workflow_status": "failed",
            "error_log": state["error_log"] + ["Maximum workflow iterations reached."]
        }

    for task in state["task_plan"]:

        if task_status[task] == "pending":
            return {
                "next_agent": task,
                "iteration_count": state["iteration_count"]+1
            }
    
    return {
        "next_agent": "end",
        "workflow_status": "completed"
    }