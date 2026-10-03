from app.agent import run_agent


JOB_ADVERTISEMENT = """
Example Robotics GmbH is hiring a Working Student Software Engineer
in Darmstadt.

Responsibilities:
- Develop Python backend services
- Design and maintain REST APIs
- Write automated tests
- Collaborate using Git

Required:
- Currently enrolled in Computer Science or a related degree
- Good Python knowledge
- Experience with Git
- English communication skills

Nice to have:
- FastAPI experience
- Docker knowledge
- PostgreSQL experience
"""

prompt = f"""
Perform a complete analysis of this job advertisement.

You must:
1. Extract its requirements.
2. Calculate the match using my verified profile.
3. Create an application checklist.
4. Explain matched and missing skills honestly.

Job advertisement:
{JOB_ADVERTISEMENT}
"""

result = run_agent(
    prompt,
    thread_id="full-analysis-test",
)

print("TOOLS USED")
for message in result["messages"]:
    tool_calls = getattr(message, "tool_calls", None)

    if tool_calls:
        for tool_call in tool_calls:
            print(f"- {tool_call['name']}")

print("\nFINAL RESPONSE")
print(result["messages"][-1].content)