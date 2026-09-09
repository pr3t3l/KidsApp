from __future__ import annotations

"""Deterministic compiler from bounded AI drafts to the versioned delivery contract.

The model proposes compact sections. This module owns identifiers, references,
hashing, family UI blocks and RAG chunks so model output can never become a
published contract merely by looking plausible.
"""

from copy import deepcopy
import hashlib
import json
import re
from typing import Any, Iterable


AREA_CODES = {
    "physics": "PHY",
    "engineering": "ENG",
    "electricity": "ELEC",
    "mathematics": "MATH",
    "safe_chemistry": "CHEM",
    "biology_nature": "BIO",
    "motor_skills": "MOTOR",
    "creativity": "CREATIVE",
    "logical_thinking": "LOGIC",
    "communication": "COMM",
    "self_regulation": "SELF_REG",
    "practical_life": "LIFE",
}


def _id(prefix: str, value: Any, fallback: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "-", str(value or fallback)).strip("-").upper()
    return f"{prefix}-{cleaned}"[:100].rstrip("-")


def _age(value: Any) -> list[int]:
    if isinstance(value, list) and len(value) == 2:
        low, high = int(value[0]), int(value[1])
    else:
        numbers = [int(item) for item in re.findall(r"\d+", str(value))]
        low, high = (numbers + [5, 10])[:2]
    low, high = max(5, min(low, 10)), max(5, min(high, 10))
    return [min(low, high), max(low, high)]


def _levels(age: list[int]) -> list[str]:
    result: list[str] = []
    for low, high, values in ((5, 6, ("L1", "L2")), (7, 8, ("L2", "L3")), (9, 10, ("L3", "L4"))):
        if age[0] <= high and age[1] >= low:
            result.extend(values)
    return list(dict.fromkeys(result)) or ["L1"]


def _strings(values: Iterable[Any], fallback: str = "Human review required.") -> list[str]:
    result = [str(value).strip() for value in values if str(value).strip()]
    return result or [fallback]


def _stage_action(stage: str) -> str:
    return {
        "discover": "encounter_problem",
        "imagine": "propose",
        "build_or_do": "build_or_do",
        "experiment": "test_or_check",
        "improve": "improve_or_recommend",
        "explain": "explain",
        "close": "explain",
        "cleanup": "observe_result",
    }.get(stage, "observe_result")


def _artifact(job: dict[str, Any], stage: str, key: str) -> dict[str, Any]:
    value = job.get("artifacts", {}).get(stage, {})
    nested = value.get(key, value)
    return nested if isinstance(nested, dict) else {}


