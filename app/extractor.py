import json
import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

from app.schemas import JobRequirements


PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

MODEL_NAME = "openai/gpt-oss-20b"


def get_groq_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY was not found. "
            "Add it to the private .env file."
        )

    return Groq(
    api_key=api_key,
    max_retries=3,
    timeout=45.0,
)


def extract_job_requirements(job_text: str) -> JobRequirements:
    if len(job_text.strip()) < 50:
        raise ValueError(
            "The job description must contain at least 50 characters."
        )

    client = get_groq_client()

    system_prompt = """
You extract factual requirements from job advertisements.

Return one JSON object with exactly these fields:
- job_title: string
- company: string or null
- required_skills: array of strings
- preferred_skills: array of strings
- required_languages: array of strings
- responsibilities: array of strings
- education_requirements: array of strings

Rules:
- Use only information explicitly stated in the advertisement.
- Do not invent skills, responsibilities, or company information.
- Separate mandatory requirements from optional/preferred ones.
- Use short canonical skill names such as Python, Docker, Git, SQL.
- Remove duplicates.
- If information is absent, use an empty array or null.
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": job_text,
            },
        ],
        response_format={"type": "json_object"},
        temperature=0,
        reasoning_effort="low",
        max_completion_tokens=1500,
    )

    content = response.choices[0].message.content

    if not content:
        raise RuntimeError("The model returned an empty response.")

    response_data = json.loads(content)
    return JobRequirements.model_validate(response_data)