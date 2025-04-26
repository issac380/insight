# Insight Retail
### Revolutionizing retail security and efficiency through agentic AI, real-time data insights, and in-person customer analytics to eliminate theft, optimize operations, and empower smarter decision-making for SMEs.

Codebase Structure
project/
│
├── main.py
├── readers/                    # modular ways to read RFID data (thru bluetooth, usb serial, etc.)
│   ├── __init__.py
│   ├── read_rfid_bluetooth.py
│   └── read_rfid_usb.py
├── data/                       # contains relevant inventory data and log
│   ├── inventory_status.csv
│   └── rfid_logs.csv
├── utils/                      # (future) if we implement backend api
│   ├── logger.py
│   └── api_client.py
└── requirements.txt
