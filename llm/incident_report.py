# llm/incident_report.py

stream_func = None  # Function to send reports to frontend (e.g., via SSE)
logger_func = None  # Optional: could be set to logger.info or similar

def set_stream_function(fn):
    """
    Register a callback function that receives real-time report data.
    Usually points to backend.main.send_theft_report().
    """
    global stream_func
    stream_func = fn

def set_logger_function(fn):
    """
    Optional: register a logger to write reports to file or system log.
    """
    global logger_func
    logger_func = fn

def generate_theft_report(tag, product_info):
    """
    Main report generation function.
    Sends output to configured stream/log handlers and returns the report string.
    """
    report = format_theft_report(tag, product_info)

    if logger_func:
        logger_func(report)
    else:
        print(report)

    if stream_func:
        stream_func(tag, product_info)

    return report

def format_theft_report(tag, product_info):
    """
    Return a plain-text report for internal logging or display.
    """
    return (
        f"🚨 Theft Detected 🚨\n"
        f"RFID Tag: {tag}\n"
        f"Product: {product_info['product']}\n"
        f"Price: ${product_info['price']:.2f}\n"
        f"Status: UNPAID\n"
        f"Investigate unauthorized removal of secured item.\n"
    )
