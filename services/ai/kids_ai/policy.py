from __future__ import annotations

import re
from .models import Intent

STOP_PATTERNS = re.compile(r"\b(fire|flame|mains|outlet|bleach|gasoline|broken glass|fuego|llama|enchufe|lej[ií]a|gasolina|vidrio roto)\b", re.I)
REFUSAL_PATTERNS = re.compile(
    r"\b(diagnos\w*|learning delay|another family|full name|birthday|remove (?:the )?adult|publish .*invent\w*|oldest child supervise|"
    r"diagnostic\w*|retraso de aprendizaje|otra familia|nombre completo|cumplea[nñ]os|elimina (?:la )?revisi[oó]n adulta|publica .*invent\w*|niñ[oa] mayor supervise)\b",
    re.I,
)
REPLACE_PATTERNS = re.compile(r"\b(replace|another activity|different activity|change activity|otra actividad|cambi\w*(?: la)? actividad|reemplaz\w*)\b", re.I)
ADAPT_PATTERNS = re.compile(r"\b(adapt\w*|ad[aá]pt\w*|easier|harder|shorter|more time|less mess|f[aá]cil|dif[ií]cil|cort[oa]|menos desorden|m[aá]s tiempo)\b", re.I)


def classify_intent(message: str) -> Intent:
    if REPLACE_PATTERNS.search(message):
        return "replace_planned_activity"
    if ADAPT_PATTERNS.search(message):
        return "adapt_current_activity"
    return "troubleshoot"


def contains_unapproved_hazard(message: str) -> bool:
    return bool(STOP_PATTERNS.search(message))


def contains_disallowed_request(message: str) -> bool:
    return bool(REFUSAL_PATTERNS.search(message))


def preference_reason(message: str) -> str | None:
    categories = {
        "mess": r"mess|messy|cleanup|desorden|limpiar|sucio",
        "duration": r"time|long|short|tiempo|largo|corto",
        "difficulty": r"hard|easy|difficult|dif[ií]cil|f[aá]cil",
        "materials": r"material|missing|don.t have|falta|no tengo",
        "participants": r"child|children|person|niñ|persona",
        "interest": r"boring|interest|aburr|inter[eé]s",
        "preparation": r"prepare|setup|prepar",
    }
    lowered = message.lower()
    return next((name for name, pattern in categories.items() if re.search(pattern, lowered)), None)


def is_explicit_family_constraint(message: str) -> bool:
    return bool(re.search(r"\b(never|do not ever|don.t show|nunca|jam[aá]s|no muestres)\b", message, re.I))
