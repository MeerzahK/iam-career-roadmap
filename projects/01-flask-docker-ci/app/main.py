from dotenv import load_dotenv
load_dotenv()

import os

ISSUER = os.getenv("OKTA_ISSUER")
AUDIENCE = os.getenv("OKTA_AUDIENCE")

from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/health")
def health_check():
    return jsonify({"status": "ok", "service": "iam-demo"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
