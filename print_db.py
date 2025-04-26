import sqlite3

DB_PATH = 'data/stolen_items.db'

def view_stolen_items():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM stolen_items")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    conn.close()

if __name__ == "__main__":
    view_stolen_items()
