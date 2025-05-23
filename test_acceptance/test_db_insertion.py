import os
import sqlite3
import pytest
from data.utils.db_handler import DBHandler
from readers.read_rfid_manual import read_rfid_manual
from data.utils.inventory_loader import load_inventory_file
from test_acceptance import test_utils

TEST_DB_PATH = 'test_acceptance/test_data/test_exited_items.db'
TEST_INVENTORY_PATH = 'test_acceptance/test_data/test_inventory_status.csv'

@pytest.fixture(scope="function")
def setup_test_environment():
    # Setup: Initialize DB and load inventory
    db = DBHandler(TEST_DB_PATH)
    load_inventory_file(TEST_INVENTORY_PATH)

    yield db  # Provide db handler to the test

    # Teardown: Remove test DB after test
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

def test_db_insertion(setup_test_environment):
    db = setup_test_environment

    # Simulate RFID scans
    simulated_tags = ["E20047061FE06026BFE10112", "E20047061FE06026BFE10112", "E20047061FE06026BFE10113"]
    for tag in simulated_tags:
        read_rfid_manual(db, tag)

    stolen_db = test_utils.view_exited_items(TEST_DB_PATH)
    
    # Pretty Print
    print("\n📄 Contents of exited_items DB:")
    for row in stolen_db:
        print(f"RFID: {row[0]}, Product: {row[1]}, Price: {row[2]}, Detected At: {row[3]}, Status: {row[4]}, Current Security: {row[5]}")

    paid_tags, unpaid_tags = [], []
    for row in stolen_db:
        if row[4] == "paid":
            paid_tags.append(row[0])
        else:
            unpaid_tags.append(row[0])

    # Assertions: Check that both tags were recorded if unpaid
    assert "E20047061FE06026BFE10112" in unpaid_tags
    assert "E20047061FE06026BFE10113" in paid_tags
