
from agents.supervisor import (
    create_task_plan,
    supervisor_router
)


def test_supervisor():

    state = {
        "topic": "Electric vehicle growth in India",
        "research_findings": [],
        "analysis_insights": {},
        "data_results": {},
        "final_report": "",
        "error_log": [],
        "iteration_count": 0,
        "workflow_status": "running"
    }

    # Initialize workflow
    state.update(create_task_plan(state))

    print("\n[INITIAL STATE]")
    print(state)

    # Simulate specialist execution
    for agent in ["research", "analysis", "data", "report"]:

        decision = supervisor_router(state)
        state.update(decision)

        print(f"\n[SUPERVISOR] Next agent: {state['next_agent']}")

        if state["next_agent"] == "end":
            break

        # Simulate successful agent completion
        state["task_status"][agent] = "completed"

    # Final decision
    decision = supervisor_router(state)
    state.update(decision)

    print("\n[FINAL STATE]")
    print(state)

    assert state["next_agent"] == "end"
    assert state["workflow_status"] == "completed"

    print("\n[SUCCESS] Supervisor test passed!")


if __name__ == "__main__":
    test_supervisor()
