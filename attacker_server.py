from flask import Flask, request, jsonify
import logging
import os

app = Flask(__name__)

if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(filename="logs/attacker_server.log", level=logging.INFO, format='%(asctime)s - %(message)s')

@app.route("/<endpoint>", methods=["GET", "POST"])
def capture_data(endpoint):
    data = request.args if request.method == "GET" else request.form
    logging.info(f"Endpoint: {endpoint}, Data: {data}")
    
    return jsonify({"message": f"Data captured at /{endpoint}", "data": data})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
