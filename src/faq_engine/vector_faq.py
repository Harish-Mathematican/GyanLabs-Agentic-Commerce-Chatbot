"""
#Gyan Labs - Vector FAQ Search & Grounding Engine
=================================================
Indexes enterprise FAQ documents and performs semantic cosine similarity search
to answer warranty, shipping, SLA, and procurement questions instantly.
"""

from typing import List, Dict, Any, Tuple, Optional
import csv
import math
import os
import re
from pathlib import Path
from collections import Counter
from src.config import FAQ_CSV_PATH, GROQ_API_KEY, DEFAULT_LLM_MODEL


def cosine_sim(vec_a: List[float], vec_b: List[float]) -> float:
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return max(0.0, min(1.0, dot / (norm_a * norm_b)))


class DenseVectorEngine:
    def __init__(self, dim: int = 256):
        self.dim = dim

    def vectorize(self, text: str) -> List[float]:
        words = re.findall(r"\b[a-zA-Z0-9_-]{2,}\b", text.lower())
        if not words:
            return [0.0] * self.dim
        counts = Counter(words)
        vec = [0.0] * self.dim
        for w, count in counts.items():
            idx = abs(hash(w)) % self.dim
            vec[idx] += (1.0 + math.log(count)) * (1.0 + 0.1 * len(w))
        norm = math.sqrt(sum(x * x for x in vec))
        return [x / norm for x in vec] if norm > 0 else vec


class VectorFAQEngine:
    def __init__(self, csv_path: Optional[str] = None):
        self.csv_path = Path(csv_path or FAQ_CSV_PATH)
        self.vectorizer = DenseVectorEngine()
        self.faqs: List[Dict[str, Any]] = []
        self._load_and_index_faqs()

    def _load_and_index_faqs(self):
        if not self.csv_path.exists():
            return

        with open(self.csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader):
                q = row.get("question", "")
                cat = row.get("category", "General")
                ans = row.get("answer", "")

                text_to_embed = f"{q} {cat}"
                vec = self.vectorizer.vectorize(text_to_embed)

                self.faqs.append({
                    "id": idx + 1,
                    "question": q,
                    "category": cat,
                    "answer": ans,
                    "embedding": vec
                })

    def search_faq(self, query: str, top_k: int = 2) -> List[Tuple[Dict[str, Any], float]]:
        """
        Searches FAQ database using cosine semantic similarity.
        """
        if not self.faqs:
            return []

        q_vec = self.vectorizer.vectorize(query)
        scored = []

        for item in self.faqs:
            score = cosine_sim(q_vec, item["embedding"])
            scored.append((item, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]

    def answer_query(self, query: str) -> Dict[str, Any]:
        """
        Answers a user FAQ question with confidence score and source category.
        """
        results = self.search_faq(query, top_k=1)
        if not results or results[0][1] < 0.20:
            return {
                "answer": "I could not locate an exact match in the #Gyan Labs policy handbook. Please contact our support team at **support@gyanlabs.ai** for personalized enterprise assistance.",
                "confidence": 0.0,
                "matched_question": None,
                "category": None
            }

        best_faq, score = results[0]
        formatted_answer = (
            f"### 📚 #Gyan Labs Policy & Warranty Knowledge Base\n\n"
            f"**Q: {best_faq['question']}**\n\n"
            f"{best_faq['answer']}\n\n"
            f"*Category: {best_faq['category']} &bull; Match Confidence: {int(score * 100)}%*"
        )

        return {
            "answer": formatted_answer,
            "confidence": round(score, 3),
            "matched_question": best_faq["question"],
            "category": best_faq["category"]
        }
