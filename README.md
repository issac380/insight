# Insight Retail
### Revolutionizing retail security and efficiency through agentic AI, real-time data insights, and in-person customer analytics to eliminate theft, optimize operations, and empower smarter decision-making for SMEs.

Codebase Structure
project/
│
├── main.py
├── main_test.py
├── data/                       # contains relevant inventory data and log
│   ├── inventory_status.csv
│   └── rfid_logs.csv
├── database/                   # contains database utilities
│   ├── db_handler.py
│   └── test/
├── llm/                        # contains LLM related functionalities
│   ├── business_insights.py
│   ├── incident_report.py
│   └── test/
├── log/                        # contains system logs for debugging
│   └── system.log
├── process_logic/              # contains subsequent logic to handle functionalities
│   ├── process_unpaid_item.py/
│   └── test/
├── readers/                    # modular ways to read RFID data (thru bluetooth, usb serial, etc.)
│   ├── __init__.py
│   ├── read_rfid_bluetooth.py
│   └── read_rfid_usb.py
├── utils/                      # (future) if we implement backend api
│   ├── logger.py
│   └── api_client.py
├── test_acceptance/            # acceptance tests for this project
│   └── ...
└── requirements.txt
