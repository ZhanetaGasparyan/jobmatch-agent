from langchain_core.messages import ToolMessage

from app.result_parser import parse_job_comparison
from app.schemas import JobRequirements, MatchAnalysis


def test_parser_builds_job_comparison() -> None:
    requirements = JobRequirements(
        job_title="Working Student AI",
        company="Example GmbH",
        required_skills=["Python", "Docker"],
        preferred_skills=["PostgreSQL"],
    )

    analysis = MatchAnalysis(
        score=65,
        missing_required_skills=["Docker"],
        missing_preferred_skills=["PostgreSQL"],
        recommendation="possible_match",
    )

    messages = [
        ToolMessage(
            content=requirements.model_dump_json(),
            tool_call_id="requirements-call",
            name="extract_requirements",
        ),
        ToolMessage(
            content=analysis.model_dump_json(),
            tool_call_id="analysis-call",
            name="calculate_job_match",
        ),
    ]

    comparison = parse_job_comparison(messages)

    assert comparison is not None
    assert comparison.job_title == "Working Student AI"
    assert comparison.company == "Example GmbH"
    assert comparison.score == 65
    assert comparison.missing_required_skills == ["Docker"]


def test_parser_returns_none_when_analysis_is_missing() -> None:
    requirements = JobRequirements(
        job_title="Working Student",
    )

    messages = [
        ToolMessage(
            content=requirements.model_dump_json(),
            tool_call_id="requirements-call",
            name="extract_requirements",
        )
    ]

    assert parse_job_comparison(messages) is None