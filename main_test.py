from database.db_handler import init_db
from readers import read_rfid_bluetooth_hid
from process_logic.process_unpaid_item import unpaid_item

if __name__ == "__main__":
    init_db()
    read_rfid_bluetooth_hid.test(unpaid_item)