from data.utils.db_handler import DBHandler
from readers import read_rfid_bluetooth_hid, read_rfid_manual
from data.utils.inventory_loader import load_inventory_file

# ======================================= #
#
#       For testing, CLI:
#       python3 main.py
#
# ======================================= #

def run(stolen_db_path='data/stolen_items.db', inventory_file_path='data/inventory_status.csv'):
    db = DBHandler(stolen_db_path)
    load_inventory_file(inventory_file_path)
    #read_rfid_bluetooth_hid.start_bluetooth_listener(db)
    read_rfid_manual.read_rfid_manual(db, "E20047061FE06026BFE10113")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--inventory', default='data/inventory_status.csv', help='Path to inventory CSV')
    args = parser.parse_args()
    run(inventory_file_path=args.inventory)
