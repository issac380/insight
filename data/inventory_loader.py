import csv
import os
from utils.logger import logger

INVENTORY_FILE = 'data/inventory_status.csv'

# Load inventory into memory once
_inventory_data = {}

def load_inventory():
    global _inventory_data

    if not os.path.exists(INVENTORY_FILE):
        logger.error(f"Inventory file '{INVENTORY_FILE}' not found.")
        return

    with open(INVENTORY_FILE, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                _inventory_data[row['RFID Tag']] = {
                    'product': row['Product Name'],
                    'price': float(row['Price'].strip().replace('$', '')),
                    'checked_out': row['Checked Out'].strip().lower() == 'yes',
                    'current_security': row['Current Security'].strip()
                }
            except Exception as e:
                logger.error(f"Error parsing inventory row: {e}")

    logger.info(f"Loaded {_inventory_data.__len__()} inventory items into memory.")

# Call load_inventory() when module is imported
load_inventory()

def get_product_info(tag):
    """
    Returns product info dict if tag exists, else None.
    """
    return _inventory_data.get(tag)
