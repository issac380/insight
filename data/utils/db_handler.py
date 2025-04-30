import sqlite3
from datetime import datetime
from utils.logger import logger
import os

DEFAULT_DB_PATH = 'data/exited_items.db'

class DBHandler:
    VALID_STATUSES = {'unresolved', 'reported', 'resolved', 'dismissed', 'investigating'}

    def __init__(self, db_path=DEFAULT_DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.init_db()

    def init_db(self):
        """
        Initializes the database and creates the exited_items table if it doesn't exist.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS exited_items (
                RFID_Tag TEXT PRIMARY KEY,
                Product_Name TEXT,
                Price REAL,
                Detected_At TIMESTAMP,
                Status TEXT,
                Current_Security TEXT
            )
        """)
        self.conn.commit()
        logger.info(f"Database initialized at {self.db_path}")

    def record_item(self, tag, product_info, paid):
        """
        Adds new unpaid item to DB. Ignores duplicate scans.
        """
        now = datetime.now().isoformat()
        try:
            if paid:
                self.cursor.execute("""
                    INSERT OR IGNORE INTO exited_items (RFID_Tag, Product_Name, Price, Detected_At, Status, Current_Security)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """, (tag, product_info['product'], product_info['price'], now, 'paid', product_info['current_security']))
            else:
                self.cursor.execute("""
                    INSERT OR IGNORE INTO exited_items (RFID_Tag, Product_Name, Price, Detected_At, Status, Current_Security)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """, (tag, product_info['product'], product_info['price'], now, 'unresolved', product_info['current_security']))

            first_insertion = self.cursor.rowcount == 1

            if first_insertion:
                if paid:
                    logger.info(f"Paid item added to database: {tag}")
                else:
                    logger.info(f"Unpaid item added to database: {tag}")
            else:
                logger.info(f"Duplicate scan ignored for: {tag}")

            self.conn.commit()

            return first_insertion

        except Exception as e:
            logger.error(f"Database error when processing tag {tag}: {e}")

    def update_record_status_by_rfid(self, tag, new_status):
        if new_status not in self.VALID_STATUSES:
            logger.error(f"Invalid status '{new_status}' provided.")
            return
        try:
            self.cursor.execute("""
                UPDATE exited_items
                SET Status = ?
                WHERE RFID_Tag = ?
            """, (new_status, tag))
            self.conn.commit()
            logger.info(f"Updated status for tag {tag} to '{new_status}'")
        except Exception as e:
            logger.error(f"Database error when updating status for tag {tag}: {e}")

    def print_db(self):
        """
        Prints all records in the exited_items table.
        """
        self.cursor.execute("SELECT * FROM exited_items")
        rows = self.cursor.fetchall()
        if rows:
            logger.info("📄 Current Unpaid Items in DB:")
            for row in rows:
                print(row)
        else:
            logger.info("No unpaid items recorded.")

    def close_and_cleanup(self, auto_remove=False):
        """
        Closes DB connection. Removes DB file if auto_remove=True.
        """
        self.conn.close()
        if auto_remove:
            if os.path.exists(self.db_path):
                os.remove(self.db_path)
                logger.info(f"🗑️  Removed database file: {self.db_path}")

