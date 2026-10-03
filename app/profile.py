import json
from pathlib import Path

from app.schemas import CandidateProfile


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROFILE_PATH = (
    PROJECT_ROOT / "data" / "candidate_profile.json"
)


def load_candidate_profile(
    profile_path: Path = DEFAULT_PROFILE_PATH,
) -> CandidateProfile:
    if not profile_path.exists():
        raise FileNotFoundError(
            f"Candidate profile not found: {profile_path}"
        )

    with profile_path.open(encoding="utf-8") as file:
        profile_data = json.load(file)

    return CandidateProfile.model_validate(profile_data)