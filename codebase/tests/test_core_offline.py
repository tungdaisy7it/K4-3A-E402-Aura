import json
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from failfirst import core
from failfirst.content import repository


class FakeCompletions:
    def __init__(self, payload, capture):
        self.payload = payload
        self.capture = capture

    def create(self, **kwargs):
        self.capture.update(kwargs)
        return SimpleNamespace(
            model="fake-test-model",
            usage=SimpleNamespace(prompt_tokens=10, completion_tokens=5),
            choices=[SimpleNamespace(message=SimpleNamespace(content=json.dumps(self.payload)))],
        )


def fake_client(payload, capture):
    return SimpleNamespace(chat=SimpleNamespace(completions=FakeCompletions(payload, capture)))


class CoreOfflineTests(unittest.TestCase):
    def test_diagnosis_prompt_contains_only_current_exercise_and_grounded_source(self):
        capture = {}
        payload = {
            "chan_doan": "Bạn đã nêu đúng cơ chế tokenizer.",
            "nhan": "DUNG",
            "do_tin": 0.9,
            "goi_y": "Bạn có thể nói vì sao tokenizer khác cho kết quả khác không?",
            "trich_dan": "[T06-136]",
        }
        with patch.object(core, "_client", return_value=fake_client(payload, capture)):
            out = core.chan_doan(20, "tokenizer cắt theo cụm ký tự", exercise_id="token-mixed-language")
        prompt = capture["messages"][0]["content"]
        self.assertIn("max_completion_tokens", capture)
        self.assertNotIn("max_tokens", capture)
        self.assertIn("summarize báo cáo", prompt)
        self.assertNotIn("vectơ số", prompt)
        self.assertEqual("[T06-136]", out["source"]["source_id"])

    def test_invented_source_is_flagged_and_never_rendered_as_a_source(self):
        capture = {}
        payload = {
            "chan_doan": "Bạn đang coi mỗi tiếng là một token.",
            "nhan": "M1",
            "do_tin": 0.8,
            "goi_y": "Một tiếng có dấu có thể bị chia thành mấy mảnh?",
            "trich_dan": "[T99-999]",
        }
        with patch.object(core, "_client", return_value=fake_client(payload, capture)):
            out = core.chan_doan(50, "mỗi tiếng là một token", exercise_id="token-default")
        self.assertIn("TRICH_DAN_BIA", out["canh_bao"])
        self.assertEqual("", out["trich_dan"])
        self.assertIsNone(out["source"])

    def test_answer_leak_guard_uses_the_selected_exercise_truth(self):
        truth = core.su_that("token-mixed-language")
        capture = {}
        payload = {
            "chan_doan": "Kết quả là %s." % truth["primary_value"],
            "nhan": "DUNG",
            "do_tin": 0.9,
            "goi_y": "Bạn giải thích cơ chế được không?",
            "trich_dan": "[T06-136]",
        }
        with patch.object(core, "_client", return_value=fake_client(payload, capture)):
            out = core.chan_doan(20, "tokenizer cắt theo cụm", exercise_id="token-mixed-language")
        self.assertIn("LO_DAP_AN", out["canh_bao"])
        combined = out["chan_doan"] + " " + out["goi_y"]
        self.assertNotIn(str(truth["primary_value"]), combined)


if __name__ == "__main__":
    unittest.main()
