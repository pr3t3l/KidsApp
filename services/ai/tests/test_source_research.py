import unittest
from unittest.mock import patch

from services.ai.kids_ai.source_research import SourceResearchService


class FakeResponse:
    status_code = 200

    def raise_for_status(self):
        return None

    def json(self):
        return {"web": {"results": [
            {"url": "https://www.nasa.gov/learning/example", "title": "NASA learning", "description": "Public example"},
            {"url": "https://unapproved.example/activity", "title": "Rejected"},
        ]}}


class FakeClient:
    headers = None
    params = None

    def __init__(self, *args, **kwargs):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_args):
        return False

    async def get(self, url, headers=None, params=None):
        type(self).headers = headers
        type(self).params = params
        return FakeResponse()


class SourceResearchTests(unittest.IsolatedAsyncioTestCase):
    async def test_search_is_transient_allowlisted_and_does_not_claim_rights(self):
        service = SourceResearchService("brave-key", ("nasa.gov",))
        with patch("services.ai.kids_ai.source_research.httpx.AsyncClient", FakeClient):
            result = await service.search("bridge activity", "en-US")
        self.assertEqual(len(result["results"]), 1)
        self.assertTrue(result["results"][0]["transient"])
        self.assertFalse(result["results"][0]["licenseVerified"])
        self.assertIn("site:nasa.gov", FakeClient.params["q"])
        self.assertEqual(FakeClient.params["safesearch"], "strict")
        self.assertNotEqual(FakeClient.headers["X-Subscription-Token"], "")

    async def test_unapproved_requested_domain_fails_before_network(self):
        service = SourceResearchService("brave-key", ("nasa.gov",))
        with self.assertRaises(PermissionError):
            await service.search("bridge activity", "en-US", ["example.com"])


if __name__ == "__main__":
    unittest.main()
