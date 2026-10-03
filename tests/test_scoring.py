from app.schemas import (
    CandidateProfile,
    CandidateSkill,
    JobRequirements,
)
from app.scoring import analyze_match, normalize_skill


def create_test_profile() -> CandidateProfile:
    return CandidateProfile(
        name="Test Candidate",
        skills=[
            CandidateSkill(
                name="Python",
                level="advanced",
                evidence="Built multiple Python projects.",
            ),
            CandidateSkill(
                name="Git",
                level="intermediate",
                evidence="Used Git for version control.",
            ),
            CandidateSkill(
                name="REST APIs",
                level="intermediate",
                evidence="Built REST endpoints.",
            ),
            CandidateSkill(
                name="FastAPI",
                level="intermediate",
                evidence="Built a FastAPI application.",
            ),
        ],
    )


def test_skill_aliases_are_normalized() -> None:
    assert normalize_skill("REST APIs") == "rest api"
    assert normalize_skill("REST API") == "rest api"
    assert normalize_skill("scikit-learn") == "scikit learn"
    assert normalize_skill("ML") == "machine learning"


def test_match_score_is_calculated_transparently() -> None:
    profile = create_test_profile()

    requirements = JobRequirements(
        job_title="Working Student",
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

    result = analyze_match(profile, requirements)

    assert result.score == 70
    assert result.recommendation == "possible_match"
    assert result.missing_required_skills == ["Docker"]
    assert result.missing_preferred_skills == ["PostgreSQL"]


def test_unknown_skill_is_not_invented() -> None:
    profile = create_test_profile()

    requirements = JobRequirements(
        job_title="Working Student",
        required_skills=["Kubernetes"],
    )

    result = analyze_match(profile, requirements)

    assert result.score == 0
    assert result.recommendation == "needs_development"
    assert result.missing_required_skills == ["Kubernetes"]

    match = result.matched_skills[0]
    assert match.status == "missing"
    assert match.matched_candidate_skill is None
    assert match.evidence is None


def test_empty_requirements_produce_zero_score() -> None:
    profile = create_test_profile()

    requirements = JobRequirements(
        job_title="Unspecified Position",
    )

    result = analyze_match(profile, requirements)

    assert result.score == 0
    assert result.recommendation == "needs_development"