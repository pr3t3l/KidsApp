from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import httpx


SYSTEM_PROMPT = """You assist an adult facilitating one published family learning activity. Use only the supplied activity context. Never invent a material substitution, remove a safety rule, diagnose a child, or claim certainty without evidence. If safety cannot be verified, tell the adult to stop. Return only JSON matching the response schema. Keep the answer concise and actionable."""


@dataclass
class GeneratedAnswer:
    answer: str
    uncertainty: str
    safety_status: str
    model_route: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    cost_usd: float | None = None


class OpenRouterGateway:
    def __init__(self, settings: Any):
        self.settings = settings

    async def answer(self, message: str, locale: str, context: str) -> GeneratedAnswer:
        if not self.settings.openrouter_api_key:
            return self._safe_template(locale, context)
        last_error: Exception | None = None
        for model in (self.settings.primary_model, self.settings.fallback_model):
            try:
                payload = {
                    "model": model,
                    "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": f"Locale: {locale}\nActivity evidence:\n{context}\nAdult message: {message}"}],
                    "temperature": 0.1,
                    "max_tokens": 350,
                    "response_format": {"type": "json_schema", "json_schema": {"name": "bounded_answer", "strict": True, "schema": {"type": "object", "additionalProperties": False, "required": ["answer", "uncertainty", "safety_status"], "properties": {"answer": {"type": "string"}, "uncertainty": {"enum": ["low", "medium", "high"]}, "safety_status": {"enum": ["safe", "stop"]}}}}},
                    "provider": {"allow_fallbacks": False, "require_parameters": True, "data_collection": "deny", "zdr": True},
                }
                async with httpx.AsyncClient(timeout=12) as client:
                    response = await client.post(f"{self.settings.openrouter_base_url}/chat/completions", headers={"Authorization": f"Bearer {self.settings.openrouter_api_key}", "Content-Type": "application/json", "HTTP-Referer": self.settings.site_url, "X-Title": self.settings.app_name}, json=payload)
                response.raise_for_status()
                body = response.json()
                content = body["choices"][0]["message"]["content"]
                import json
                result = json.loads(content)
                usage = body.get("usage", {})
                return GeneratedAnswer(answer=result["answer"], uncertainty=result["uncertainty"], safety_status=result["safety_status"], model_route=model, prompt_tokens=int(usage.get("prompt_tokens", 0)), completion_tokens=int(usage.get("completion_tokens", 0)), cost_usd=usage.get("cost"))
            except (httpx.HTTPError, KeyError, ValueError, TypeError) as error:
                last_error = error
        raise RuntimeError("No eligible model route completed the request") from last_error

    async def embed(self, text: str) -> list[float]:
        if not self.settings.openrouter_api_key:
            raise RuntimeError("Embedding provider is not configured")
        payload = {
            "model": self.settings.embedding_model,
            "input": text,
            "dimensions": 1536,
            "encoding_format": "float",
            "provider": {"data_collection": "deny", "zdr": True},
        }
        async with httpx.AsyncClient(timeout=12) as client:
            response = await client.post(
                f"{self.settings.openrouter_base_url}/embeddings",
                headers={"Authorization": f"Bearer {self.settings.openrouter_api_key}", "Content-Type": "application/json", "HTTP-Referer": self.settings.site_url, "X-Title": self.settings.app_name},
                json=payload,
            )
        response.raise_for_status()
        embedding = response.json()["data"][0]["embedding"]
        if len(embedding) != 1536:
            raise RuntimeError("Embedding dimension mismatch")
        return embedding

    @staticmethod
    def _safe_template(locale: str, context: str) -> GeneratedAnswer:
        # The deterministic demo deliberately does not echo the compact internal
        # context. That context is an implementation detail and may later contain
        # fields that are safe for the model but not useful in the UI.
        del context
        if locale == "es-US":
            answer = "Revisa el paso y el aviso de seguridad publicados que aparecen en pantalla. Si no puedes verificarlos de forma segura, detén la actividad."
        else:
            answer = "Review the published step and safety notice shown on screen. If you cannot verify them safely, stop the activity."
        return GeneratedAnswer(answer=answer, uncertainty="medium", safety_status="safe", model_route="deterministic-demo")
