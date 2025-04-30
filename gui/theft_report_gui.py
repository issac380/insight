import tkinter as tk
from tkinter import scrolledtext

class TheftReportGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🚨 Theft Incident Monitor")
        self.root.geometry("600x400")

        # Scrolling text area
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=("Courier", 10))
        self.text_area.pack(expand=True, fill='both')

        # Disable user editing
        self.text_area.config(state=tk.DISABLED)

    def append_report(self, report_str):
        # Enable editing, insert text, disable editing again
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, report_str + "\n" + "="*50 + "\n")
        self.text_area.yview(tk.END)  # Auto-scroll to the bottom
        self.text_area.config(state=tk.DISABLED)

    def run(self):
        self.root.mainloop()