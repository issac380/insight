import csv
import os
from utils.logger import logger

# Load inventory into memory once
_inventory_data = {}

def load_inventory(inventory_file_path):
    global _inventory_data

    if not os.path.exists(inventory_file_path):
        logger.error(f"Inventory file '{inventory_file_path}' not found.")
        return

    with open(inventory_file_path, mode='r') as csvfile:
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

def get_product_info(tag):
    """
    Returns product info dict if tag exists, else None.
    """
    return _inventory_data.get(tag)
