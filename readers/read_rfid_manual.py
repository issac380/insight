from process_logic.process_item import check_item
from utils.logger import logger

# Dumb script, assumes manual worker input, it has a file to preserve abstraction.

def read_rfid_manual(db, tag):
    logger.info(f"Tag scanned: {tag}")
    check_item(db, tag)