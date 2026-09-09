import unittest

from services.ai.kids_ai.editorial_compile import apply_translations, build_source_locale, compile_bundle, translatable_items



class EditorialCompileTests(unittest.TestCase):
    def fixture(self):
        return {
            "jobId": "12345678-1234-1234-1234-123456789012",
            "brief": {"primaryArea": "engineering", "ageBand": "5-6", "participants": {"min": 1, "max": 2}, "time": {"min": 20, "max": 30}, "riskMax": "B"},
            "artifacts": {
                "idea": {"ideaBrief": {"title": "Build a paper ramp", "promise": "Compare two shapes through an observable test.", "fit": {"age": [5, 6], "group": [1, 2], "minutes": 25, "risk": "A"}, "area": "ENG", "mechanism": "shape changes motion", "materials": ["paper"], "safety": ["Stop if material is damaged."], "sourceRefs": ["source-1"]}},
                "core": {"corePlan": {"goal": "Compare two paper shapes in the same test.", "method": "Change one shape and observe the result.", "skills": ["compare results"], "states": [{"id": "ready", "meaning": "Materials are ready."}, {"id": "tested", "meaning": "The result is visible."}, {"id": "closed", "meaning": "The result was explained."}], "steps": [{"id": "one", "entry": "ready", "exit": "tested", "actor": "group", "action": "Build and test one shape.", "purpose": "Make one result visible.", "signal": "Each child names what moved."}, {"id": "two", "entry": "tested", "exit": "closed", "actor": "group", "action": "Compare and explain.", "purpose": "Connect evidence to a change.", "signal": "Each child names one difference."}], "risks": []}},
                "materials_safety": {"draft": {"materials": [{"id": "paper", "name": "Paper", "quantity": 2, "unit": "sheet", "required": True, "reusable": False, "prep": "Use clean sheets.", "safety": "Stop for a paper cut.", "substitutes": []}], "safety": {"level": "A", "supervision": "An adult remains present.", "hazards": [], "stops": ["Stop if anyone feels unsafe."], "prohibited": ["Do not use sharp tools."], "cleanup": "Count and recycle paper."}}},
                "steps": {"draft": {"steps": [{"id": "one", "stage": "build_or_do", "minutes": 12, "title": "Build", "instruction": "Fold one sheet and test it.", "adultActions": ["Stabilize the surface."], "prompts": ["What moved?"], "participantActions": ["Fold and test."], "materialIds": ["paper"], "observable": "Names what moved.", "problems": [], "resume": "Restart the test."}, {"id": "two", "stage": "explain", "minutes": 8, "title": "Compare", "instruction": "Compare both results.", "adultActions": ["Listen without scoring."], "prompts": ["What changed?"], "participantActions": ["Explain one difference."], "materialIds": ["paper"], "decision": "Choose one shape to try next.", "observable": "Names one difference.", "problems": [], "resume": "Return to the comparison."}]}},
                "roles_adaptations": {"draft": {"roles": [{"id": "builder", "name": "Builder", "levels": ["L1", "L2"], "skills": ["compare results"], "allowedSteps": ["one", "two"], "restrictedSteps": [], "contribution": "Completes a full test.", "responsibilities": ["Build, test, and explain."]}], "groups": [{"size": 1, "roles": ["builder"], "notes": "One child completes the cycle."}, {"size": 2, "roles": ["builder", "builder"], "notes": "Both children complete the cycle."}], "adaptations": [{"id": "short", "type": "duration", "safety": "none", "adultConfirm": False, "name": "Short version", "conditions": "Use when time is limited.", "changes": "Complete one comparison instead of two."}]}},
                "closeout": {"draft": {"items": [{"skill": "compare results", "question": "What changed the result?", "evidence": ["Names one observed difference."], "nonEvidence": ["A guessed score."], "external": []}], "targetSeconds": 20}},
            },
        }

    def test_compiler_preserves_identity_references_and_safety(self):
        job = self.fixture()
        _, english = build_source_locale(job)
        translations = [{"key": item["key"], "text": f"ES: {item['text']}"} for item in translatable_items(english)]
        job["artifacts"]["localize"] = {"locales": {"en-US": english, "es-US": apply_translations(english, "es-US", translations)}}
        bundle = compile_bundle(job)
        self.assertEqual(set(bundle["locales"]), {"en-US", "es-US"})
        self.assertEqual(bundle["core"]["safety"]["level"], "A")
        self.assertTrue(bundle["contentHash"].startswith("sha256:"))
        self.assertTrue(all(block["version"] == 1 for block in bundle["blocks"]["es-US"]))
        self.assertTrue(all(adaptation["adultConfirm"] for adaptation in bundle["core"]["adaptations"] if adaptation["safety"] != "none"))


if __name__ == "__main__":
    unittest.main()
