# llm/incident_report.py

report_gui = None  # Optional global GUI handler injected by main/test runner

def set_gui(gui_instance):
    """
    Injects the GUI instance for real-time display.
    """
    global report_gui
    report_gui = gui_instance

def generate_theft_report(tag, product_info):
    """
    Formats and optionally displays a theft report for the given RFID tag.
    Only unpaid items should be passed to this function.
    """
    report = format_theft_report(tag, product_info)

    if report_gui:
        report_gui.append_report(report)

    print(report)  # Still print for console visibility or logging
    return report

def format_theft_report(tag, product_info):
    """
    Returns a formatted theft report string.
    """
    return (
        f"🚨 Theft Detected 🚨\n"
        f"RFID Tag: {tag}\n"
        f"Product: {product_info['product']}\n"
        f"Price: ${product_info['price']:.2f}\n"
        f"Status: UNPAID\n"
        f"Investigate unauthorized removal of secured item.\n"
    )
