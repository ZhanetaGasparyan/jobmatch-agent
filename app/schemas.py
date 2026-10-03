from typing import Literal

from pydantic import BaseModel, Field


SkillLevel = Literal["beginner", "intermediate", "advanced"]

class JobComparison(BaseModel):
    job_title: str
    company: str | None = None
    score: int = Field(ge=0, le=100)
    recommendation: Literal[
        "strong_match",
        "possible_match",
        "needs_development",
    ]
    missing_required_skills: list[str] = Field(default_factory=list)
    missing_preferred_skills: list[str] = Field(default_factory=list)

class CandidateSkill(BaseModel):
    name: str = Field(min_length=1)
    level: SkillLevel
    evidence: str = Field(
        min_length=1,
        description="Project, course, or work experience proving this skill.",
    )


class CandidateProfile(BaseModel):
    name: str = Field(min_length=1)
    target_roles: list[str] = Field(default_factory=list)
    skills: list[CandidateSkill] = Field(default_factory=list)
    languages: list[str] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    experience_summary: list[str] = Field(default_factory=list)


class JobRequirements(BaseModel):
    job_title: str
    company: str | None = None
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    required_languages: list[str] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)
    education_requirements: list[str] = Field(default_factory=list)


class SkillMatch(BaseModel):
    required_skill: str
    matched_candidate_skill: str | None = None
    evidence: str | None = None
    status: Literal["matched", "partial", "missing"]


class MatchAnalysis(BaseModel):
    score: int = Field(ge=0, le=100)
    matched_skills: list[SkillMatch] = Field(default_factory=list)
    missing_required_skills: list[str] = Field(default_factory=list)
    missing_preferred_skills: list[str] = Field(default_factory=list)
    recommendation: Literal[
        "strong_match",
        "possible_match",
        "needs_development",
    ]