Table Schema:
    CREATE TABLE IF NOT EXISTS exited_items
    RFID_Tag TEXT PRIMARY KEY,
    Product_Name TEXT,
    Price REAL,
    Detected_At TIMESTAMP,
    Status TEXT,
    Current_Security TEXT

    Status == unresolved    🚨 Item detected as unpaid but no action taken yet (default on detection)
              reported	    📄 LLM report has been generated and logged
              investigating	🕵️ Manual review or further action in progress
              resolved	    ✅ Case closed (e.g., false alarm, item recovered, or paid afterward)
              dismissed	    ❌ Ignored case (e.g., known issue, test scan)
              paid          Item is paid

Ideal Workflow:
    Insertion:              All entries will be inserted by calling "db_handler.record_unpaid_item()" as UNRESOLVED
    Report Generation:      Incident reports will be created in real time by incident_report.{FUNC NAME}()
                            This function will change the status of this record to REPORTED via db_handler.update_record_status_by_rfid()
    Report Acknowledgement: When the incident report is received by the human manager, this record will be labeled as INVESTIGATING
    Resolution:             Humans will manually mark entry as RESOLVED 
    Dismissal:              Humans will manually mark entry as DISMISSED 
    TODO: Last 3 workflow are currently not implemented. Function endpoints will be added later.
    
