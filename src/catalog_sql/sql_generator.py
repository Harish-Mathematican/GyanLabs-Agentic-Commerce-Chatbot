"""
#Gyan Labs - Natural Language to SQL Query Generator
====================================================
Translates user natural language hardware queries into safe SQLite SELECT queries
using LLM inference with fallback heuristic rules.
"""

from typing import Optional
import re
from src.config import GROQ_API_KEY, OPENAI_API_KEY, DEFAULT_LLM_MODEL


SQL_GENERATOR_PROMPT = """You are a senior SQLite database engineer for #Gyan Labs Enterprise Hardware & AI Catalog.
Convert the natural language user question into a valid, safe, read-only SQL query.

DATABASE SCHEMA:
{schema}

RULES:
- Generate ONLY a single SELECT query.
- Use `LIKE '%keyword%'` for case-insensitive matching on brand, title, specs, or category.
- Do NOT use INSERT, UPDATE, DELETE, or DROP.
- Wrap output strictly in `<SQL> SELECT ... </SQL>`.

QUESTION: {question}
"""


class SQLGenerator:
    def __init__(self, schema: str, model_name: str = DEFAULT_LLM_MODEL):
        self.schema = schema
        self.model_name = model_name
        self.groq_client = None

        if GROQ_API_KEY:
            try:
                from groq import Groq
                self.groq_client = Groq(api_key=GROQ_API_KEY)
            except Exception:
                self.groq_client = None

    def generate_sql(self, natural_query: str) -> str:
        """
        Generates SQL string for a given natural language query.
        """
        # 1. Try Groq LLM if available
        if self.groq_client:
            try:
                prompt = SQL_GENERATOR_PROMPT.format(schema=self.schema, question=natural_query)
                completion = self.groq_client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1,
                    max_tokens=256
                )
                raw_out = completion.choices[0].message.content.strip()
                matches = re.findall(r"<SQL>(.*?)</SQL>", raw_out, re.DOTALL)
                if matches:
                    return matches[0].strip()
            except Exception as e:
                print(f"Warning: LLM SQL generation failed: {e}")

        # 2. Robust Heuristic Rule-Based Generator (Offline Fallback)
        q = natural_query.lower()

        # Price filters
        price_under = re.search(r"(under|less than|below)\s*(?:usd|\$)?\s*(\d+(?:,\d+)?)", q)
        if price_under:
            max_p = float(price_under.group(2).replace(",", ""))
            return f"SELECT * FROM products WHERE price_usd <= {max_p} ORDER BY price_usd ASC;"

        if "h100" in q or "hgx" in q:
            return "SELECT * FROM products WHERE title LIKE '%H100%' OR specs LIKE '%H100%';"
        elif "h200" in q or "b200" in q or "blackwell" in q:
            return "SELECT * FROM products WHERE title LIKE '%H200%' OR title LIKE '%GB200%' OR specs LIKE '%Blackwell%';"
        elif "macbook" in q or "apple" in q or "laptop" in q:
            return "SELECT * FROM products WHERE brand = 'Apple' OR title LIKE '%MacBook%';"
        elif "workstation" in q or "desktop" in q:
            return "SELECT * FROM products WHERE category LIKE '%Workstation%' ORDER BY price_usd ASC;"
        elif "discount" in q or "sale" in q or "offer" in q:
            return "SELECT * FROM products WHERE discount_pct > 0 ORDER BY discount_pct DESC;"
        elif "yubikey" in q or "security" in q or "zero trust" in q:
            return "SELECT * FROM products WHERE category LIKE '%Security%' OR title LIKE '%YubiKey%';"
        elif "monitor" in q or "display" in q or "keyboard" in q or "peripheral" in q:
            return "SELECT * FROM products WHERE category LIKE '%Peripherals%' ORDER BY price_usd ASC;"
        elif "edge" in q or "jetson" in q or "orin" in q:
            return "SELECT * FROM products WHERE category LIKE '%Edge%' OR title LIKE '%Jetson%';"
        elif "top rated" in q or "best" in q or "rating" in q:
            return "SELECT * FROM products ORDER BY avg_rating DESC, price_usd ASC LIMIT 5;"
        else:
            return "SELECT * FROM products ORDER BY price_usd DESC LIMIT 8;"
