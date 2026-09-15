import pytest
from pydantic import ValidationError

from agent_course.config import Settings


def test_rejects_router_alias() -> None:
    with pytest.raises(ValidationError):
        Settings(model_name="openrouter/auto")


def test_limits_agent_steps() -> None:
    with pytest.raises(ValidationError):
        Settings(max_agent_steps=9)
