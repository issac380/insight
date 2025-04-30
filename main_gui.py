from threading import Thread
from time import sleep

from gui.theft_report_gui import TheftReportGUI
from llm.incident_report import generate_theft_report, set_gui

# Create GUI instance
gui = TheftReportGUI()

# Make it globally available to the report generator
set_gui(gui)

# Start GUI in background
Thread(target=gui.run, daemon=True).start()

# Simulated test data
sample_tags = [
    ("E20047061FE06026BFE10112", {"product": "Aquafina Water", "price": 0.99, "checked_out": False, "current_security": "Locked Shelf"}),
    ("E20047061FE06026BFE10113", {"product": "Laptop", "price": 1299.99, "checked_out": False, "current_security": "Secure Cabinet"}),
]

# Feed reports to the GUI
for tag, info in sample_tags:
    generate_theft_report(tag, info)
    sleep(2)

# Keep the runner alive
while True:
    sleep(1)
