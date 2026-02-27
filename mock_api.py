from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

MOCK_USER = {
    "account_id": "A12345",
    "phone": "4695551234",
    "bill": {
        "current_amount": 142.67,
        "due_date": "2026-03-18",
        "last_month": 119.43,
        "breakdown": {
            "plan": 75,
            "device_installment": 10,
            "international_roaming": 20,
            "late_fee": 5,
        },
    },
    "plan": "Unlimited Starter",
}


@app.get("/api/health")
def health():
    return jsonify({"ok": True, "service": "verizon-mock-api"})


@app.post("/api/auth")
def auth():
    data = request.get_json(silent=True) or {}
    if data.get("phone") == MOCK_USER["phone"]:
        return jsonify({"authenticated": True, "account_id": MOCK_USER["account_id"]})
    return jsonify({"authenticated": False}), 401


@app.get("/api/billing/<account_id>")
def billing(account_id):
    if account_id != MOCK_USER["account_id"]:
        return jsonify({"error": "Account not found"}), 404
    return jsonify(MOCK_USER["bill"])


@app.get("/api/plan/current")
def current_plan():
    return jsonify({"plan": MOCK_USER["plan"], "price": 65})


@app.get("/api/plan/eligible")
def eligible_plan():
    return jsonify(
        {
            "eligible": [
                {"name": "Unlimited Plus", "price": 75},
                {"name": "Unlimited Ultimate", "price": 90},
            ]
        }
    )


@app.post("/api/network/diagnostics")
def diagnostics():
    return jsonify({"status": "area_outage", "eta": "2 hours"})


if __name__ == "__main__":
    port = int(os.getenv("MOCK_API_PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
