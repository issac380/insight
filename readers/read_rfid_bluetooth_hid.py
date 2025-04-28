import tkinter as tk
from utils.logger import logger
from process_logic.process_unpaid_item import unpaid_item

def start_bluetooth_listener(db):
    def on_enter(event):
        tag = entry.get().strip()
        if tag:
            logger.info(f"Tag scanned: {tag}")
            unpaid_item(db, tag)   # Pass tag to processor
        entry.delete(0, tk.END)

    root = tk.Tk()
    root.withdraw()

    top = tk.Toplevel()
    top.geometry("1x1+0+0")
    top.attributes("-topmost", True)

    entry = tk.Entry(top)
    entry.pack()
    entry.focus_force()
    entry.bind('<Return>', on_enter)

    logger.info("Bluetooth HID RFID listener started.")
    root.mainloop()

# called by main_test.py or other testing functions. real workflow will not call this
def test(db):
    tag = "E20047061FE06026BFE10112"
    logger.info(f"Tag scanned: {tag}")
    unpaid_item(db, tag)