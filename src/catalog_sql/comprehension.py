"""
#Gyan Labs - Product Data Comprehension & Markdown Card Synthesizer
===================================================================
Formats tabular SQL query outputs into polished, executive hardware cards
featuring specifications, stock indicators, and direct procurement links.
"""

from typing import List, Dict, Any, Optional
from src.config import GROQ_API_KEY, DEFAULT_LLM_MODEL


class ProductComprehensionEngine:
    def __init__(self, model_name: str = DEFAULT_LLM_MODEL):
        self.model_name = model_name
        self.groq_client = None

        if GROQ_API_KEY:
            try:
                from groq import Groq
                self.groq_client = Groq(api_key=GROQ_API_KEY)
            except Exception:
                self.groq_client = None

    def format_products(self, query: str, products: List[Dict[str, Any]], sql_used: str) -> str:
        """
        Formats products into structured markdown cards.
        """
        if not products:
            return f"No products found in the #Gyan Labs enterprise catalog matching: *'{query}'*.\n\n*Executed SQL:* `{sql_used}`"

        cards = []
        cards.append(f"### 🛒 Found {len(products)} Product(s) for: *'{query}'*\n")

        for idx, p in enumerate(products, 1):
            title = p.get("title", "Hardware Item")
            price = p.get("price_usd", 0)
            discount = p.get("discount_pct", 0.0)
            discount_str = f" 🔥 **({int(discount * 100)}% Enterprise Discount)**" if discount > 0 else ""
            final_price = price * (1.0 - discount) if discount > 0 else price
            specs = p.get("specs", "Standard enterprise specification")
            stock = p.get("stock_quantity", 0)
            stock_badge = f"🟢 In Stock ({stock} available)" if stock > 0 else "🔴 Out of Stock / Backorder"
            rating = p.get("avg_rating", 5.0)
            url = p.get("product_url", "https://gyanlabs.ai/hardware")

            card = (
                f"#### {idx}. [{title}]({url})\n"
                f"• **Price:** ${final_price:,.2f} USD{discount_str}\n"
                f"• **Specifications:** {specs}\n"
                f"• **Status:** {stock_badge} &bull; **Rating:** ⭐ {rating}/5.0\n"
                f"• **Procure Item:** [Order #{p.get('product_id', '')}]({url})\n"
            )
            cards.append(card)

        cards.append(f"\n*Executed Query:* `{sql_used}`")
        return "\n".join(cards)
