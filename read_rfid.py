import serial
import time
from datetime import datetime

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

def log_to_file(tag_id):
    timestamp = datetime.now().isoformat()
    with open(LOG_FILE, 'a') as f:
        f.write(f'{timestamp},{tag_id}\n')
    print(f'[{timestamp}] Tag read: {tag_id}')

def read_rfid():
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            print(f"Listening on {SERIAL_PORT}...")
            while True:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    log_to_file(line)
    except serial.SerialException as e:
        print(f"Serial error: {e}")

if __name__ == '__main__':
    read_rfid()
