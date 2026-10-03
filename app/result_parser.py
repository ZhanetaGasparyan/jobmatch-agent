from typing import Any

from app.schemas import (
    JobComparison,
    JobRequirements,
    MatchAnalysis,
)


def parse_job_comparison(
    messages: list[Any],
) -> JobComparison | None:
    requirements_json: str | None = None
    analysis_json: str | None = None

    for message in messages:
        tool_name = getattr(message, "name", None)
        content = getattr(message, "content", None)

        if not isinstance(content, str):
            continue

        if tool_name == "extract_requirements":
            requirements_json = content

        if tool_name == "calculate_job_match":
            analysis_json = content

    if requirements_json is None or analysis_json is None:
        return None

    requirements = JobRequirements.model_validate_json(
        requirements_json
    )
    analysis = MatchAnalysis.model_validate_json(
        analysis_json
    )

    return JobComparison(
        job_title=requirements.job_title,
        company=requirements.company,
        score=analysis.score,
        recommendation=analysis.recommendation,
        missing_required_skills=analysis.missing_required_skills,
        missing_preferred_skills=analysis.missing_preferred_skills,
    )