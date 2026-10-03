from app.extractor import extract_job_requirements


SAMPLE_JOB = """
Example Robotics GmbH is looking for a Working Student Software
Engineering in Darmstadt.

You will develop Python services, create REST APIs, write automated
tests, and use Git as part of our development workflow.

Required qualifications:
- Currently enrolled in Computer Science or a related degree
- Good Python knowledge
- Experience with Git
- English communication skills

Nice to have:
- Experience with FastAPI
- Docker knowledge
- Familiarity with PostgreSQL
"""

requirements = extract_job_requirements(SAMPLE_JOB)

print(requirements.model_dump_json(indent=2))