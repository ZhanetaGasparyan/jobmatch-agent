from app.agent import run_agent


THREAD_ID = "manual-agent-test"

first_result = run_agent(
    "Load my verified candidate profile and summarize my skills.",
    thread_id=THREAD_ID,
)

print("FIRST RESPONSE")
print(first_result["messages"][-1].content)

print("\nTOOLS USED")
for message in first_result["messages"]:
    if getattr(message, "tool_calls", None):
        for tool_call in message.tool_calls:
            print(f"- {tool_call['name']}")

second_result = run_agent(
    "Which of those skills has evidence involving predictive maintenance?",
    thread_id=THREAD_ID,
)

print("\nFOLLOW-UP RESPONSE")
print(second_result["messages"][-1].content)