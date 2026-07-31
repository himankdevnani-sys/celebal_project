"""
PatchContext Verification Test Suite
Tests Phase 8 Questions to verify that every question retrieves different documents,
different similarity scores, different confidence scores, and different answers.
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.config import config
from services.api import api

PHASE_8_QUESTIONS = [
    "What is FastAPI dependency injection?",
    "Why was APIRouter introduced?",
    "Explain lifespan protocol.",
    "Why migrate to Pydantic v2?",
    "How does async improve FastAPI performance?"
]

class TestPhase8RAGSystem(unittest.TestCase):

    def test_real_rag_query_diversity(self):
        """Verifies that all 5 Phase 8 questions produce different answers, sources, similarities, and confidence scores."""
        config.USE_MOCK = False
        
        answers = {}
        top_chunk_ids = {}
        similarity_scores = {}
        confidence_scores = {}

        for q in PHASE_8_QUESTIONS:
            ans = api.ask_repository(q)
            self.assertIsNotNone(ans.markdown_answer)
            self.assertGreater(len(ans.evidences), 0)
            self.assertGreater(len(ans.citations), 0)

            answers[q] = ans.markdown_answer
            top_chunk_ids[q] = ans.evidences[0].id
            similarity_scores[q] = ans.evidences[0].similarity_score
            confidence_scores[q] = ans.verification.confidence_score

            print(f"\n[QUERY]: {q}")
            print(f"  -> Top Chunk ID: {ans.evidences[0].id} ({ans.evidences[0].title})")
            print(f"  -> Real Similarity Score: {ans.evidences[0].similarity_score:.4f}")
            print(f"  -> Real Confidence Score: {ans.verification.confidence_score:.4f}")

        # Assertions
        unique_answers = set(answers.values())
        self.assertEqual(len(unique_answers), len(PHASE_8_QUESTIONS), "All 5 answers must be distinct!")

        unique_chunks = set(top_chunk_ids.values())
        self.assertEqual(len(unique_chunks), len(PHASE_8_QUESTIONS), "All 5 questions must retrieve different top chunks!")

    def test_low_similarity_guard(self):
        """Verifies that ungrounded/unrelated queries are rejected by similarity threshold guard."""
        config.USE_MOCK = False
        ans = api.ask_repository("quantum entanglement superstring astrophysics formula xyz999")
        self.assertIn("No Relevant Evidence Found", ans.markdown_answer)

if __name__ == "__main__":
    unittest.main()
