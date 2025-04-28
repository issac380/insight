from database import db_handler
from llm import incident_report
from utils.logger import logger
from data.inventory_loader import get_product_info

def unpaid_item(tag):
    product_info = get_product_info(tag)
    if not product_info:
        logger.warning(f"Unknown tag detected: {tag}")
        return

    if not product_info['checked_out']:
        if db_handler.record_unpaid_item(tag, product_info):
            incident_report.generate_theft_report(tag, product_info)
