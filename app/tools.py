import json

from langchain_core.tools import tool

from app.extractor import extract_job_requirements
from app.profile import load_candidate_profile
from app.schemas import JobRequirements, MatchAnalysis
from app.scoring import analyze_match


@tool
def get_candidate_profile() -> str:
    """Load the candidate's verified skills, education, and experience."""
    profile = load_candidate_profile()
    return profile.model_dump_json(indent=2)


@tool
def extract_requirements(job_text: str) -> str:
    """Extract structured requirements from a job advertisement."""
    requirements = extract_job_requirements(job_text)
    return requirements.model_dump_json(indent=2)


@tool
def calculate_job_match(requirements_json: str) -> str:
    """
    Compare structured job requirements with the verified candidate profile.

    The input must be a JSON string matching the JobRequirements schema.
    """
    requirements_data = json.loads(requirements_json)
    requirements = JobRequirements.model_validate(requirements_data)

    profile = load_candidate_profile()
    analysis = analyze_match(profile, requirements)

    return analysis.model_dump_json(indent=2)


@tool
def create_application_checklist(analysis_json: str) -> str:
    """
    Create an honest application checklist from a MatchAnalysis JSON string.
    """
    analysis_data = json.loads(analysis_json)
    analysis = MatchAnalysis.model_validate(analysis_data)

    checklist: list[dict[str, str]] = []

    for match in analysis.matched_skills:
        if match.status == "matched" and match.evidence:
            checklist.append(
                {
                    "priority": "high",
                    "action": (
                        f"Highlight {match.matched_candidate_skill}: "
                        f"{match.evidence}"
                    ),
                }
            )

    for skill in analysis.missing_required_skills:
        checklist.append(
            {
                "priority": "high",
                "action": (
                    f"Do not claim {skill}. Decide whether your related "
                    "experience is sufficient or whether this role should "
                    "be deprioritized."
                ),
            }
        )

    for skill in analysis.missing_preferred_skills:
        checklist.append(
            {
                "priority": "medium",
                "action": (
                    f"Treat {skill} as a learning opportunity; do not "
                    "present it as existing experience."
                ),
            }
        )

    checklist.extend(
        [
            {
                "priority": "high",
                "action": "Tailor the CV summary to the job responsibilities.",
            },
            {
                "priority": "medium",
                "action": "Proofread the application before submitting it.",
            },
        ]
    )

    return json.dumps(
        {
            "match_score": analysis.score,
            "recommendation": analysis.recommendation,
            "checklist": checklist,
        },
        indent=2,
    )


AGENT_TOOLS = [
    get_candidate_profile,
    extract_requirements,
    calculate_job_match,
    create_application_checklist,
]