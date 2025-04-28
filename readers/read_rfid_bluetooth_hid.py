import tkinter as tk
from utils.logger import logger

def start_bluetooth_listener(process_function):
    def on_enter(event):
        tag = entry.get().strip()
        if tag:
            logger.info(f"Tag scanned: {tag}")
            process_function(tag)   # Pass tag to processor
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
def test(process_function):
    tag = "E20047061FE06026BFE10112"
    logger.info(f"Tag scanned: {tag}")
    process_function(tag)