from data.utils.db_handler import init_db
from readers import read_rfid_bluetooth_hid
from process_logic.process_unpaid_item import unpaid_item
from data.utils.inventory_loader import load_inventory

def run(inventory_file_path='data/inventory_status.csv', start_bluetooth=True):
    init_db()
    load_inventory(inventory_file_path)
    if start_bluetooth:
        read_rfid_bluetooth_hid.start_bluetooth_listener(unpaid_item)
    else:
        read_rfid_bluetooth_hid.test(unpaid_item)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--inventory', default='data/inventory_status.csv', help='Path to inventory CSV')
    parser.add_argument('--test', action='store_true', help='Run in test mode without Bluetooth')
    args = parser.parse_args()

    run(inventory_file_path=args.inventory, start_bluetooth=not args.test)
