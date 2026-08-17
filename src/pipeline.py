"""
#Gyan Labs - Unified AI Commerce & Infrastructure Chatbot Pipeline
==================================================================
Coordinates multi-route intent classification, Text-to-SQL product search,
vector FAQ retrieval, order status tracking, and conversational interactions.
"""

from typing import Dict, Any, Optional, List
import time
from pathlib import Path

from src.config import DB_PATH, FAQ_CSV_PATH
from src.catalog_sql import DatabaseManager, SQLGenerator, ProductComprehensionEngine
from src.faq_engine import VectorFAQEngine
from src.order_tracker import OrderTracker
from src.smalltalk import SmallTalkAgent
from src.router import CommerceSemanticRouter


class CommerceChatbotPipeline:
    def __init__(
        self,
        db_path: Optional[str] = None,
        faq_csv_path: Optional[str] = None
    ):
        self.db_path = db_path or str(DB_PATH)
        self.faq_csv_path = faq_csv_path or str(FAQ_CSV_PATH)

        # 1. Initialize Database & Catalog
        self.db_manager = DatabaseManager(db_path=self.db_path)
        schema = self.db_manager.get_schema()

        # 2. Subsystems
        self.sql_generator = SQLGenerator(schema=schema)
        self.comprehension = ProductComprehensionEngine()
        self.faq_engine = VectorFAQEngine(csv_path=self.faq_csv_path)
        self.order_tracker = OrderTracker(db_path=self.db_path)
        self.smalltalk = SmallTalkAgent()
        self.router = CommerceSemanticRouter()

    def process_message(
        self,
        user_query: str,
        force_route: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Processes an incoming user query through the intent router and appropriate engine.
        """
        start_time = time.time()

        # Step 1: Semantic Intent Routing
        if force_route:
            route, confidence = force_route, 1.0
        else:
            route, confidence = self.router.route_query(user_query)

        # Step 2: Route Execution
        # Route A: Order Tracking
        if route == "order_tracking":
            order_id = self.order_tracker.extract_order_id(user_query)
            if order_id:
                track_res = self.order_tracker.track_order(order_id)
                return {
                    "route": "order_tracking",
                    "route_confidence": confidence,
                    "answer": track_res["formatted_message"] if track_res["found"] else track_res["message"],
                    "data": track_res.get("data"),
                    "latency_seconds": round(time.time() - start_time, 3)
                }
            else:
                return {
                    "route": "order_tracking",
                    "route_confidence": confidence,
                    "answer": "Please provide your #Gyan Labs **Order ID** (e.g. `GL-ORD-8821`) or carrier **Tracking Number** (e.g. `FX-9982410294`) so I can retrieve your real-time shipment status.",
                    "data": None,
                    "latency_seconds": round(time.time() - start_time, 3)
                }

        # Route B: Policy & Warranty FAQ
        elif route == "faq":
            faq_res = self.faq_engine.answer_query(user_query)
            return {
                "route": "faq",
                "route_confidence": confidence,
                "answer": faq_res["answer"],
                "data": {"category": faq_res.get("category"), "question": faq_res.get("matched_question")},
                "latency_seconds": round(time.time() - start_time, 3)
            }

        # Route C: Smalltalk
        elif route == "small_talk":
            talk_answer = self.smalltalk.talk(user_query)
            return {
                "route": "small_talk",
                "route_confidence": confidence,
                "answer": talk_answer,
                "data": None,
                "latency_seconds": round(time.time() - start_time, 3)
            }

        # Route D: Hardware Catalog SQL (Default)
        else:
            sql_query = self.sql_generator.generate_sql(user_query)
            query_res = self.db_manager.execute_query(sql_query)
            products = query_res.get("rows", [])
            formatted_cards = self.comprehension.format_products(
                query=user_query,
                products=products,
                sql_used=sql_query
            )

            return {
                "route": "catalog_sql",
                "route_confidence": confidence,
                "answer": formatted_cards,
                "data": {"products": products, "sql": sql_query, "count": len(products)},
                "latency_seconds": round(time.time() - start_time, 3)
            }

    def get_all_products(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Helper method to list products for catalog explorer.
        """
        sql = "SELECT * FROM products"
        if category and category != "All":
            sql += f" WHERE category = '{category}'"
        sql += " ORDER BY price_usd DESC;"
        res = self.db_manager.execute_query(sql)
        return res.get("rows", [])
