# -*- coding: utf-8 -*-
"""Kho lesson/exercise và retrieval nhỏ, không phụ thuộc framework hay vector DB."""
from __future__ import annotations

import json
import os
import re
import unicodedata
from copy import deepcopy


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_ROOT = os.path.join(ROOT, "content")
LESSON_PATH = os.path.join(CONTENT_ROOT, "lessons", "token-foundations.json")
MANIFEST_PATH = os.path.join(CONTENT_ROOT, "documents", "manifest.json")


def _tokens(text: str) -> set[str]:
    folded = unicodedata.normalize("NFD", (text or "").lower())
    folded = "".join(ch for ch in folded if unicodedata.category(ch) != "Mn")
    return {x for x in re.findall(r"[a-z0-9_]+", folded) if len(x) > 1}


class ContentRepository:
    def __init__(self, lesson_path: str = LESSON_PATH, manifest_path: str = MANIFEST_PATH):
        with open(lesson_path, encoding="utf-8") as f:
            self.lesson = json.load(f)
        with open(manifest_path, encoding="utf-8") as f:
            manifest = json.load(f)

        self.exercises = {x["exercise_id"]: x for x in self.lesson["exercises"]}
        self.sources = {}
        document_dir = os.path.dirname(manifest_path)
        for document in manifest["documents"]:
            path = os.path.join(document_dir, document["path"])
            with open(path, encoding="utf-8") as f:
                body = f.read()
            for source in document["sources"]:
                if source["quote"] not in body:
                    raise ValueError("Trích dẫn %s không tồn tại trong %s" % (source["source_id"], path))
                item = deepcopy(source)
                item.update({
                    "document_id": document["document_id"],
                    "document_name": document["document_name"],
                    "lesson_id": document["lesson_id"],
                    "lesson_name": self.lesson["lesson_name"],
                })
                if item["source_id"] in self.sources:
                    raise ValueError("source_id trùng: %s" % item["source_id"])
                self.sources[item["source_id"]] = item

        for exercise in self.exercises.values():
            missing = set(exercise["source_refs"]) - set(self.sources)
            if missing:
                raise ValueError("Exercise %s tham chiếu nguồn thiếu: %s" %
                                 (exercise["exercise_id"], ", ".join(sorted(missing))))

    @property
    def default_exercise_id(self) -> str:
        return self.lesson["exercises"][0]["exercise_id"]

    def get_exercise(self, exercise_id: str | None = None) -> dict:
        key = exercise_id or self.default_exercise_id
        if key not in self.exercises:
            raise KeyError("Không có exercise_id: %s" % key)
        return deepcopy(self.exercises[key])

    def public_lesson(self) -> dict:
        return {
            "lesson_id": self.lesson["lesson_id"],
            "lesson_name": self.lesson["lesson_name"],
            "title": self.lesson["title"],
            "exercises": [self.public_exercise(x["exercise_id"]) for x in self.lesson["exercises"]],
        }

    def public_exercise(self, exercise_id: str) -> dict:
        exercise = self.get_exercise(exercise_id)
        exercise["encoding"] = exercise["answer"]["encoding"]
        exercise.pop("answer", None)
        exercise.pop("expected_errors", None)
        exercise.pop("source_refs", None)
        exercise["n_tieng"] = len(exercise["content"].split())
        return exercise

    def retrieve(self, exercise_id: str, query: str, top_k: int = 2) -> list[dict]:
        exercise = self.get_exercise(exercise_id)
        query_terms = _tokens(query + " " + exercise["question"] + " " + exercise["content"])
        ranked = []
        for order, source_id in enumerate(exercise["source_refs"]):
            source = self.sources[source_id]
            haystack = _tokens(source["section"] + " " + source["quote"])
            overlap = len(query_terms & haystack)
            # source_refs là allowlist biên tập theo từng exercise; overlap chỉ xếp hạng trong allowlist.
            ranked.append((overlap, -order, source))
        ranked.sort(key=lambda row: (row[0], row[1]), reverse=True)
        return [deepcopy(row[2]) for row in ranked[:max(0, top_k)] if row[0] > 0]

    def source(self, source_id: str) -> dict | None:
        item = self.sources.get(source_id)
        return deepcopy(item) if item else None


repository = ContentRepository()
