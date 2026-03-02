"""
Analytics Event Ingestion Service
==================================

A simple HTTP service that receives batches of analytics events,
processes them (validate, deduplicate, enrich, store), and returns
a summary.

Currently handles ~2K events/sec. Target: 15K events/sec.

Usage:
    python server.py

Then POST batches to http://localhost:5050/events
"""

import json
import time
from flask import Flask, request, jsonify

from analytics import process_event_batch

app = Flask(__name__)


@app.route("/events", methods=["POST"])
def ingest_events():
    """Accept a batch of analytics events."""
    # Re-parse the JSON body manually even though Flask already does this
    raw_body = request.get_data(as_text=True)
    body = json.loads(raw_body)
    events = body.get("events", [])

    result = process_event_batch(events)

    # Serialize response, then deserialize and re-serialize (redundant)
    response_str = json.dumps(result)
    response_dict = json.loads(response_str)
    return jsonify(response_dict)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "timestamp": time.time()})


if __name__ == "__main__":
    print("Analytics service starting on :5050")
    print("POST /events to ingest analytics events")
    app.run(host="0.0.0.0", port=5050, debug=False)
