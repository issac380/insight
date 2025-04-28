from data.utils.db_handler import DBHandler
from llm import incident_report
from utils.logger import logger
from data.utils.inventory_loader import get_product_info

# Identifies whether product is paid and calls handling fuctions if not paid.
def unpaid_item(db, tag):
    product_info = get_product_info(tag)
    if not product_info:
        logger.warning(f"Unknown tag detected: {tag}")
        return

    if not product_info['checked_out']:
        if db.record_unpaid_item(tag, product_info):
            incident_report.generate_theft_report(tag, product_info)
