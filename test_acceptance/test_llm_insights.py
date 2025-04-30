import os
import pytest
from data.utils.db_handler import DBHandler
from data.utils.inventory_loader import load_inventory_file
from readers.read_rfid_manual import read_rfid_manual
from test_acceptance import test_utils
from llm import security_recommendation

TEST_DB_PATH = 'test_acceptance/test_data/test_exited_items.db'
TEST_INVENTORY_PATH = 'test_acceptance/test_data/test_llm_inventory_status.csv'

@pytest.fixture(scope="function")
def setup_test_environment():
    db = DBHandler(TEST_DB_PATH)
    load_inventory_file(TEST_INVENTORY_PATH)

    yield db  # Provide db handler to the test

    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

def test_large_theft_case(setup_test_environment):
    db = setup_test_environment

    # Simulate scans: all 100 shampoos and all 60 toothbrushes
    simulated_tags = [f"SHAMPOO{i:03}" for i in range(1, 101)] + \
                     [f"TOOTHBRUSH{i:03}" for i in range(1, 61)]

    for tag in simulated_tags:
        read_rfid_manual(db, tag)

    stolen_db = test_utils.view_exited_items(TEST_DB_PATH)

    print("\n📄 Stolen Items Recorded:")
    for row in stolen_db:
        print(f"RFID: {row[0]}, Product: {row[1]}, Price: {row[2]}, Detected At: {row[3]}, Status: {row[4]}, Current Security: {row[5]}")

    paid_tags, unpaid_tags = [], []
    for row in stolen_db:
        if row[4] == "paid":
            paid_tags.append(row[0])
        else:
            unpaid_tags.append(row[0])


    # Ensure only the 80 unpaid shampoos are in the DB
    for i in range(1, 81):
        assert f"SHAMPOO{i:03}" in unpaid_tags

    for i in range(81, 101):
        assert f"SHAMPOO{i:03}" in paid_tags  # Paid

    for i in range(1, 61):
        assert f"TOOTHBRUSH{i:03}" in paid_tags  # All paid

    assert len(unpaid_tags) == 80
    assert len(unpaid_tags) + len(paid_tags) == 160

    llm_response = security_recommendation.generate_security_recommendation(TEST_DB_PATH)
    print(llm_response)