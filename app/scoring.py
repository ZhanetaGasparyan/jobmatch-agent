import re

from app.schemas import (
    CandidateProfile,
    JobRequirements,
    MatchAnalysis,
    SkillMatch,
)


SKILL_ALIASES = {
    "sklearn": "scikit learn",
    "scikit-learn": "scikit learn",
    "rest api": "rest api",
    "rest apis": "rest api",
    "restful api": "rest api",
    "restful apis": "rest api",
    "github action": "github actions",
    "ml": "machine learning",
    "opcua": "opc ua",
}


def normalize_skill(skill: str) -> str:
    normalized = skill.lower().strip()
    normalized = re.sub(r"[^a-z0-9+#. ]", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return SKILL_ALIASES.get(normalized, normalized)


def find_candidate_skill(
    required_skill: str,
    profile: CandidateProfile,
):
    required_normalized = normalize_skill(required_skill)

    for candidate_skill in profile.skills:
        candidate_normalized = normalize_skill(candidate_skill.name)

        if required_normalized == candidate_normalized:
            return candidate_skill

    return None


def build_skill_match(
    required_skill: str,
    profile: CandidateProfile,
) -> SkillMatch:
    candidate_skill = find_candidate_skill(required_skill, profile)

    if candidate_skill is None:
        return SkillMatch(
            required_skill=required_skill,
            status="missing",
        )

    return SkillMatch(
        required_skill=required_skill,
        matched_candidate_skill=candidate_skill.name,
        evidence=candidate_skill.evidence,
        status="matched",
    )


def calculate_percentage(matches: list[SkillMatch]) -> float:
    if not matches:
        return 100.0

    matched_count = sum(
        match.status == "matched"
        for match in matches
    )

    return matched_count / len(matches) * 100


def analyze_match(
    profile: CandidateProfile,
    requirements: JobRequirements,
) -> MatchAnalysis:
    required_matches = [
        build_skill_match(skill, profile)
        for skill in requirements.required_skills
    ]

    preferred_matches = [
        build_skill_match(skill, profile)
        for skill in requirements.preferred_skills
    ]

    required_percentage = calculate_percentage(required_matches)
    preferred_percentage = calculate_percentage(preferred_matches)

    if requirements.required_skills and requirements.preferred_skills:
        score = round(
            required_percentage * 0.8
            + preferred_percentage * 0.2
        )
    elif requirements.required_skills:
        score = round(required_percentage)
    elif requirements.preferred_skills:
        score = round(preferred_percentage)
    else:
        score = 0

    if score >= 75:
        recommendation = "strong_match"
    elif score >= 50:
        recommendation = "possible_match"
    else:
        recommendation = "needs_development"

    missing_required = [
        match.required_skill
        for match in required_matches
        if match.status == "missing"
    ]

    missing_preferred = [
        match.required_skill
        for match in preferred_matches
        if match.status == "missing"
    ]

    return MatchAnalysis(
        score=score,
        matched_skills=required_matches + preferred_matches,
        missing_required_skills=missing_required,
        missing_preferred_skills=missing_preferred,
        recommendation=recommendation,
    )