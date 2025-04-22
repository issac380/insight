import serial
import time
from datetime import datetime
import requests

# Update this to match your serial port and baud rate
SERIAL_PORT = '/dev/cu.usbserial-XXXX'  # this is based on the RFID (e.g. /dev/cu.usbserial-110 or COM3)

# speed at which data is transmitted over the serial connection (bps)
# 9600 is default that's slow but reliable BUT...
# need to match your reader’s baud rate or else the data will look like gibberish or nothing will be received
# to find the reader’s baud rate, check the manual or datasheet or it's sometimes printed on the device
BAUD_RATE = 9600 

# insight_logs.csv example output:
# 2025-04-18T18:30:25.934001,AB123456
# 2025-04-18T18:30:28.221042,AB123457
LOG_FILE = 'insight_logs.csv'

BACKEND_URL = "http://localhost:8000/rfid"

# Function to read RFID tags from the serial port
def read_from_serial():
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            while True:
                # Read data from the serial port
                line = ser.readline().decode("utf-8").strip()
                if line:
                    print(f"Tag read: {line}")
                    # Send RFID tag to backend to store it in the database
                    store_rfid_tag(line)
                time.sleep(1)  # Wait a bit before reading the next tag
    except serial.SerialException as e:
        print(f"[ERROR] Could not open serial port: {e}")

# Function to send RFID tag to the FastAPI backend
def store_rfid_tag(tag: str):
    payload = {"tag": tag}
    try:
        # Sending the RFID tag to the backend using a POST request
        response = requests.post(BACKEND_URL, json=payload)
        if response.status_code == 200:
            print(f"Tag {tag} successfully stored in the database.")
        else:
            print(f"[ERROR] Failed to store tag: {tag}. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Error sending RFID tag to backend: {e}")

if __name__ == "__main__":
    print("Starting RFID reader...")
    read_from_serial()