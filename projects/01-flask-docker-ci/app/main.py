import os
import jwt
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
# Importing RSAAlgorithm from PyJWT
#from jwt.algorithms import RSAAlgorithm  # Corrected import statement


# Load environment variables from .env or build args
load_dotenv()

app = Flask(__name__)

# Environment configs
ISSUER = os.getenv("OKTA_ISSUER")
AUDIENCE = os.getenv("OKTA_AUDIENCE")
JWKS_URL = f"{ISSUER}/v1/keys"

# Fetch and cache Okta public keys
jwks = requests.get(JWKS_URL).json()
public_keys = {
    key["kid"]: jwt.algorithms.RSAAlgorithm.from_jwk(key)
    for key in jwks["keys"]
}

def verify_token(token):
    """Decode and verify the Okta-issued JWT"""
    header = jwt.get_unverified_header(token)
    key = public_keys.get(header["kid"])
    if not key:
        raise Exception("Invalid token: key not found.")
    return jwt.decode(
        token,
        key,
        algorithms=["RS256"],
        audience=AUDIENCE,
        issuer=ISSUER
    )

@app.route("/health")
def health_check():
    return jsonify({"status": "ok"})

@app.route("/protected")
def protected():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or malformed token"}), 401

    token = auth_header.split(" ")[1]

    try:
        payload = verify_token(token)
        user_type = payload.get("user_type", "regular")

        if user_type != "admin":
            return jsonify({"error": "Access denied: admin only"}), 403

        return jsonify({
            "message": f"Access granted for {user_type} user",
            "claims": payload
        })

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError as e:
        return jsonify({"error": f"Invalid token: {str(e)}"}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
