from flask import Flask, jsonify
import requests

app = Flask(__name__)

AWS_URL = "http://aws-app:5000"
AZURE_URL = "http://azure-app:5000"

def is_healthy(url):
    try:
        response = requests.get(f"{url}/health", timeout=2)
        return response.status_code == 200
    except requests.RequestException:
        return False

@app.route("/")
def route_traffic():
    if is_healthy(AWS_URL):
        response = requests.get(f"{AWS_URL}/cloud-status")
        return jsonify({
            "routed_to": "AWS",
            "response": response.json()
        })

    response = requests.get(f"{AZURE_URL}/cloud-status")
    return jsonify({
        "routed_to": "AZURE",
        "response": response.json()
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "gateway healthy"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)