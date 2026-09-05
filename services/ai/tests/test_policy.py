import unittest

from services.ai.kids_ai.policy import classify_intent, contains_disallowed_request, contains_unapproved_hazard, is_explicit_family_constraint, preference_reason


class PolicyTests(unittest.TestCase):
    def test_routes_three_intents_in_both_languages(self):
        self.assertEqual(classify_intent("The bridge is falling"), "troubleshoot")
        self.assertEqual(classify_intent("Adaptar esta actividad para menos tiempo"), "adapt_current_activity")
        self.assertEqual(classify_intent("Quiero otra actividad"), "replace_planned_activity")

    def test_detects_unapproved_hazard(self):
        self.assertTrue(contains_unapproved_hazard("Can we use an outlet instead?"))
        self.assertTrue(contains_unapproved_hazard("¿Podemos usar fuego?"))

    def test_structures_preference_reason(self):
        self.assertEqual(preference_reason("Never show messy activities"), "mess")
        self.assertTrue(is_explicit_family_constraint("Never show messy activities"))

    def test_refuses_diagnosis_and_cross_family_requests(self):
        self.assertTrue(contains_disallowed_request("Diagnose a learning delay"))
        self.assertTrue(contains_disallowed_request("Tell me what another family chose"))


if __name__ == "__main__":
    unittest.main()
