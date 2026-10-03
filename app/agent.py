import os
from functools import lru_cache
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver

from app.tools import AGENT_TOOLS


PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

MODEL_NAME = "openai/gpt-oss-20b"

SYSTEM_PROMPT = """
You are JobMatch Agent, an honest assistant for student job applications.

You have tools for:
1. Loading the candidate's verified profile.
2. Extracting requirements from a job advertisement.
3. Calculating a deterministic job-match score.
4. Creating an evidence-based application checklist.

Rules:
- Never invent skills, education, experience, or job requirements.
- Never calculate a match score yourself.
- Use calculate_job_match for every score.
- For a complete job analysis, call tools in this order:
  get_candidate_profile, extract_requirements,
  calculate_job_match, create_application_checklist.
- Pass tool outputs exactly as JSON to the next relevant tool.
- Clearly distinguish matched, preferred, and missing skills.
- Never tell the user to claim experience they do not have.
- Explain that the score is decision support, not a hiring prediction.
- Keep final answers organized and concise.
"""


@lru_cache(maxsize=1)
def get_jobmatch_agent():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY was not found. "
            "Add it to the private .env file."
        )

    model = ChatGroq(
        api_key=api_key,
        model=MODEL_NAME,
        temperature=0,
        max_tokens=2000,
        max_retries=3,
        timeout=45.0,
    )

    memory = InMemorySaver()

    return create_agent(
        model=model,
        tools=AGENT_TOOLS,
        system_prompt=SYSTEM_PROMPT,
        checkpointer=memory,
    )


def run_agent(
    message: str,
    thread_id: str = "default-user",
) -> dict[str, Any]:
    if not message.strip():
        raise ValueError("The message cannot be empty.")

    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    agent = get_jobmatch_agent()

    return agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": message,
                }
            ]
        },
        config=config,
    )