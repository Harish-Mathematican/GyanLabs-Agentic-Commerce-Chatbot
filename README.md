# 🤖 #GyanLabs-Agentic-Commerce-Chatbot: Enterprise AI Hardware & Cloud Infrastructure Assistant

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit UI](https://img.shields.io/badge/Streamlit-Interactive%20Dashboard-FF4B4B.svg)](https://streamlit.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-REST%20Endpoints-009688.svg)](https://fastapi.tiangolo.com/)
[![SQLite](https://img.shields.io/badge/SQLite-Catalog%20%26%20Orders-003B57.svg)](https://www.sqlite.org/)
[![Vector Search](https://img.shields.io/badge/Vector%20Search-Cosine%20Similarity-8A2BE2.svg)](https://github.com/langchain-ai/langchain)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

> [!NOTE]
> **Educational & Research Demonstration Disclaimer:**  
> This project, including the fictitious enterprise identity ("#Gyan Labs / HashGyan Technologies"), simulated AI server catalogs, pricing tiers, and sample customer logistics records, is developed exclusively for **educational, instructional, open-source portfolio demonstration, and conversational AI research**. All hardware configurations and order tracking IDs are synthetically generated. Any resemblance to real entities is purely coincidental.

**#GyanLabs-Agentic-Commerce-Chatbot** is an enterprise-grade, multi-route conversational AI assistant engineered for high-performance AI hardware and cloud compute procurement. It features **semantic query intent routing**, **natural language Text-to-SQL catalog querying**, **vector-based warranty & policy FAQ retrieval**, and **real-time carrier order tracking** across North American logistics hubs.

---

## 🌟 Multi-Route System Architecture

<div align="center">
  <img src="assets/architecture_diagram.png" alt="#Gyan Labs AI Commerce Architecture Diagram" width="95%" style="border-radius: 10px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); margin-bottom: 20px;" />
</div>

<details open>
<summary><b>📐 Text-Based Architecture View</b></summary>
┌──────────────────────────────────────────────────────────────────────────┐
│                       1. CLIENT INTERFACE LAYER                          │
│       👤 User Query (Natural Language)   •   📦 Order Tracking ID        │
└────────────────────────────────────┬─────────────────────────────────────┘
                                     │
                                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                       2. SEMANTIC INTENT ROUTER                          │
│             4-Way Autonomous AI Classifier (Sub-5ms Latency)             │
└───────────────┬────────────────────┬────────────────────┬────────────────┘
                │                    │                    │
                ▼                    ▼                    ▼
     ┌─────────────────────┐┌─────────────────────┐┌───────────────────────┐
     │ 🛒 HARDWARE CATALOG ││ 📚 POLICY & FAQS    ││ 🚚 LOGISTICS TRACKER  │
     │  Text-to-SQL Engine ││  Vector Cosine Search││  Carrier Order Status│
     └──────────┬──────────┘└──────────┬──────────┘└───────────┬───────────┘
                │                      │                       │
                ▼                      ▼                       ▼
     ┌─────────────────────┐┌─────────────────────┐┌───────────────────────┐
     │ 🗄️ SQLite Catalog DB││ 📁 Vector Knowledge ││ 📋 Orders Registry   │
     │  (GPU Nodes & Specs)││  (Warranty & RMA)   ││  (FedEx/UPS/CanadaPost│
     └──────────┬──────────┘└──────────┬──────────┘└───────────┬───────────┘
                │                      │                       │
                └──────────────────────┼───────────────────────┘
                                       │
                                       ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                       3. SYNTHESIS & PRESENTATION                        │
│          📄 Markdown Product Cards  •  🏷️ Enterprise Discount Badges     │
└────────────────────────────────────┬─────────────────────────────────────┘
                                     │
                     ┌───────────────┴───────────────┐
                     ▼                               ▼
     ┌───────────────────────────────┐ ┌───────────────────────────────────┐
     │ 💻 Streamlit UI (app.py)      │ │ 🌐 FastAPI REST API (api.py)      │
     │   Interactive Chat & Explorer │ │   Production Microservice         │
     └───────────────────────────────┘ └───────────────────────────────────┘
```
</details>

---

## 🚀 Key Subsystems & Capabilities

| Subsystem | Technical Implementation | Description |
| :--- | :--- | :--- |
| **🎯 Semantic Intent Router** | `CommerceSemanticRouter` | Classifies user queries across 4 distinct execution paths with sub-5ms latency and confidence scoring. |
| **📊 Natural Language Text-to-SQL** | `SQLGenerator`, `DatabaseManager` | Translates natural language requests into safe, read-only SQLite queries over GPU servers, workstations, and peripherals. |
| **🛒 Product Card Comprehension** | `ProductComprehensionEngine` | Formats SQL outputs into executive markdown cards with specs, prices, discount badges, and links. |
| **📚 Vector FAQ & Policy Engine** | `VectorFAQEngine` | Cosine similarity semantic search over enterprise warranties, Net-30 payment terms, and RMA return procedures. |
| **📦 Real-Time Order Tracking** | `OrderTracker` | Extracts tracking numbers and order IDs to query real-time transit status, carriers (FedEx, UPS, Canada Post), and delivery dates. |
| **💬 Conversational Agent** | `SmallTalkAgent` | Provides friendly conversational interactions, capabilities overview, and platform guidance. |
| **⚡ Zero-Dependency Fallback** | `DenseVectorEngine` | Operates completely offline with zero mandatory cloud API keys or heavy GPU runtimes. |

---

## 📁 Repository Structure

```text
Project HashGyan/Chatbot/
├── data/                            # Enterprise catalog and FAQ datasets
│   ├── enterprise_catalog.db        # SQLite database (Products & Orders tables)
│   └── enterprise_faqs.csv          # 10+ detailed hardware and warranty FAQs
├── src/                             # Core Python Engine
│   ├── __init__.py
│   ├── config.py                    # Global configurations & constants
│   ├── router/                      # Semantic Intent Routing
│   │   ├── __init__.py
│   │   └── semantic_router.py       # 4-Route query classifier
│   ├── catalog_sql/                 # Text-to-SQL Catalog Subsystem
│   │   ├── __init__.py
│   │   ├── db_manager.py            # SQLite schema setup & catalog seeder
│   │   ├── sql_generator.py         # Natural Language to SQL converter
│   │   └── comprehension.py         # Tabular data synthesis into product cards
│   ├── faq_engine/                  # Policy & Warranty FAQ Subsystem
│   │   ├── __init__.py
│   │   └── vector_faq.py            # Dense vector semantic similarity search
│   ├── order_tracker/               # Logistics & Order Tracking Subsystem
│   │   ├── __init__.py
│   │   └── tracker.py               # Order status lookup by ID / tracking #
│   ├── smalltalk/                   # Conversational Smalltalk Subsystem
│   │   ├── __init__.py
│   │   └── agent.py                 # Identity & guidance agent
│   └── pipeline.py                  # Central enterprise orchestrator
├── tests/
│   ├── __init__.py
│   └── test_chatbot_services.py     # Comprehensive Pytest test suite
├── app.py                           # Interactive Streamlit Web Application
├── api.py                           # FastAPI REST API microservice
├── run_app.bat                      # Windows launcher script
├── pyproject.toml                   # Packaging metadata
├── requirements.txt                 # Frozen dependencies
├── .env.example                     # Sample environment file
├── LICENSE                          # MIT License
└── README.md                        # Documentation & architecture guides
```

---

## ⚡ Quickstart & Installation

### 1. Clone & Set Up Virtual Environment

```bash
git clone https://github.com/Harish-Mathematican/GyanLabs-Agentic-Commerce-Chatbot.git
cd GyanLabs-Agentic-Commerce-Chatbot

python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment (Optional)

Create a `.env` file (or copy `.env.example`):
```ini
GROQ_API_KEY=your_groq_api_key_here
DEFAULT_LLM_MODEL=llama-3.3-70b-versatile
```
*(If no API keys are provided, the system automatically uses the internal zero-dependency synthesizer!)*

---

## 🖥️ Launching the Application

### Option A: Launch Streamlit Dashboard
```bash
streamlit run app.py
```
*(Or double-click `run_app.bat` on Windows)*

👉 Open **`http://localhost:8501`** in your browser.

### Option B: Launch FastAPI REST Microservice
```bash
python api.py
```
👉 Open Swagger API Docs at **`http://localhost:8001/docs`**.

---

## 🧪 Testing & Verification

Run the automated Pytest test suite:
```bash
python -m pytest tests/ -v
```

---

## 🏷️ Sample Test Prompts

* **Hardware Search:** `"Show me NVIDIA HGX H100 and H200 GPU servers"`
* **Price Filter:** `"Show developer workstations under 10000 USD"`
* **Warranty Policy:** `"What is the warranty and RMA policy on GPU servers?"`
* **Order Tracking:** `"Track status of order GL-ORD-8821"` (or `GL-ORD-8822`)
* **Shipping Policy:** `"How fast is shipping to Canada and the United States?"`

---

## 📜 License

Distributed under the [MIT License](LICENSE).  
Developed by **Harish Dhakal** (#Gyan Labs AI Systems Demo).
