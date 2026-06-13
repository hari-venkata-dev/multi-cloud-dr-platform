from flask import Flask, jsonify
import os

app = Flask(__name__)

CLOUD_PROVIDER = os.getenv("CLOUD_PROVIDER", "LOCAL")

@app.route("/")
def home():
    return jsonify({
        "message": "Multi-Cloud DR Platform Running"
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })

@app.route("/cloud-status")
def cloud_status():
    return jsonify({
        "cloud": CLOUD_PROVIDER,
        "status": "active"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)