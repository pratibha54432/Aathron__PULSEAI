#!/usr/bin/env python3
"""Test minimal Flask server"""
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def root():
    return {"status": "ok"}, 200

@app.route("/health", methods=["GET"])
def health():
    return {"healthy": True}, 200

if __name__ == "__main__":
    print("Starting test server on port 8000...")
    app.run(host="0.0.0.0", port=8000, debug=False)