def build_source_locale(job: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    """Build a complete English V2 contract from the small stage outputs."""

    idea = _artifact(job, "idea", "ideaBrief")
    plan = _artifact(job, "core", "corePlan")
    material_draft = _artifact(job, "materials_safety", "draft")
    step_draft = _artifact(job, "steps", "draft")
    role_draft = _artifact(job, "roles_adaptations", "draft")
    close_draft = _artifact(job, "closeout", "draft")
    brief = job.get("brief", {})

    activity_id = f"ACT-{str(job['jobId']).replace('-', '')[:10].upper()}"
    version = "0.1.0"
    age = _age((idea.get("fit") or {}).get("age") or brief.get("ageBand"))
    group_hint = (idea.get("fit") or {}).get("group") or []
    participant_brief = brief.get("participants") or {}
    sizes = sorted({int(size) for size in group_hint if isinstance(size, int) and 1 <= size <= 4})
    if not sizes:
        minimum = max(1, min(4, int(participant_brief.get("min", 1))))
        maximum = max(minimum, min(4, int(participant_brief.get("max", minimum))))
        sizes = list(range(minimum, maximum + 1))
    time_brief = brief.get("time") or {}
    minutes = int((idea.get("fit") or {}).get("minutes") or time_brief.get("max") or 30)
    min_minutes = max(5, min(minutes, int(time_brief.get("min") or max(5, minutes - 10))))
    max_minutes = max(min_minutes, min(180, int(time_brief.get("max") or minutes)))
    levels = _levels(age)
    primary = AREA_CODES.get(str(brief.get("primaryArea") or "engineering"), str(idea.get("area") or "ENG").upper())

    raw_steps = plan.get("steps") or []
    details = {str(item.get("id")): item for item in step_draft.get("steps") or []}
    if len(raw_steps) < 2:
        raw_steps = [
            {"id": "STEP-01", "entry": "STATE-READY", "exit": "STATE-ACTIVE", "actor": "group", "action": "Explore the proposed activity.", "purpose": "Notice the starting condition.", "signal": "Each participant shares one observation."},
            {"id": "STEP-02", "entry": "STATE-ACTIVE", "exit": "STATE-COMPLETE", "actor": "group", "action": "Compare the result and explain one finding.", "purpose": "Connect an action to evidence.", "signal": "Each participant explains one observation."},
        ]
    step_ids = [_id("STEP", item.get("id"), str(index + 1)) for index, item in enumerate(raw_steps)]
    state_pairs: list[tuple[str, str]] = []
    for index, item in enumerate(raw_steps):
        entry = _id("STATE", item.get("entry"), f"{index}-ENTRY")
        exit_state = _id("STATE", item.get("exit"), f"{index}-EXIT")
        if index and state_pairs[-1][1] != entry:
            entry = state_pairs[-1][1]
        state_pairs.append((entry, exit_state))

    state_meaning = {
        _id("STATE", item.get("id"), str(index)): str(item.get("meaning") or "Activity state")
        for index, item in enumerate(plan.get("states") or [])
    }
    states = list(dict.fromkeys([state for pair in state_pairs for state in pair]))

    skills_raw = _strings(plan.get("skills") or [], "Observe and explain")[:5]
    skills = [_id(f"{primary}-SKL", value, str(index + 1)) for index, value in enumerate(skills_raw)]
    skill_by_raw = {str(raw): skill for raw, skill in zip(skills_raw, skills, strict=True)}
    mechanism = str(idea.get("mechanism") or plan.get("method") or "guided investigation")
    concept_id = _id(f"{primary}-CON", mechanism, "CORE")

    materials_core: list[dict[str, Any]] = []
    materials_locale: list[dict[str, Any]] = []
    material_id_map: dict[str, str] = {}
    for index, item in enumerate(material_draft.get("materials") or []):
        material_id = _id("MAT", item.get("id") or item.get("name"), str(index + 1))
        material_id_map[str(item.get("id"))] = material_id
        substitutes_core, substitutes_locale = [], []
        for sub_index, sub in enumerate(item.get("substitutes") or []):
            sub_id = _id("SUB", sub.get("id") or sub.get("name"), f"{index + 1}-{sub_index + 1}")
            substitutes_core.append({"id": sub_id, "quantity": max(0.01, float(sub.get("quantity") or 1)), "unit": str(sub.get("unit") or "item"), "safety": sub.get("safety") if sub.get("safety") in {"none", "reviewed", "reviewed_equivalent"} else "reviewed"})
            substitutes_locale.append({"id": sub_id, "name": str(sub.get("name") or "Reviewed substitute"), "conditions": str(sub.get("conditions") or "Use only after adult confirmation."), "rationale": str(sub.get("rationale") or "Preserves the intended mechanism.")})
        materials_core.append({"id": material_id, "quantity": max(0.01, float(item.get("quantity") or 1)), "unit": str(item.get("unit") or "item"), "required": bool(item.get("required", True)), "reusable": bool(item.get("reusable", False)), "substitutes": substitutes_core})
        materials_locale.append({"id": material_id, "name": str(item.get("name") or material_id), "prep": str(item.get("prep") or "Prepare before inviting the child."), "safety": str(item.get("safety") or "Adult supervision is required."), "substitutes": substitutes_locale})
    if not materials_core:
        names = _strings(idea.get("materials") or [], "Common household material")[:12]
        for index, name in enumerate(names):
            material_id = _id("MAT", name, str(index + 1))
            materials_core.append({"id": material_id, "quantity": 1, "unit": "item", "required": True, "reusable": True, "substitutes": []})
            materials_locale.append({"id": material_id, "name": name, "prep": "Prepare before inviting the child.", "safety": "Adult supervision is required.", "substitutes": []})
            material_id_map[name] = material_id

    core_steps: list[dict[str, Any]] = []
    locale_steps: list[dict[str, Any]] = []
    for index, item in enumerate(raw_steps):
        step_id = step_ids[index]
        detail = details.get(str(item.get("id")), {})
        stage = str(detail.get("stage") or ("discover" if index == 0 else "explain" if index == len(raw_steps) - 1 else "build_or_do"))
        if stage not in {"discover", "imagine", "build_or_do", "experiment", "improve", "explain", "close", "cleanup"}:
            stage = "build_or_do"
        material_ids = [material_id_map.get(str(value), _id("MAT", value, "ITEM")) for value in detail.get("materialIds") or []]
        material_ids = [value for value in material_ids if value in {row["id"] for row in materials_core}]
        if not material_ids:
            material_ids = [row["id"] for row in materials_core]
        adult_actions = _strings(detail.get("adultActions") or [], "Stay close and support only as needed.")
        prompts = _strings(detail.get("prompts") or [], "What do you notice?")
        participant_actions = _strings(detail.get("participantActions") or [], item.get("action") or "Try the step and describe what happens.")
        adult_ids = [f"{step_id}-ADULT-{number + 1}" for number in range(len(adult_actions))]
        prompt_ids = [f"{step_id}-PROMPT-{number + 1}" for number in range(len(prompts))]
        action_ids = [f"{step_id}-ACTION-{number + 1}" for number in range(len(participant_actions))]
        observable = str(detail.get("observable") or item.get("signal") or "The participant describes one observable result.")
        core_steps.append({
            "id": step_id, "stage": stage, "actor": item.get("actor") if item.get("actor") in {"adult", "child", "group", "role"} else "group",
            "entry": state_pairs[index][0], "exit": state_pairs[index][1], "minutes": max(1, min(45, int(detail.get("minutes") or max_minutes / len(raw_steps)))),
            "adultActionIds": adult_ids, "promptIds": prompt_ids,
            "participantActions": [{"id": action_id, "audience": "all_participants", "roles": [], "turn": "sequential"} for action_id in action_ids],
            "cycle": [{"action": _stage_action(stage), "audience": "every_active_participant"}],
            "materialIds": material_ids, "hasDecision": bool(detail.get("decision")),
            "cues": [{"id": f"{step_id}-CUE-1", "skill": skills[index % len(skills)]}],
            "visualIds": [], "skills": [skills[index % len(skills)]], "concepts": [concept_id],
        })
        localized: dict[str, Any] = {
            "id": step_id, "title": str(detail.get("title") or f"Step {index + 1}"), "purpose": str(item.get("purpose") or "Make the next change visible."),
            "transition": state_meaning.get(state_pairs[index][1], f"The activity moves to step {index + 2}." if index + 1 < len(raw_steps) else "The activity is ready to close."),
            "instruction": str(detail.get("instruction") or item.get("action") or "Complete this step together."),
            "adultActions": [{"id": value_id, "text": value} for value_id, value in zip(adult_ids, adult_actions, strict=True)],
            "prompts": [{"id": value_id, "text": value} for value_id, value in zip(prompt_ids, prompts, strict=True)],
            "participantActions": [{"id": value_id, "text": value} for value_id, value in zip(action_ids, participant_actions, strict=True)],
            "materialUses": [{"material": value, "purpose": "Use this material for the current action."} for value in material_ids],
            "cues": [{"id": f"{step_id}-CUE-1", "behavior": observable, "doNotInfer": "Do not infer ability, diagnosis, or a stable score from one session."}],
            "result": observable, "success": observable,
            "problems": [{"problem": str(problem.get("problem") or "The step is not working."), "safeResponse": str(problem.get("safeResponse") or "Pause and use only a published option.")} for problem in detail.get("problems") or []],
            "resume": str(detail.get("resume") or "Resume from the start of this step."),
        }
        if detail.get("decision"):
            localized["decision"] = str(detail["decision"])
        if detail.get("warning"):
            localized["warning"] = str(detail["warning"])
        locale_steps.append(localized)

    raw_roles = role_draft.get("roles") or []
    required_role_count = max(sizes)
    while len(raw_roles) < required_role_count:
        number = len(raw_roles) + 1
        raw_roles.append({"id": f"PARTICIPANT-{number}", "name": f"Participant {number}", "levels": levels, "skills": skills_raw, "allowedSteps": [item.get("id") for item in raw_steps], "restrictedSteps": [], "contribution": "Completes the full learning cycle.", "responsibilities": ["Propose, try, observe, improve, and explain."]})
    core_roles, locale_roles = [], []
    role_id_map: dict[str, str] = {}
    for index, item in enumerate(raw_roles[:4]):
        role_id = _id("ROLE", item.get("id") or item.get("name"), str(index + 1))
        role_id_map[str(item.get("id"))] = role_id
        role_skills = [skill_by_raw.get(str(value), _id(f"{primary}-SKL", value, "GENERAL")) for value in item.get("skills") or skills_raw]
        role_skills = [value for value in role_skills if value in skills] or [skills[index % len(skills)]]
        allowed = [_id("STEP", value, "1") for value in item.get("allowedSteps") or []]
        allowed = [value for value in allowed if value in step_ids] or step_ids
        restricted = [_id("STEP", value, "1") for value in item.get("restrictedSteps") or []]
        restricted = [value for value in restricted if value in step_ids]
        core_roles.append({"id": role_id, "levels": [value for value in item.get("levels") or levels if value in {"L1", "L2", "L3", "L4"}] or levels, "primarySkills": role_skills[:1], "skills": role_skills, "concepts": [concept_id], "allowedSteps": allowed, "restrictedSteps": restricted})
        locale_roles.append({"id": role_id, "name": str(item.get("name") or f"Participant {index + 1}"), "contribution": str(item.get("contribution") or "Completes the full learning cycle."), "responsibilities": _strings(item.get("responsibilities") or [], "Propose, try, observe, improve, and explain.")})
    core_groups, locale_groups = [], []
    for size in sizes:
        roles = [row["id"] for row in core_roles[:size]]
        core_groups.append({"size": size, "roles": roles})
        matching = next((item for item in role_draft.get("groups") or [] if item.get("size") == size), {})
        locale_groups.append({"size": size, "notes": str(matching.get("notes") or "Each participant completes an observable part of the cycle.")})

    safety_draft = material_draft.get("safety") or {}
    safety_level = str(safety_draft.get("level") or (idea.get("fit") or {}).get("risk") or brief.get("riskMax") or "B")
    risk_limit = str(brief.get("riskMax") or "B")
    order = {"A": 1, "B": 2, "C": 3, "D": 4}
    if safety_level not in order or order[safety_level] > order.get(risk_limit, 2):
        safety_level = risk_limit if risk_limit in {"A", "B", "C"} else "B"
    hazards_core, hazards_locale = [], []
    for index, item in enumerate(safety_draft.get("hazards") or []):
        hazard_id = _id("HAZ", item.get("id") or item.get("category"), str(index + 1))
        controls = _strings(item.get("controls") or [], "Adult maintains direct supervision.")
        control_ids = [f"{hazard_id}-CONTROL-{number + 1}" for number in range(len(controls))]
        affected = [_id("STEP", value, "1") for value in item.get("stepIds") or []]
        affected = [value for value in affected if value in step_ids] or step_ids
        hazards_core.append({"id": hazard_id, "category": str(item.get("category") or "general"), "controlIds": control_ids, "steps": affected})
        hazards_locale.append({"id": hazard_id, "description": str(item.get("description") or "Adult supervision is required."), "controls": [{"id": control_id, "text": value} for control_id, value in zip(control_ids, controls, strict=True)]})
    stop_text = _strings(safety_draft.get("stops") or idea.get("safety") or [], "Stop immediately if the adult cannot maintain the stated controls.")[:6]
    stop_ids = [f"STOP-{index + 1}" for index in range(len(stop_text))]
    prohibited_text = [str(value) for value in safety_draft.get("prohibited") or []]
    prohibited_ids = [f"PROHIBITED-{index + 1}" for index in range(len(prohibited_text))]

    adaptations_core, adaptations_locale = [], []
    for index, item in enumerate(role_draft.get("adaptations") or []):
        adaptation_id = _id(f"{activity_id}-ADAPT", item.get("id") or item.get("name"), str(index + 1))
        safety = item.get("safety") if item.get("safety") in {"none", "reviewed"} else "reviewed"
        adult_confirm = bool(item.get("adultConfirm", True)) or safety != "none"
        adaptations_core.append({"id": adaptation_id, "type": item.get("type") if item.get("type") in {"presentation", "difficulty", "role", "material", "duration", "simplification", "extension"} else "presentation", "safety": safety, "adultConfirm": adult_confirm})
        adaptations_locale.append({"id": adaptation_id, "name": str(item.get("name") or "Published option"), "conditions": str(item.get("conditions") or "Use when the adult confirms it fits the current session."), "changes": str(item.get("changes") or "Changes presentation only; safety limits remain unchanged.")})

    close_items = close_draft.get("items") or []
    if not close_items:
        close_items = [{"skill": skills_raw[0], "question": "What did you notice?", "evidence": ["Names one observable result."], "nonEvidence": ["A guessed trait or score."], "external": []}]
    core_close, locale_close = [], []
    for item in close_items[:4]:
        skill = skill_by_raw.get(str(item.get("skill")), skills[0])
        core_close.append({"skill": skill})
        locale_close.append({"skill": skill, "question": str(item.get("question") or "What did you notice?"), "evidence": _strings(item.get("evidence") or [], "Names one observable result."), "nonEvidence": _strings(item.get("nonEvidence") or [], "A guessed trait, diagnosis, or score."), "external": [str(value) for value in item.get("external") or []]})

    core = {
        "schema": "activity@2", "id": activity_id, "version": version, "sourceLocale": "en-US", "state": "review",
        "fit": {"age": age, "levels": levels, "group": {"min": min(sizes), "max": max(sizes), "sizes": sizes}, "time": {"min": min_minutes, "max": max_minutes, "prep": 5, "clean": 5}, "mess": "low", "spaces": ["table_or_floor"], "offline": True},
        "learn": {"primary": primary, "secondary": [], "concepts": [concept_id], "skills": skills, "cycle": list(dict.fromkeys(item["stage"] for item in core_steps if item["stage"] in {"discover", "imagine", "build_or_do", "experiment", "improve", "explain"})) or ["discover", "explain"], "guidance": [{"skill": skill, "age": age, "intent": "exploration"} for skill in skills]},
        "materials": materials_core,
        "flow": {"mode": "hybrid" if max(sizes) > 1 else "individual_cycles", "start": state_pairs[0][0], "end": state_pairs[-1][1], "states": states, "materialFunctions": [{"material": item["id"], "firstStep": next((step["id"] for step in core_steps if item["id"] in step["materialIds"]), step_ids[0])} for item in materials_core], "participantCycle": {"policy": "every_active_participant", "actions": list(dict.fromkeys(action["action"] for step in core_steps for action in step["cycle"]))}, "roles": core_roles, "groups": core_groups, "steps": core_steps},
        "safety": {"level": safety_level, "hazards": hazards_core, "adultOnlySteps": [], "stopIds": stop_ids, "prohibitedIds": prohibited_ids},
        "adaptations": adaptations_core,
        "closeout": core_close,
    }

    method = str(plan.get("method") or mechanism)
    locale = {
        "schema": "activity-locale@2", "activityId": activity_id, "version": version, "locale": "en-US",
        "content": {"title": str(idea.get("title") or "Learning investigation"), "summary": str(idea.get("promise") or plan.get("goal") or "Explore a question together."), "openingQuestion": "What do you think will happen, and why?", "adultBrief": str(plan.get("goal") or "Support one observable learning objective."), "adultDetail": method, "childExplanation": method, "reflections": [item["question"] for item in locale_close]},
        "learn": {"goal": str(plan.get("goal") or "Complete the cycle and explain one observable result."), "method": method, "concepts": [{"id": concept_id, "name": mechanism}], "skills": [{"id": skill, "name": raw, "evidence": [next((step["success"] for step in locale_steps if skill in core_steps[locale_steps.index(step)]["skills"]), "Names one observable result.")], "nonEvidence": ["A guessed trait, diagnosis, or stable score."]} for raw, skill in zip(skills_raw, skills, strict=True)], "decisions": [step["decision"] for step in locale_steps if step.get("decision")], "lookFors": ["Observe actions and support needed without scoring the child."], "guidance": [{"skill": skill, "rationale": "This session offers an observable opportunity to practice the skill.", "simplify": "Reduce choices or adult language without changing the safety controls.", "extend": "Ask for an explanation using another observation."} for skill in skills]},
        "materials": materials_locale,
        "flow": {"states": [{"id": state, "text": state_meaning.get(state, state.replace("STATE-", "").replace("-", " ").title())} for state in states], "materialFunctions": [{"material": item["id"], "purpose": "Supports the observable activity mechanism."} for item in materials_core], "roles": locale_roles, "groups": locale_groups, "steps": locale_steps},
        "safety": {"supervision": str(safety_draft.get("supervision") or "An adult stays present and controls setup, materials, and stopping."), "hazards": hazards_locale, "stops": [{"id": value_id, "text": value} for value_id, value in zip(stop_ids, stop_text, strict=True)], "prohibited": [{"id": value_id, "text": value} for value_id, value in zip(prohibited_ids, prohibited_text, strict=True)], "cleanup": str(safety_draft.get("cleanup") or "The adult counts, stores, and disposes of materials safely.")},
        "adaptations": adaptations_locale,
        "closeout": locale_close,
        "visuals": [],
    }
    return core, locale


def translatable_items(locale: dict[str, Any]) -> list[dict[str, str]]:
    skip = {"schema", "activityId", "version", "locale", "id", "skill", "material"}
    result: list[dict[str, str]] = []

    def visit(value: Any, path: str = "") -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                child_path = f"{path}.{key}" if path else key
                if isinstance(child, str) and key not in skip:
                    result.append({"key": child_path, "text": child})
                elif not isinstance(child, str):
                    visit(child, child_path)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                visit(child, f"{path}[{index}]")
        elif isinstance(value, str):
            result.append({"key": path, "text": value})

    visit(locale)
    return result


def apply_translations(source: dict[str, Any], target_locale: str, items: list[dict[str, str]]) -> dict[str, Any]:
    target = deepcopy(source)
    target["locale"] = target_locale
    expected = {item["key"] for item in translatable_items(source)}
    supplied = {item.get("key") for item in items}
    if supplied != expected:
        raise ValueError("Localization did not preserve the exact field set")
    for item in items:
        tokens = re.findall(r"([^.[\]]+)|\[(\d+)\]", item["key"])
        cursor: Any = target
        for index, (name, array_index) in enumerate(tokens):
            key: Any = int(array_index) if array_index else name
            if index == len(tokens) - 1:
                cursor[key] = item["text"]
            else:
                cursor = cursor[key]
    return target


def compile_bundle(job: dict[str, Any]) -> dict[str, Any]:
    core, english = build_source_locale(job)
    localized = _artifact(job, "localize", "locales")
    spanish = localized.get("es-US") if isinstance(localized, dict) else None
    if not isinstance(spanish, dict):
        raise ValueError("Both locale contracts must be generated before compilation")
    locales = {"en-US": english, "es-US": spanish}
    canonical = json.dumps({"core": core, "locales": locales}, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    content_hash = f"sha256:{hashlib.sha256(canonical.encode('utf-8')).hexdigest()}"
    version_id = f"{core['id']}@{core['version']}"
    blocks: dict[str, list[dict[str, Any]]] = {}
    chunks: list[dict[str, Any]] = []
    for locale_name, copy in locales.items():
        items: list[dict[str, Any]] = [
            {"id": "PREP-01", "kind": "prep", "version": 1, "required": True, "data": {"title": copy["content"]["title"], "text": copy["content"]["adultBrief"]}},
            {"id": "PURPOSE-01", "kind": "purpose", "version": 1, "required": True, "data": {"title": copy["learn"]["goal"], "text": copy["learn"]["method"]}},
            {"id": "SAFETY-01", "kind": "safety", "version": 1, "required": True, "data": {"title": "Safety" if locale_name == "en-US" else "Seguridad", "text": " ".join([copy["safety"]["supervision"], *[item["text"] for item in copy["safety"]["stops"]]])}},
        ]
        for index, step in enumerate(copy["flow"]["steps"]):
            prompt = step["prompts"][0]["text"] if step["prompts"] else ""
            text = f"{step['instruction']} {prompt}".strip()
            items.append({"id": f"BLOCK-{index + 1:02d}", "kind": "instruction", "version": 1, "required": True, "data": {"eyebrow": f"{index + 1}/{len(copy['flow']['steps'])}", "title": step["title"], "text": text}})
        items.append({"id": "CLOSEOUT-01", "kind": "closeout", "version": 1, "required": True, "data": {"title": "Close together" if locale_name == "en-US" else "Cierren juntos", "text": copy["closeout"][0]["question"]}})
        blocks[locale_name] = items
        chunks.append({"chunkId": f"{version_id}:{locale_name}:overview", "locale": locale_name, "type": "overview", "step": None, "label": copy["content"]["title"], "content": " ".join([copy["content"]["summary"], copy["learn"]["goal"], copy["learn"]["method"]])})
        chunks.append({"chunkId": f"{version_id}:{locale_name}:safety", "locale": locale_name, "type": "safety", "step": None, "label": "Safety", "content": " ".join([copy["safety"]["supervision"], *[item["text"] for item in copy["safety"]["stops"]], *[item["text"] for item in copy["safety"]["prohibited"]]])})
        for index, step in enumerate(copy["flow"]["steps"]):
            chunks.append({"chunkId": f"{version_id}:{locale_name}:step-{index + 1:02d}", "locale": locale_name, "type": "step", "step": step["id"], "label": step["title"], "content": " ".join([step["purpose"], step["instruction"], *[item["text"] for item in step["prompts"]], step["success"], *[item["safeResponse"] for item in step["problems"]]])})
        for index, adaptation in enumerate(copy["adaptations"]):
            chunks.append({"chunkId": f"{version_id}:{locale_name}:adapt-{index + 1:02d}", "locale": locale_name, "type": "adaptation", "step": None, "label": adaptation["name"], "content": f"{adaptation['conditions']} {adaptation['changes']}"})
    bundle = {"activityId": core["id"], "activityVersionId": version_id, "version": core["version"], "contentHash": content_hash, "core": core, "locales": locales, "blocks": blocks, "chunks": chunks}
    validate_bundle(bundle)
    return bundle


def validate_bundle(bundle: dict[str, Any]) -> None:
    """Enforce the cross-reference invariants JSON Schema cannot express."""

    core = bundle["core"]
    if core.get("schema") != "activity@2" or core.get("state") != "review":
        raise ValueError("Compiled core must be an Activity V2 review draft")
    if core["safety"]["level"] == "D":
        raise ValueError("Risk D is outside the product scope")
    steps = core["flow"]["steps"]
    step_ids = [item["id"] for item in steps]
    if len(step_ids) != len(set(step_ids)) or len(steps) < 2:
        raise ValueError("Compiled steps must have unique identifiers")
    if steps[0]["entry"] != core["flow"]["start"] or steps[-1]["exit"] != core["flow"]["end"]:
        raise ValueError("Compiled flow boundaries are inconsistent")
    for previous, current in zip(steps, steps[1:], strict=False):
        if previous["exit"] != current["entry"]:
            raise ValueError("Compiled flow is not causally continuous")
    material_ids = {item["id"] for item in core["materials"]}
    role_ids = {item["id"] for item in core["flow"]["roles"]}
    skill_ids = set(core["learn"]["skills"])
    for step in steps:
        if not set(step["materialIds"]).issubset(material_ids):
            raise ValueError("A step references an unknown material")
        if any(cue["skill"] not in skill_ids for cue in step["cues"]):
            raise ValueError("A step references an unknown skill")
    for group in core["flow"]["groups"]:
        if len(group["roles"]) != group["size"] or not set(group["roles"]).issubset(role_ids):
            raise ValueError("A group configuration has invalid role slots")
    for hazard in core["safety"]["hazards"]:
        if not hazard["controlIds"] or not set(hazard["steps"]).issubset(set(step_ids)):
            raise ValueError("A hazard lacks a valid control or affected step")
    for adaptation in core["adaptations"]:
        if adaptation["safety"] != "none" and not adaptation["adultConfirm"]:
            raise ValueError("Safety-changing adaptations require adult confirmation")
    if set(bundle["locales"]) != {"en-US", "es-US"}:
        raise ValueError("Both required locale contracts must be present")
    for locale_name, locale in bundle["locales"].items():
        if locale.get("locale") != locale_name or locale.get("activityId") != core["id"] or locale.get("version") != core["version"]:
            raise ValueError("Localized contract identity does not match the core")
        locale_step_ids = {item["id"] for item in locale["flow"]["steps"]}
        if locale_step_ids != set(step_ids):
            raise ValueError("Localized steps do not match the core")
        if len(json.dumps(bundle["blocks"][locale_name], ensure_ascii=False).encode("utf-8")) > 64 * 1024:
            raise ValueError("Compiled family blocks exceed the delivery budget")
