# backend/main.py

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import time
import json
import threading
import queue

# Thread-safe queue to hold theft reports
report_queue = queue.Queue()

app = FastAPI()

# Allow frontend (e.g., React on localhost:3000) to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev, allow all; restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/stream")
async def stream_reports():
    """
    Server-Sent Events endpoint that streams theft reports in real time.
    """
    def event_stream():
        while True:
            try:
                report = report_queue.get(timeout=1)
                yield f"data: {json.dumps(report)}\n\n"
            except queue.Empty:
                continue

    return StreamingResponse(event_stream(), media_type="text/event-stream")

# Called from elsewhere (e.g., process logic or test sim)
def send_theft_report(tag, product_info):
    """
    Queues a theft report for front-end display.
    """
    report = {
        "tag": tag,
        "product": product_info["product"],
        "price": float(product_info["price"]),
        "message": "Investigate unauthorized removal of secured item."
    }
    report_queue.put(report)

# Optional: demo mode with fake data
def simulate_reports():
    sample_data = [
        ("TAG001", {"product": "Laptop", "price": 1299.99}),
        ("TAG002", {"product": "Aquafina Water", "price": 0.99}),
        ("TAG003", {"product": "Backpack", "price": 75.00}),
    ]

    for tag, info in sample_data:
        send_theft_report(tag, info)
        time.sleep(3)  # Simulate delay between incidents

# Run simulator if script is launched directly
if __name__ == "__main__":
    print("👀 Simulating reports...")
    threading.Thread(target=simulate_reports, daemon=True).start()

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
