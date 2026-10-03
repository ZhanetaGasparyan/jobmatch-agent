import json

from app.tools import (
    calculate_job_match,
    create_application_checklist,
    get_candidate_profile,
)


def test_profile_tool_returns_verified_profile() -> None:
    result = get_candidate_profile.invoke({})
    profile = json.loads(result)

    assert profile["name"] == "Zhaneta Gasparyan"
    assert len(profile["skills"]) > 0


def test_match_tool_uses_deterministic_scoring() -> None:
    requirements = {
        "job_title": "Working Student",
        "company": "Example Company",
        "required_skills": [
            "Python",
            "Git",
            "REST API",
            "Docker",
        ],
        "preferred_skills": [
            "FastAPI",
            "PostgreSQL",
        ],
        "required_languages": [],
        "responsibilities": [],
        "education_requirements": [],
    }

    result = calculate_job_match.invoke(
        {
            "requirements_json": json.dumps(requirements),
        }
    )
    analysis = json.loads(result)

    assert analysis["score"] == 70
    assert analysis["missing_required_skills"] == ["Docker"]


def test_checklist_does_not_invent_missing_skill() -> None:
    analysis = {
        "score": 50,
        "matched_skills": [],
        "missing_required_skills": ["Docker"],
        "missing_preferred_skills": ["PostgreSQL"],
        "recommendation": "possible_match",
    }

    result = create_application_checklist.invoke(
        {
            "analysis_json": json.dumps(analysis),
        }
    )
    checklist = json.loads(result)

    actions = [
        item["action"]
        for item in checklist["checklist"]
    ]

    assert any("Do not claim Docker" in action for action in actions)
    assert any("PostgreSQL" in action for action in actions)