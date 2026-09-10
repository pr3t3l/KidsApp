import unittest

from services.ai.kids_ai.supabase_http import supabase_headers


class SupabaseHeaderTests(unittest.TestCase):
    def test_new_secret_key_is_not_misrepresented_as_a_jwt(self):
        headers = supabase_headers("sb_secret_example")
        self.assertEqual(headers["apikey"], "sb_secret_example")
        self.assertNotIn("Authorization", headers)

    def test_legacy_service_role_key_keeps_bearer_compatibility(self):
        headers = supabase_headers("eyJlegacy-service-role")
        self.assertEqual(headers["Authorization"], "Bearer eyJlegacy-service-role")

    def test_user_jwt_is_used_with_the_publishable_key(self):
        headers = supabase_headers("sb_publishable_example", "eyJadult-session")
        self.assertEqual(headers["apikey"], "sb_publishable_example")
        self.assertEqual(headers["Authorization"], "Bearer eyJadult-session")


if __name__ == "__main__":
    unittest.main()
