from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_BASE = "http://172.24.0.2:8080"

@app.route("/")
def index():
    return render_template("index.j2")

@app.route("/proxy", methods=["POST"])
def proxy():
    data = request.json

    method = data.get("method")
    endpoint = data.get("endpoint")
    token = data.get("token")
    body = data.get("body")

    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        response = requests.request(
            method=method,
            url=f"{API_BASE}{endpoint}",
            json=body,
            headers=headers
        )

        return jsonify({
            "status": response.status_code,
            "data": response.json() if response.content else {}
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)