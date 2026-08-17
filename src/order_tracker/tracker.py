"""
#Gyan Labs - Order & Shipment Tracking Subsystem
=================================================
Looks up customer enterprise purchase orders, shipping carrier status (FedEx, UPS,
Canada Post), transit tracking codes, and estimated delivery dates.
"""

from typing import Dict, Any, Optional
import sqlite3
from pathlib import Path
import re


class OrderTracker:
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)

    def extract_order_id(self, query: str) -> Optional[str]:
        """
        Extracts order ID (e.g. GL-ORD-8821 or 8821) or tracking number from text.
        """
        # Match GL-ORD-XXXX
        match = re.search(r"GL-ORD-\d{4}", query, re.IGNORECASE)
        if match:
            return match.group(0).upper()

        # Match 4-digit number if order context
        match_digits = re.search(r"\b(\d{4})\b", query)
        if match_digits and ("order" in query.lower() or "track" in query.lower()):
            return f"GL-ORD-{match_digits.group(1)}"

        # Match tracking numbers (FX-..., 1Z-..., CP-...)
        match_track = re.search(r"\b(FX-\d+|1Z-[A-Z0-9]+|CP-\d+CA)\b", query, re.IGNORECASE)
        if match_track:
            return match_track.group(0).upper()

        return None

    def track_order(self, identifier: str) -> Dict[str, Any]:
        """
        Retrieves order and transit tracking record from SQLite.
        """
        id_clean = identifier.strip().upper()

        with sqlite3.connect(str(self.db_path)) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Query by order_id or tracking_number
            cursor.execute("""
            SELECT o.*, p.title as product_title, p.category as product_category
            FROM customer_orders o
            JOIN products p ON o.product_id = p.product_id
            WHERE UPPER(o.order_id) = ? OR UPPER(o.tracking_number) = ?
            """, (id_clean, id_clean))

            row = cursor.fetchone()
            if not row:
                return {
                    "found": False,
                    "message": f"Order or Tracking Number '{identifier}' was not found in the #Gyan Labs fulfillment registry."
                }

            data = dict(row)
            status_emojis = {
                "Processing": "⏳ Processing & Quality Gate Inspection",
                "Shipped": "📦 Dispatched from Fulfillment Hub",
                "In Transit": "🚚 In Transit with Carrier",
                "Delivered": "✅ Delivered & Signed For"
            }

            status_text = status_emojis.get(data["status"], data["status"])

            formatted = (
                f"### 📦 Order Tracking Status: `{data['order_id']}`\n\n"
                f"• **Status:** **{status_text}**\n"
                f"• **Customer:** {data['customer_name']} ({data['customer_email']})\n"
                f"• **Item Ordered:** {data['product_title']} (Qty: {data['quantity']})\n"
                f"• **Total Value:** ${data['total_usd']:,.2f} USD\n"
                f"• **Carrier:** {data['carrier']} &bull; **Tracking #:** `{data['tracking_number']}`\n"
                f"• **Destination:** 📍 {data['destination_city']}\n"
                f"• **Estimated Delivery:** 📅 **{data['estimated_delivery']}**\n"
            )

            return {
                "found": True,
                "data": data,
                "formatted_message": formatted
            }
