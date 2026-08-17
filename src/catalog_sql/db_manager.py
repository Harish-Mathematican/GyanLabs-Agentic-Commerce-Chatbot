"""
#Gyan Labs - Database Manager & Seed Catalog Subsystem
======================================================
Initializes the SQLite enterprise hardware & cloud compute catalog,
populating products, specifications, inventory, pricing, and live orders.
"""

import sqlite3
from pathlib import Path
from typing import Dict, Any, List, Optional
import os


class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.init_database()

    def init_database(self):
        """
        Creates catalog and orders tables and seeds with rich enterprise data.
        """
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.cursor()

            # 1. Products Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                brand TEXT NOT NULL,
                specs TEXT NOT NULL,
                price_usd REAL NOT NULL,
                discount_pct REAL DEFAULT 0.0,
                stock_quantity INTEGER NOT NULL,
                avg_rating REAL DEFAULT 5.0,
                product_url TEXT NOT NULL
            )
            """)

            # 2. Customer Orders Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS customer_orders (
                order_id TEXT PRIMARY KEY,
                customer_name TEXT NOT NULL,
                customer_email TEXT NOT NULL,
                product_id TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                total_usd REAL NOT NULL,
                status TEXT NOT NULL,
                carrier TEXT NOT NULL,
                tracking_number TEXT NOT NULL,
                destination_city TEXT NOT NULL,
                estimated_delivery TEXT NOT NULL,
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
            """)

            # Seed Products if empty
            cursor.execute("SELECT COUNT(*) FROM products")
            if cursor.fetchone()[0] == 0:
                products = [
                    (
                        "GL-HW-101",
                        "NVIDIA HGX H100 Enterprise AI Server (8x 80GB SXM5)",
                        "GPU Compute Server",
                        "NVIDIA",
                        "8x H100 80GB SXM5 GPUs, 640GB HBM3, Dual Intel Xeon Platinum, 2TB DDR5, 3.2Tbps InfiniBand",
                        289000.0,
                        0.05,
                        12,
                        4.95,
                        "https://gyanlabs.ai/hardware/hgx-h100"
                    ),
                    (
                        "GL-HW-102",
                        "NVIDIA HGX H200 AI Supercomputing Node (8x 141GB HBM3e)",
                        "GPU Compute Server",
                        "NVIDIA",
                        "8x H200 141GB HBM3e (1.1TB Aggregate VRAM), 4.8TB/s Bandwidth, Liquid-Cooled",
                        345000.0,
                        0.0,
                        6,
                        5.0,
                        "https://gyanlabs.ai/hardware/hgx-h200"
                    ),
                    (
                        "GL-HW-103",
                        "NVIDIA GB200 NVL72 Rack-Scale AI Supercluster",
                        "GPU Compute Server",
                        "NVIDIA",
                        "72x Blackwell GPUs + 36x Grace CPUs, 30TB Fast Memory, 1.4 Exaflops FP4 AI Inference",
                        2450000.0,
                        0.0,
                        2,
                        5.0,
                        "https://gyanlabs.ai/hardware/gb200-nvl72"
                    ),
                    (
                        "GL-HW-104",
                        "NVIDIA L40S PCIe Accelerator Node (4x 48GB GDDR6)",
                        "Inference Server",
                        "NVIDIA",
                        "4x L40S 48GB GPUs, Ada Lovelace Architecture, Optimized for vLLM & Generative Video",
                        48500.0,
                        0.08,
                        24,
                        4.85,
                        "https://gyanlabs.ai/hardware/l40s-node"
                    ),
                    (
                        "GL-WS-201",
                        "Apple MacBook Pro 16\" AI Developer Edition (M3 Max, 128GB)",
                        "Developer Workstation",
                        "Apple",
                        "M3 Max 16-Core CPU, 40-Core GPU, 128GB Unified Memory, 4TB SSD, Liquid Retina XDR",
                        4899.0,
                        0.05,
                        45,
                        4.92,
                        "https://gyanlabs.ai/hardware/macbook-pro-m3max"
                    ),
                    (
                        "GL-WS-202",
                        "Dell Precision 7960 Tower (Dual RTX 6000 Ada 96GB VRAM)",
                        "Developer Workstation",
                        "Dell",
                        "Dual NVIDIA RTX 6000 Ada (96GB VRAM), Intel Xeon w9-3495X 56-Core, 256GB DDR5, 8TB NVMe",
                        26500.0,
                        0.10,
                        18,
                        4.88,
                        "https://gyanlabs.ai/hardware/dell-precision-7960"
                    ),
                    (
                        "GL-WS-203",
                        "Lenovo ThinkStation P8 (AMD Threadripper PRO 96-Core)",
                        "Developer Workstation",
                        "Lenovo",
                        "AMD Ryzen Threadripper PRO 7995WX (96 Cores, 192 Threads), 512GB ECC RAM, 3x RTX 4090",
                        31200.0,
                        0.07,
                        14,
                        4.90,
                        "https://gyanlabs.ai/hardware/lenovo-thinkstation-p8"
                    ),
                    (
                        "GL-ED-301",
                        "NVIDIA Jetson AGX Orin 64GB Developer Kit (275 TOPS)",
                        "Edge AI Device",
                        "NVIDIA",
                        "275 TOPS AI Performance, 2048-core Ampere GPU, 64GB 256-bit LPDDR5, Industrial Enclosure",
                        1999.0,
                        0.05,
                        80,
                        4.80,
                        "https://gyanlabs.ai/hardware/jetson-agx-orin"
                    ),
                    (
                        "GL-SEC-401",
                        "YubiKey 5C NFC Enterprise Security Hardware Key (10-Pack)",
                        "Zero-Trust Security",
                        "Yubico",
                        "FIDO2/WebAuthn, U2F, Smart Card (PIV), USB-C and NFC, Hardware Cryptographic Protection",
                        700.0,
                        0.12,
                        150,
                        4.98,
                        "https://gyanlabs.ai/hardware/yubikey-5c-enterprise"
                    ),
                    (
                        "GL-ACC-501",
                        "Dell UltraSharp 32\" 6K Thunderbolt 4 Hub Monitor (U3224KB)",
                        "Peripherals & Displays",
                        "Dell",
                        "6K Resolution (6144 x 3456), IPS Black Technology, Built-in 4K HDR Webcam, 140W PD",
                        2599.0,
                        0.15,
                        35,
                        4.75,
                        "https://gyanlabs.ai/hardware/dell-ultrasharp-6k"
                    ),
                    (
                        "GL-ACC-502",
                        "Logitech MX Master 3S + MX Mechanical Wireless Bundle",
                        "Peripherals & Displays",
                        "Logitech",
                        "8K DPI Any-surface tracking, Quiet Clicks, Mechanical Tactile Quiet Switches, Flow Cross-computer",
                        279.0,
                        0.10,
                        120,
                        4.89,
                        "https://gyanlabs.ai/hardware/logitech-mx-bundle"
                    )
                ]
                cursor.executemany("INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", products)

            # Seed Orders if empty
            cursor.execute("SELECT COUNT(*) FROM customer_orders")
            if cursor.fetchone()[0] == 0:
                orders = [
                    (
                        "GL-ORD-8821",
                        "Alexandre Tremblay",
                        "alexandre.t@vectorinstitute.ai",
                        "GL-HW-101",
                        1,
                        274550.0,
                        "Shipped",
                        "FedEx Freight Priority",
                        "FX-9982410294",
                        "Toronto, ON (Canada)",
                        "2026-08-22"
                    ),
                    (
                        "GL-ORD-8822",
                        "Sarah Lin",
                        "s.lin@stanford-ai.edu",
                        "GL-WS-201",
                        3,
                        13962.15,
                        "In Transit",
                        "UPS Express Saver",
                        "1Z-88492049102",
                        "San Francisco, CA (United States)",
                        "2026-08-20"
                    ),
                    (
                        "GL-ORD-8823",
                        "David Tremblay",
                        "dtremblay@mila.quebec",
                        "GL-ED-301",
                        5,
                        9495.25,
                        "Delivered",
                        "Canada Post Xpresspost",
                        "CP-774920194CA",
                        "Montreal, QC (Canada)",
                        "2026-08-16"
                    ),
                    (
                        "GL-ORD-8824",
                        "Marcus Vance",
                        "m.vance@quantum-ai.io",
                        "GL-SEC-401",
                        2,
                        1232.0,
                        "Processing",
                        "FedEx Standard Overnight",
                        "FX-4491029482",
                        "Seattle, WA (United States)",
                        "2026-08-24"
                    )
                ]
                cursor.executemany("INSERT INTO customer_orders VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", orders)

            conn.commit()

    def get_schema(self) -> str:
        """
        Extracts table schemas for LLM context prompting.
        """
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
            rows = cursor.fetchall()
            return "\n\n".join(f"-- Table: {name}\n{sql};" for name, sql in rows)

    def execute_query(self, sql_query: str) -> Dict[str, Any]:
        """
        Executes a sanitized read-only SQL query against the SQLite database.
        """
        clean_sql = sql_query.strip().strip(";")
        first_word = clean_sql.split()[0].upper() if clean_sql else ""
        if first_word != "SELECT" and first_word != "WITH":
            raise ValueError("Security Policy: Only read-only SELECT queries are permitted.")

        with sqlite3.connect(str(self.db_path)) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(clean_sql)
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description] if cursor.description else []
            data = [dict(row) for row in rows]

            return {
                "columns": columns,
                "rows": data,
                "row_count": len(data),
                "sql": clean_sql
            }
