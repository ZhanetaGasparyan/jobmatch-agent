import json
from pathlib import Path

from app.schemas import CandidateProfile


PROJECT_ROOT = Path(__file__).resolve().parents[1]
profile_path = PROJECT_ROOT / "data" / "candidate_profile.json"

with profile_path.open(encoding="utf-8") as file:
    profile_data = json.load(file)

profile = CandidateProfile.model_validate(profile_data)

print(f"Profile valid: {profile.name}")
print(f"Skills recorded: {len(profile.skills)}")
print(f"Target roles: {len(profile.target_roles)}")