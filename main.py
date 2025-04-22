from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import serial
import threading

# Define the request model for storing RFID tags
class RFIDTagRequest(BaseModel):
    tag: str

@app.post("/rfid")
def post_rfid_tag(request: RFIDTagRequest):
    # Store the RFID tag in the database
    store_rfid_tag(request.tag)
    return JSONResponse(content={"message": "RFID tag stored successfully."}, status_code=200)

app = FastAPI()

# Database setup
DATABASE_URL = "sqlite:///./rfid_tags.db"  # SQLite database file

# Create database connection and session
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# RFID Tag Model
class RFIDTag(Base):
    __tablename__ = "rfid_tags"
    
    id = Column(Integer, primary_key=True, index=True)
    tag = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Create the table in the database
Base.metadata.create_all(bind=engine)

# Serial port config
SERIAL_PORT = "/dev/ttyUSB0"  # change this based on your device
BAUD_RATE = 9600

# Store all scanned tags in memory (for quick access)
rfid_data = {
    "tags": []
}

# Function to read RFID tags from serial port
def read_from_serial():
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            while True:
                line = ser.readline().decode("utf-8").strip()
                if line:
                    print(f"Tag read: {line}")
                    store_rfid_tag(line)
                    rfid_data["tags"].append(line)
    except serial.SerialException as e:
        print(f"[ERROR] Could not open serial port: {e}")

# Function to store the RFID tag in the database
def store_rfid_tag(tag: str):
    db = SessionLocal()
    db_tag = RFIDTag(tag=tag)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    db.close()

# Start background reader
threading.Thread(target=read_from_serial, daemon=True).start()

# FastAPI endpoint to get all RFID tags
@app.get("/rfid")
def get_all_tags():
    db = SessionLocal()
    tags = db.query(RFIDTag).order_by(RFIDTag.timestamp.desc()).all()
    db.close()
    return JSONResponse(content={"tags": [{"tag": t.tag, "timestamp": t.timestamp} for t in tags]})
