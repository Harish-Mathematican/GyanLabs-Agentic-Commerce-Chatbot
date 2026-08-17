"""
#Gyan Labs - Enterprise AI Hardware & Cloud Infrastructure Commerce Chatbot
===========================================================================
Interactive Streamlit application featuring multi-route semantic query intent,
Text-to-SQL hardware search, vector FAQ retrieval, and live order tracking.

DISCLAIMER:
Developed exclusively for educational, research, and open-source demonstration.
"""

import streamlit as st
import time
import os
import sys
import pandas as pd
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.pipeline import CommerceChatbotPipeline

# Page Configuration
st.set_page_config(
    page_title="#Gyan Labs — AI Commerce & Hardware Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.2rem;
    }
    .badge-route {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
        background-color: #f0fdf4;
        color: #15803d;
        border: 1px solid #bbf7d0;
        margin-right: 8px;
    }
    .card-product {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 14px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_pipeline():
    return CommerceChatbotPipeline()


pipeline = get_pipeline()

# Sidebar
with st.sidebar:
    st.image("https://img.shields.io/badge/%23Gyan_Labs-AI_Commerce_Assistant-10b981?style=for-the-badge", use_container_width=True)
    st.markdown("### ⚙️ Engine Controls")

    force_route = st.selectbox(
        "Intent Router Override",
        ["Auto-Detect (Semantic)", "Catalog SQL", "Policy FAQ", "Order Tracking", "Small-talk"]
    )

    st.markdown("---")
    st.markdown("### 📦 Fulfillment Hubs")
    st.markdown("""
    • 🇨🇦 **Canada Hubs:** Toronto (ON), Montreal (QC), Vancouver (BC)  
    • 🇺🇸 **US Hubs:** Seattle (WA), San Francisco (CA), Austin (TX)  
    • 🚚 **Carriers:** FedEx Freight Priority, UPS Express, Canada Post Xpresspost
    """)

    st.markdown("---")
    st.markdown("### 🏷️ Sample Order IDs for Testing")
    st.markdown("""
    • `GL-ORD-8821` (Alexandre Tremblay - H100 Server)  
    • `GL-ORD-8822` (Sarah Lin - MacBook Pro M3 Max)  
    • `GL-ORD-8823` (David Tremblay - Jetson Orin Kit)  
    • `GL-ORD-8824` (Marcus Vance - YubiKey 10-Pack)
    """)

    st.markdown("---")
    st.markdown("<small>Developed by **Harish Dhakal** &bull; #Gyan Labs</small>", unsafe_allow_html=True)

# Main Navigation Tabs
tab_chat, tab_catalog, tab_tracking, tab_faq, tab_sql = st.tabs([
    "💬 AI Commerce Chatbot",
    "🛒 Interactive Catalog Explorer",
    "📦 Live Order Tracker",
    "📚 Warranty & Policy FAQs",
    "💻 Direct SQL Console"
])

# =====================================================================
# TAB 1: AI CHATBOT
# =====================================================================
with tab_chat:
    st.markdown('<div class="main-header">🤖 #Gyan Labs AI Hardware & Compute Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Natural language GPU catalog search, instant warranty FAQs, and real-time shipment tracking.</div>', unsafe_allow_html=True)

    # Quick Suggestion Chips
    st.markdown("**💡 Quick Question Suggestions:**")
    q1, q2, q3, q4 = st.columns(4)
    sample_to_run = None
    if q1.button("⚡ Show NVIDIA H100 & H200 Servers"):
        sample_to_run = "Show me NVIDIA HGX H100 and H200 GPU servers"
    if q2.button("💻 Workstations with Discount"):
        sample_to_run = "List all developer workstations that have discounts"
    if q3.button("📦 Track Order GL-ORD-8821"):
        sample_to_run = "Track status of order GL-ORD-8821"
    if q4.button("🛡️ Check 3-Year Warranty Policy"):
        sample_to_run = "What is the warranty and RMA policy on GPU servers?"

    # Initialize Messages
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Welcome to **#Gyan Labs**! I am your AI Hardware & Infrastructure Assistant. How can I help you explore our GPU compute clusters, developer workstations, warranty policies, or track your shipment?",
                "route": "small_talk",
                "latency": 0.01
            }
        ]

    # Render History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if msg.get("route"):
                route_icons = {
                    "catalog_sql": "🛒 Hardware Catalog SQL",
                    "faq": "📚 Policy & Warranty FAQ",
                    "order_tracking": "📦 Live Order Tracker",
                    "small_talk": "💬 Conversational"
                }
                badge_text = route_icons.get(msg["route"], msg["route"])
                st.markdown(f'<span class="badge-route">{badge_text}</span> <small style="color:#64748b;">Latency: {msg.get("latency", 0)}s</small>', unsafe_allow_html=True)
            st.markdown(msg["content"])

    # Chat Input
    user_query = st.chat_input("Ask about GPU specs, pricing, warranty terms, or track an order...")
    if sample_to_run:
        user_query = sample_to_run

    if user_query:
        # Add User Message
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        # Process Query
        with st.chat_message("assistant"):
            with st.spinner("Processing request and querying systems..."):
                route_override = None if force_route == "Auto-Detect (Semantic)" else force_route.lower().replace(" ", "_")
                result = pipeline.process_message(user_query, force_route=route_override)

                route_icons = {
                    "catalog_sql": "🛒 Hardware Catalog SQL",
                    "faq": "📚 Policy & Warranty FAQ",
                    "order_tracking": "📦 Live Order Tracker",
                    "small_talk": "💬 Conversational"
                }
                badge_text = route_icons.get(result["route"], result["route"])
                st.markdown(f'<span class="badge-route">{badge_text}</span> <small style="color:#64748b;">Latency: {result["latency_seconds"]}s</small>', unsafe_allow_html=True)
                st.markdown(result["answer"])

        st.session_state.messages.append({
            "role": "assistant",
            "content": result["answer"],
            "route": result["route"],
            "latency": result["latency_seconds"]
        })

