import json

import pytest
from pydantic import ValidationError

from app.profile import load_candidate_profile


def test_candidate_profile_loads_successfully() -> None:
    profile = load_candidate_profile()

    assert profile.name == "Zhaneta Gasparyan"
    assert len(profile.skills) > 0
    assert any(skill.name == "Python" for skill in profile.skills)


def test_invalid_profile_is_rejected(tmp_path) -> None:
    invalid_profile_path = tmp_path / "invalid_profile.json"

    invalid_profile_path.write_text(
        json.dumps(
            {
                "name": "",
                "skills": [],
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValidationError):
        load_candidate_profile(invalid_profile_path)