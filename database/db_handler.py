import sqlite3
from datetime import datetime
from utils.logger import logger
import os

DB_PATH = 'data/stolen_items.db'
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

def init_db():
    """
    Initializes the SQLite database and creates the stolen_items table if it doesn't exist.
    """
    # Ensure the /data directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    # Connect to SQLite (creates file if it doesn't exist)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create the stolen_items table
    # Status == unresolved      🚨Item detected as unpaid but no action taken yet (default on detection)
    #           reported	    📄 LLM report has been generated and logged
    #           investigating	🕵️ Manual review or further action in progress
    #           resolved	    ✅ Case closed (e.g., false alarm, item recovered, or paid afterward)
    #           dismissed	    ❌ Ignored case (e.g., known issue, test scan)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stolen_items (
            RFID_Tag TEXT PRIMARY KEY,
            Product_Name TEXT,
            Price REAL,
            Detected_At TIMESTAMP,
            Status TEXT
        )
    """)

    conn.commit()
    conn.close()

    logger.info(f"Database initialized at {DB_PATH}")

def record_unpaid_item(tag, product_info):
    now = datetime.now().isoformat()

    try:
        cursor.execute("""
            INSERT OR IGNORE INTO stolen_items (RFID_Tag, Product_Name, Price, Detected_At, Status)
            VALUES (?, ?, ?, ?, ?)
        """, (tag, product_info['product'], product_info['price'], now, 'unresolved'))

        if cursor.rowcount == 1:
            logger.info(f"🚨 New unpaid item recorded: {tag}")
            # Trigger LLM report here if needed
        else:
            logger.info(f"Duplicate scan ignored for: {tag}")

        conn.commit()

    except Exception as e:
        logger.error(f"Database error when processing tag {tag}: {e}")
