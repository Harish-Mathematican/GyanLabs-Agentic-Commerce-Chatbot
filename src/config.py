"""
#Gyan Labs - AI Commerce & Infrastructure Chatbot Configuration
================================================================
Centralized configuration parameters for catalog databases, vector store paths,
semantic router thresholds, and LLM inference providers.

DISCLAIMER:
Developed exclusively for educational, research, and open-source demonstration.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "enterprise_catalog.db"
FAQ_CSV_PATH = DATA_DIR / "enterprise_faqs.csv"
VECTORSTORE_DIR = DATA_DIR / "vectorstore"

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(VECTORSTORE_DIR, exist_ok=True)

# LLM Inference Providers
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
DEFAULT_LLM_MODEL = os.getenv("DEFAULT_LLM_MODEL", "llama-3.3-70b-versatile")
TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.2))
MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", 1024))

# Vector & Router Settings
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", 0.35))
