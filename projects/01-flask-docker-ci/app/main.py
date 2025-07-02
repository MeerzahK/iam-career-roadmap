from flask import Flask, request, jsonify
import jwt
import requests
import os
import json
from dotenv import load_dotenv
from jwt.algorithms import RSAAlgorithm

load_dotenv()

app = Flask(__name__)

ISSUER = os.getenv("OKTA_ISSUER")
AUDIENCE = os.getenv("OKTA_AUDIENCE")
JWKS_URL = f"{ISSUER}/v1/keys"

# Cache the public keys
jwks = requests.get(JWKS_URL).json()
public_keys = {}
for key in jwks["keys"]:
    public_keys[kid] = RSAAlgorithm.from_jwk(json.dumps(key))
    public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key))

def verify_token(token):
    header = jwt.get_unverified_header(token)
    rsa_key = public_keys.get(header["kid"])
    return jwt.decode(token, rsa_key, algorithms=["RS256"], audience=AUDIENCE, issuer=ISSUER)

@app.route("/protected")
def protected():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or malformed token"}), 401

    token = auth_header.split(" ")[1]
    try:
        payload = verify_token(token)

        scopes = payload.get("scp", [])
        if "read" not in scopes:
            return jsonify({"error": "Missing required scope: read"}), 403

        return jsonify({
            "message": "Access granted with scope 'read'",
            "scopes": scopes,
            "claims": payload
        })

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError as e:
        return jsonify({"error": str(e)}), 403

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
