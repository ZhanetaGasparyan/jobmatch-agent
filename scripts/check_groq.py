import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq


PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError("GROQ_API_KEY was not found in the .env file.")

client = Groq(api_key=api_key)

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": "Reply with exactly: JobMatch connection successful",
        }
    ],
    temperature=0,
    max_completion_tokens=300,
)

answer = response.choices[0].message.content

if answer:
    print(answer)
else:
    print("Connection succeeded, but the model returned no visible text.")