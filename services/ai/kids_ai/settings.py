from __future__ import annotations

from dataclasses import dataclass
import os


def _bool(name: str, default: bool) -> bool:
    return os.getenv(name, str(default)).lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    app_env: str = os.getenv("APP_ENV", "development")
    demo_mode: bool = _bool("DEMO_MODE", True)
    allowed_origins: tuple[str, ...] = tuple(filter(None, os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173,http://localhost:8080").split(",")))
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_publishable_key: str = os.getenv("SUPABASE_PUBLISHABLE_KEY", "")
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    openrouter_base_url: str = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    primary_model: str = os.getenv("OPENROUTER_PRIMARY_MODEL", "openai/gpt-4.1-mini")
    fallback_model: str = os.getenv("OPENROUTER_FALLBACK_MODEL", "anthropic/claude-sonnet-4")
    approved_models: tuple[str, ...] = tuple(filter(None, os.getenv("OPENROUTER_APPROVED_MODELS", "").split(",")))
    embedding_model: str = os.getenv("OPENROUTER_EMBEDDING_MODEL", "openai/text-embedding-3-small")
    site_url: str = os.getenv("OPENROUTER_SITE_URL", "http://localhost:5173")
    app_name: str = os.getenv("OPENROUTER_APP_NAME", "Kids Learning System")
    logfire_token: str = os.getenv("LOGFIRE_TOKEN", "")
    monthly_budget_usd: float = float(os.getenv("MONTHLY_INFERENCE_BUDGET_USD", "15"))

    def validate_production(self) -> None:
        missing = [name for name, value in {
            "SUPABASE_URL": self.supabase_url,
            "SUPABASE_PUBLISHABLE_KEY": self.supabase_publishable_key,
            "OPENROUTER_API_KEY": self.openrouter_api_key,
            "OPENROUTER_APPROVED_MODELS": self.approved_models,
        }.items() if not value]
        if not self.demo_mode and missing:
            raise RuntimeError(f"Missing production configuration: {', '.join(missing)}")
        if not self.demo_mode and ({self.primary_model, self.fallback_model} - set(self.approved_models)):
            raise RuntimeError("Primary and fallback models must both be in OPENROUTER_APPROVED_MODELS")
