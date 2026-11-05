import traceback

from langchain_core.messages import HumanMessage

from app.agent import compiled_graph

state = {
    "messages": [HumanMessage(content="list pods")],
    "diagnostic_report": "",
    "remediation_needed": False,
    "goal_achieved": False,
    "issues": [],
    "retry_context": "",
    "proposed_fix": "",
    "approval_status": "pending",
    "fix_result": "",
    "verification_result": "",
    "attempt": 0,
}

try:
    out = compiled_graph.invoke(state, {"configurable": {"thread_id": "test1"}})
    print("SUCCESS")
    print(out.get("diagnostic_report"))
except Exception as e:
    traceback.print_exc()
    print("\n--- ERROR CHAIN ---")
    c = e
    seen = set()
    while c is not None and id(c) not in seen:
        seen.add(id(c))
        print("CAUSE:", type(c).__name__, str(c)[:200])
        c = c.__cause__ or c.__context__