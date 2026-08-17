"""
#Gyan Labs - Unit Test Suite for AI Commerce Chatbot
====================================================
Tests SQLite database, SQL generator, product cards comprehension,
vector FAQ search, order tracking, and 4-route semantic intent router.
"""

import pytest
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.catalog_sql import DatabaseManager, SQLGenerator, ProductComprehensionEngine
from src.faq_engine import VectorFAQEngine
from src.order_tracker import OrderTracker
from src.smalltalk import SmallTalkAgent
from src.router import CommerceSemanticRouter
from src.pipeline import CommerceChatbotPipeline


@pytest.fixture
def test_db(tmp_path):
    db_file = tmp_path / "test_catalog.db"
    return DatabaseManager(str(db_file))


@pytest.fixture
def test_pipeline(tmp_path):
    db_file = tmp_path / "pipeline_test.db"
    return CommerceChatbotPipeline(db_path=str(db_file))


def test_database_initialization(test_db):
    res = test_db.execute_query("SELECT COUNT(*) as count FROM products;")
    assert res["rows"][0]["count"] >= 10

    orders_res = test_db.execute_query("SELECT COUNT(*) as count FROM customer_orders;")
    assert orders_res["rows"][0]["count"] >= 4


def test_sql_generator_heuristics(test_db):
    schema = test_db.get_schema()
    generator = SQLGenerator(schema=schema)

    sql_h100 = generator.generate_sql("Show me NVIDIA H100 servers")
    assert "H100" in sql_h100

    sql_price = generator.generate_sql("Show workstations under 5000 USD")
    assert "5000" in sql_price


def test_product_comprehension(test_db):
    engine = ProductComprehensionEngine()
    products = test_db.execute_query("SELECT * FROM products WHERE brand = 'Apple';")["rows"]
    cards = engine.format_products("Apple MacBook Pro", products, "SELECT * FROM products WHERE brand='Apple';")
    assert "MacBook Pro" in cards
    assert "Price:" in cards


def test_vector_faq():
    faq = VectorFAQEngine()
    ans = faq.answer_query("What is the warranty policy on GPU servers?")
    assert "3-Year" in ans["answer"] or "Warranty" in ans["answer"]
    assert ans["confidence"] > 0.3


def test_order_tracking(test_db):
    tracker = OrderTracker(str(test_db.db_path))

    # Existing order
    res = tracker.track_order("GL-ORD-8821")
    assert res["found"] is True
    assert "Alexandre Tremblay" in res["formatted_message"]
    assert res["data"]["status"] == "Shipped"
    assert "GL-ORD-8821" in res["formatted_message"]

    # Non-existent order
    res_none = tracker.track_order("GL-ORD-9999")
    assert res_none["found"] is False


def test_semantic_router():
    router = CommerceSemanticRouter()

    # Smalltalk
    route, conf = router.route_query("Hello there! Who are you?")
    assert route == "small_talk"

    # Order tracking
    route, conf = router.route_query("Track order GL-ORD-8821")
    assert route == "order_tracking"

    # FAQ
    route, conf = router.route_query("What is the return and refund policy?")
    assert route == "faq"

    # Catalog SQL
    route, conf = router.route_query("Show me top rated developer workstations")
    assert route == "catalog_sql"


def test_end_to_end_pipeline(test_pipeline):
    # Test Catalog Search
    res_cat = test_pipeline.process_message("Show me NVIDIA H100 servers")
    assert res_cat["route"] == "catalog_sql"
    assert "NVIDIA" in res_cat["answer"]

    # Test FAQ
    res_faq = test_pipeline.process_message("What is the warranty policy on NVIDIA GPU servers?")
    assert res_faq["route"] == "faq"
    assert "Warranty" in res_faq["answer"] or "3-Year" in res_faq["answer"]

    # Test Order Tracker
    res_order = test_pipeline.process_message("Check status of order GL-ORD-8821")
    assert res_order["route"] == "order_tracking"
    assert "Alexandre" in res_order["answer"]
