import sqlite3

def view_stolen_items(db_path):
    """
    Connects to the SQLite DB at db_path and returns all stolen_items entries.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT RFID_Tag, Product_Name, Price, Detected_At, Status FROM stolen_items")
    rows = cursor.fetchall()
    conn.close()
    return rows
