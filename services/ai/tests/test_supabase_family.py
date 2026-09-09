from datetime import timedelta
from types import SimpleNamespace
import unittest
from uuid import uuid4

from services.ai.kids_ai.family import FamilySetup
from services.ai.kids_ai.models import Principal
from services.ai.kids_ai.supabase_family import SupabaseFamilyService, now_utc


def service() -> SupabaseFamilyService:
    return SupabaseFamilyService(SimpleNamespace(
        supabase_url="https://example.supabase.co",
        supabase_publishable_key="publishable",
        supabase_secret_key="service-secret",
        adult_gate_signing_secret="a-long-independent-signing-secret",
        legal_matrix_version="pilot-us-v1",
    ))


class SupabaseFamilyTests(unittest.TestCase):
    def test_gate_token_is_bound_to_user_family_and_expiry(self):
        adapter = service()
        user_id, family_id, gate_id = uuid4(), uuid4(), uuid4()
        principal = Principal(user_id=user_id)
        token = adapter._issue_gate_token(gate_id, user_id, family_id, now_utc() + timedelta(minutes=15))
        self.assertEqual(adapter._verify_gate_token(token, principal, family_id), gate_id)
        with self.assertRaises(PermissionError):
            adapter._verify_gate_token(token + "tampered", principal, family_id)
        with self.assertRaises(PermissionError):
            adapter._verify_gate_token(token, Principal(user_id=uuid4()), family_id)
        expired = adapter._issue_gate_token(gate_id, user_id, family_id, now_utc() - timedelta(seconds=1))
        with self.assertRaises(PermissionError):
            adapter._verify_gate_token(expired, principal, family_id)

    def test_gate_answer_hash_is_context_bound(self):
        adapter = service()
        user_id, family_id, gate_id = uuid4(), uuid4(), uuid4()
        expected = adapter._challenge_hash(gate_id, user_id, family_id, [2, 4, 6])
        self.assertNotEqual(expected, adapter._challenge_hash(gate_id, user_id, family_id, [2, 4, 7]))
        self.assertNotEqual(expected, adapter._challenge_hash(gate_id, uuid4(), family_id, [2, 4, 6]))

    def test_learner_validation_rejects_pii_and_duplicate_aliases(self):
        adapter = service()
        valid = FamilySetup(locale="en-US", timezone="America/New_York", learnerAliases=["Explorer"], ageBands=["5-6"])
        self.assertEqual(adapter._validate_learners(valid)[0]["alias"], "Explorer")
        duplicate = FamilySetup(locale="en-US", timezone="America/New_York", learnerAliases=["Explorer", "explorer"], ageBands=["5-6", "7-8"])
        with self.assertRaises(ValueError):
            adapter._validate_learners(duplicate)
        email = FamilySetup(locale="en-US", timezone="America/New_York", learnerAliases=["child@example.com"], ageBands=["5-6"])
        with self.assertRaises(ValueError):
            adapter._validate_learners(email)

    def test_feedback_redaction_never_keeps_contact_values(self):
        value = SupabaseFamilyService._redact("Write parent@example.com or +1 555 555 1212")
        self.assertNotIn("parent@example.com", value)
        self.assertNotIn("555 555 1212", value)


if __name__ == "__main__":
    unittest.main()
