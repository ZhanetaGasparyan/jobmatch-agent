import json
from pathlib import Path

from app.schemas import CandidateProfile, JobRequirements
from app.scoring import analyze_match


PROJECT_ROOT = Path(__file__).resolve().parents[1]

with (PROJECT_ROOT / "data" / "candidate_profile.json").open(
    encoding="utf-8"
) as file:
    profile = CandidateProfile.model_validate(json.load(file))

requirements = JobRequirements(
    job_title="Working Student Software Engineering",
    company="Example Company",
    required_skills=[
        "Python",
        "Git",
        "REST API",
        "Docker",
    ],
    preferred_skills=[
        "FastAPI",
        "PostgreSQL",
    ],
)

analysis = analyze_match(profile, requirements)

print(f"Score: {analysis.score}")
print(f"Recommendation: {analysis.recommendation}")
print(f"Missing required: {analysis.missing_required_skills}")
print(f"Missing preferred: {analysis.missing_preferred_skills}")

for match in analysis.matched_skills:
    print(
        f"- {match.required_skill}: {match.status}"
        f" -> {match.matched_candidate_skill}"
    )