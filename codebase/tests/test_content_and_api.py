import unittest
from unittest.mock import patch

import httpx2
from openai import APITimeoutError

from app import app
from failfirst.content import repository


class ContentAndApiTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_public_lesson_has_three_ordered_exercises_without_answers(self):
        data = self.client.get("/api/lessons/token-foundations").get_json()
        self.assertEqual(3, len(data["exercises"]))
        self.assertEqual("token-default", data["exercises"][0]["exercise_id"])
        for exercise in data["exercises"]:
            self.assertNotIn("answer", exercise)
            self.assertNotIn("source_refs", exercise)
            self.assertIn("encoding", exercise)

    def test_legacy_exercise_api_keeps_its_schema(self):
        response = self.client.get("/api/bai-tap")
        self.assertEqual(200, response.status_code)
        self.assertEqual({"doan_van", "n_tieng"}, set(response.get_json()))

    def test_health_distinguishes_configuration_from_verified_connection(self):
        data = self.client.get("/api/health").get_json()
        self.assertIn("app_version", data)
        self.assertIn("configured", data)
        self.assertFalse(data["verified"])

        with patch("app.kiem_tra_ket_noi", return_value={
            "ok": True, "model": "fake-model", "ms": 12,
            "tokens_in": 5, "tokens_out": 3, "request_id": "req_test",
        }):
            live = self.client.post("/api/health/ai", json={})
        self.assertEqual(200, live.status_code)
        self.assertTrue(live.get_json()["verified"])

    def test_openai_timeout_is_returned_as_actionable_json(self):
        error = APITimeoutError(request=httpx2.Request("POST", "https://api.openai.com/v1/chat/completions"))
        with patch("app.chan_doan", side_effect=error):
            response = self.client.post("/api/chan-doan", json={"so": 99, "ly_do": "mỗi tiếng một token"})
        self.assertEqual(504, response.status_code)
        self.assertEqual("OPENAI_TIMEOUT", response.get_json()["error"]["code"])

    def test_new_unlock_flow_rejects_missing_explanation_proof(self):
        response = self.client.post("/api/mo-khoa", json={"exercise_id": "token-default"})
        self.assertEqual(403, response.status_code)

    def test_manifest_quotes_exist_and_retrieval_stays_in_exercise_allowlist(self):
        exercise = repository.get_exercise("token-mixed-language")
        results = repository.retrieve("token-mixed-language", "tokenizer và ngôn ngữ", top_k=3)
        self.assertTrue(results)
        self.assertTrue({x["source_id"] for x in results}.issubset(set(exercise["source_refs"])))
        for source in results:
            self.assertTrue(source["document_id"])
            self.assertTrue(source["document_name"])
            self.assertTrue(source["lesson_id"])
            self.assertTrue(source["section"] or source["page"])
            self.assertTrue(source["quote"])


if __name__ == "__main__":
    unittest.main()
