from unittest.mock import MagicMock, patch

import pytest

from app.agent import run_agent


def test_empty_agent_message_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="message cannot be empty",
    ):
        run_agent("   ")


@patch("app.agent.get_jobmatch_agent")
def test_agent_uses_thread_id_and_user_message(
    mock_get_agent,
) -> None:
    fake_agent = MagicMock()
    fake_agent.invoke.return_value = {
        "messages": ["mock response"],
    }
    mock_get_agent.return_value = fake_agent

    result = run_agent(
        "Analyze this job",
        thread_id="test-thread-123",
    )

    assert result == {
        "messages": ["mock response"],
    }

    fake_agent.invoke.assert_called_once_with(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Analyze this job",
                }
            ]
        },
        config={
            "configurable": {
                "thread_id": "test-thread-123",
            }
        },
    )