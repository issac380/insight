import tkinter as tk
from datetime import datetime
import requests
import csv
import os

from utils.logger import logger  # Import your centralized logger

INVENTORY_FILE = 'data/inventory_status.csv'
BACKEND_URL = "http://localhost:8000/rfid"

def load_inventory():
    inventory = {}
    if not os.path.exists(INVENTORY_FILE):
        logger.warning(f"Inventory file '{INVENTORY_FILE}' not found.")
        return inventory

    with open(INVENTORY_FILE, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                inventory[row['RFID Tag']] = {
                    'product': row['Product Name'],
                    'price': float(row['Price'].strip().replace('$', '')),  # Handle price as float
                    'checked_out': row['Checked Out'].strip().lower() == 'yes',
                    'current_security': row['Current Security'].strip()
                }
            except ValueError as e:
                logger.error(f"Error parsing row for tag {row.get('RFID Tag', 'UNKNOWN')}: {e}")

    logger.info(f"Loaded {len(inventory)} items from inventory.")
    return inventory

def start_bluetooth_listener():
    inventory = load_inventory()

    def on_enter(event):
        tag = entry.get().strip()
        if tag:
            timestamp = datetime.now().isoformat()
            
            if tag in inventory:
                product = inventory[tag]['product']
                price = inventory[tag]['price']
                checked_out = inventory[tag]['checked_out']
                current_security = inventory[tag]['current_security']
                
                if not checked_out:
                    logger.warning(f"🚨 ALERT: '{product}' ({tag}) taken without checkout! Value: ${price}")
                else:
                    logger.info(f"✅ CLEAR: '{product}' ({tag}) scanned at exit.")
            else:
                logger.warning(f"⚠️ Unknown tag scanned: {tag}")
                product = "Unknown"
                checked_out = "Unknown"
                current_security = "Unknown"

            # Optionally send to backend
            # store_rfid_tag(tag)

        entry.delete(0, tk.END)

    def store_rfid_tag(tag):
        payload = {"tag": tag}
        try:
            response = requests.post(BACKEND_URL, json=payload)
            if response.status_code == 200:
                logger.info(f"Tag {tag} stored in backend.")
            else:
                logger.error(f"Backend rejected tag {tag}. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send tag to backend: {e}")

    # ----- Tkinter Setup -----
    root = tk.Tk()
    root.withdraw()

    top = tk.Toplevel()
    top.geometry("1x1+0+0")
    top.attributes("-topmost", True)

    entry = tk.Entry(top)
    entry.pack()
    entry.focus_force()

    entry.bind('<Return>', on_enter)

    logger.info("RFID Bluetooth HID Listener started. Waiting for scans...")
    root.mainloop()

if __name__ == "__main__":
    start_bluetooth_listener()
