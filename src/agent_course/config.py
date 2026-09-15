"""Environment-backed course configuration."""

from enum import StrEnum

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class ModelMode(StrEnum):
    MOCK = "mock"
    RECORDED = "recorded"
    LIVE = "live"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    model_provider: str = "openrouter"
    model_base_url: str = "https://openrouter.ai/api/v1"
    model_name: str = "published-by-instructor-after-benchmark"
    openrouter_api_key: str = ""
    model_mode: ModelMode = ModelMode.MOCK
    max_agent_steps: int = Field(default=8, ge=1, le=8)
    max_run_cost_usd: float = Field(default=0.10, gt=0, le=0.10)
    max_output_tokens: int = Field(default=1024, ge=1, le=4096)

    @field_validator("model_name")
    @classmethod
    def reject_router_aliases(cls, value: str) -> str:
        if value in {"openrouter/auto", "openrouter/free"}:
            raise ValueError("Use the exact instructor-published course model")
        return value

    def require_live_credentials(self) -> None:
        if self.model_mode is not ModelMode.LIVE:
            return
        if not self.openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY is required in live mode")
        if self.model_name == "published-by-instructor-after-benchmark":
            raise ValueError("MODEL_NAME has not been published by the instructor")