# =====================================================================
# TAB 2: INTERACTIVE CATALOG EXPLORER
# =====================================================================
with tab_catalog:
    st.markdown("### 🛒 #Gyan Labs Enterprise Hardware Catalog")
    st.markdown("Explore high-performance GPU compute clusters, developer workstations, and zero-trust security hardware.")

    col1, col2 = st.columns([1, 3])
    with col1:
        cat_filter = st.selectbox(
            "Filter Category",
            ["All", "GPU Compute Server", "Inference Server", "Developer Workstation", "Edge AI Device", "Zero-Trust Security", "Peripherals & Displays"]
        )

    products = pipeline.get_all_products(category=cat_filter)
    st.markdown(f"**Showing {len(products)} Product(s):**")

    for p in products:
        discount = p.get("discount_pct", 0.0)
        price = p.get("price_usd", 0)
        final_price = price * (1.0 - discount) if discount > 0 else price
        discount_badge = f"<span style='color:#ef4444; font-weight:bold;'>({int(discount*100)}% OFF)</span>" if discount > 0 else ""

        with st.container():
            st.markdown(f"""
            <div class="card-product">
                <h4 style="margin:0 0 8px 0;"><a href="{p['product_url']}" target="_blank" style="text-decoration:none; color:#0f172a;">{p['title']}</a></h4>
                <p style="margin:4px 0; color:#475569;"><strong>Specs:</strong> {p['specs']}</p>
                <div style="display:flex; justify-content:space-between; margin-top:10px;">
                    <div>
                        <span style="font-size:1.15rem; font-weight:700; color:#0284c7;">${final_price:,.2f} USD</span> {discount_badge}
                    </div>
                    <div>
                        <span style="background-color:#e0f2fe; color:#0369a1; padding:3px 8px; border-radius:4px; font-size:0.85rem; font-weight:600;">{p['category']}</span> &bull; 
                        <span style="color:#16a34a; font-weight:600;">In Stock ({p['stock_quantity']})</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# =====================================================================
# TAB 3: ORDER TRACKER
# =====================================================================
with tab_tracking:
    st.markdown("### 📦 Real-Time Order & Logistics Tracker")
    st.markdown("Check transit status, carrier tracking numbers, and delivery dates across North American fulfillment hubs.")

    order_input = st.text_input("Enter Order ID or Carrier Tracking Number:", "GL-ORD-8821")
    if st.button("🔍 Track Shipment"):
        res = pipeline.order_tracker.track_order(order_input)
        if res["found"]:
            st.markdown(res["formatted_message"])
            data = res["data"]
            # Visual status indicator
            statuses = ["Processing", "Shipped", "In Transit", "Delivered"]
            curr_status = data["status"]
            curr_idx = statuses.index(curr_status) if curr_status in statuses else 0
            st.progress((curr_idx + 1) / len(statuses))
        else:
            st.warning(res["message"])

# =====================================================================
# TAB 4: FAQS & POLICIES
# =====================================================================
with tab_faq:
    st.markdown("### 📚 Enterprise Warranty, RMA & Procurement Policies")
    st.markdown("Search our vector-indexed knowledge base for policies regarding warranties, Net-30 terms, and cross-border shipping.")

    faq_query = st.text_input("Search Policy Question:", "What is the return policy?")
    if st.button("🔎 Search Policy"):
        faq_res = pipeline.faq_engine.answer_query(faq_query)
        st.markdown(faq_res["answer"])

    with st.expander("📖 Browse All Indexed Policy FAQs"):
        if pipeline.faq_engine.faqs:
            for item in pipeline.faq_engine.faqs:
                st.markdown(f"**Q: {item['question']}** *({item['category']})*")
                st.markdown(f"{item['answer']}")
                st.markdown("---")

# =====================================================================
# TAB 5: DIRECT SQL CONSOLE
# =====================================================================
with tab_sql:
    st.markdown("### 💻 Direct SQLite Catalog Sandbox")
    st.markdown("Execute custom read-only SQL queries directly against the enterprise database.")

    raw_sql = st.text_area("SQL Query:", "SELECT category, count(*) as count, AVG(price_usd) as avg_price FROM products GROUP BY category;", height=100)
    if st.button("▶️ Run SQL Query"):
        try:
            res = pipeline.db_manager.execute_query(raw_sql)
            if res.get("rows"):
                df = pd.DataFrame(res["rows"])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("Query executed successfully. No rows returned.")
        except Exception as e:
            st.error(f"SQL Error: {e}")

    with st.expander("🗄️ View Database Schemas"):
        st.code(pipeline.db_manager.get_schema(), language="sql")
