from data.utils.db_handler import DBHandler
from readers import read_rfid_bluetooth_hid
from data.utils.inventory_loader import load_inventory_file

# ======================================= #
#
#       For testing, CLI:
#       python3 main.py
#
# ======================================= #

def run(inventory_file_path='data/inventory_status.csv', start_bluetooth=True):
    db = DBHandler(db_path='test_acceptance/test_data/stolen_items_test.db')
    load_inventory_file(inventory_file_path)
    if start_bluetooth:
        read_rfid_bluetooth_hid.start_bluetooth_listener(db)
    else:
        read_rfid_bluetooth_hid.test(db)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--inventory', default='data/inventory_status.csv', help='Path to inventory CSV')
    parser.add_argument('--test', action='store_true', help='Run in test mode without Bluetooth')
    args = parser.parse_args()
    run(inventory_file_path=args.inventory, start_bluetooth=not args.test)
