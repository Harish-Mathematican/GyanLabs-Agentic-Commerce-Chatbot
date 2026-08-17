"""
#Gyan Labs - Semantic Query Intent Router
==========================================
Classifies incoming user messages into one of 4 specialized routes:
- 'catalog_sql': Hardware product specs, pricing, stock levels, and comparisons.
- 'faq': Warranty, RMA, shipping terms, return policies, and enterprise SLAs.
- 'order_tracking': Real-time order status, tracking numbers, and delivery dates.
- 'small_talk': Conversational greetings, identity questions, and pleasantries.
"""

from typing import Tuple, Dict, List
import re
from src.faq_engine.vector_faq import DenseVectorEngine, cosine_sim


class CommerceSemanticRouter:
    def __init__(self):
        self.vectorizer = DenseVectorEngine(dim=256)

        # Seed Anchor Utterances
        self.route_anchors = {
            "small_talk": [
                "hello", "hi there", "hey", "good morning", "who are you",
                "what is your name", "are you an ai", "what can you do",
                "thank you", "thanks a lot", "bye", "how are you"
            ],
            "order_tracking": [
                "track my order", "where is my package", "order status",
                "track GL-ORD-8821", "tracking number FX-9982410294",
                "when will my order arrive", "has my order shipped yet",
                "check status of order 8822", "delivery date for my shipment"
            ],
            "faq": [
                "what is your warranty policy on gpu servers",
                "how fast is shipping to canada and us",
                "do you support net-30 corporate purchase orders",
                "what is your return and refund policy",
                "can we lease gpu servers on monthly contracts",
                "how do i initiate an rma for defective hardware",
                "are yubikeys compatible with linux and mac"
            ],
            "catalog_sql": [
                "show me all nvidia h100 gpu servers",
                "what is the price of macbook pro m3 max",
                "do you have workstations under 10000 usd",
                "list all products with enterprise discounts",
                "which gpu nodes are in stock",
                "compare h100 and h200 server specifications",
                "show top rated developer workstations",
                "jetson edge ai developer kits in stock"
            ]
        }

        # Pre-embed anchor vectors
        self.anchor_vectors: Dict[str, List[List[float]]] = {}
        for route_name, utterances in self.route_anchors.items():
            self.anchor_vectors[route_name] = [self.vectorizer.vectorize(u) for u in utterances]

    def route_query(self, query: str) -> Tuple[str, float]:
        """
        Routes user query to the most appropriate subsystem with confidence score.
        """
        q_clean = query.strip().lower()

        # 1. Direct Regex Fast Paths
        if re.search(r"\b(track|order\s+status|gl-ord-|tracking\s*#?)\b", q_clean):
            return "order_tracking", 0.98

        if re.match(r"^(hi|hello|hey|good\s+(morning|afternoon|evening)|thanks|thank\s+you|bye)[\s!.]*$", q_clean):
            return "small_talk", 0.99

        if any(w in q_clean for w in ["warranty", "rma", "refund", "return policy", "net-30", "how fast is shipping", "payment method", "custom liquid cooling"]):
            return "faq", 0.95

        if any(w in q_clean for w in ["price", "cost", "buy", "specs", "stock", "server", "workstation", "h100", "h200", "b200", "macbook", "yubikey", "under", "discount"]):
            return "catalog_sql", 0.95

        # 2. Semantic Cosine Vector Distance Routing
        q_vec = self.vectorizer.vectorize(query)
        scores = {}

        for route_name, vectors in self.anchor_vectors.items():
            max_sim = max(cosine_sim(q_vec, v) for v in vectors)
            scores[route_name] = max_sim

        best_route = max(scores, key=scores.get)
        best_score = scores[best_route]

        # Default fallback
        if best_score < 0.25:
            return "catalog_sql", 0.50

        return best_route, best_score
