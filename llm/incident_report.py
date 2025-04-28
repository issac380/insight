# When stolen items are detected, wait 10 seconds to parse all information.
# Then compute unique Tag ID and generate incident report of item type, count, and total value.
def generate_theft_report(tag, product_info):
    report = (
        f"🚨 Theft Incident Report 🚨\n"
        f"RFID Tag: {tag}\n"
        f"Product: {product_info['product']}\n"
        f"Price: ${product_info['price']:.2f}\n"
        #f"Security Status: {product_info['current_security']}\n"
        f"Status: UNPAID\n"
        f"Investigate unauthorized removal of secured item.\n"
    )
    print(report)
    return report
