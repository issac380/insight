import sqlite3

def view_exited_items(db_path):
    """
    Connects to the SQLite DB at db_path and returns all exited_items entries.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT RFID_Tag, Product_Name, Price, Detected_At, Status, Current_Security FROM exited_items")
    rows = cursor.fetchall()
    conn.close()
    return rows
