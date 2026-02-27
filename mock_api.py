from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)


def build_bill_card(card_values):
    return {
        "generic": [
            {
                "response_type": "card",
                "body": [
                    {
                        "response_type": "text",
                        "text": "# Bill summary (Feb 2026)",
                    },
                    {
                        "response_type": "grid",
                        "columns": [{"width": "1"}, {"width": "1"}],
                        "rows": [
                            {
                                "cells": [
                                    {
                                        "items": [
                                            {
                                                "response_type": "text",
                                                "text": f"**Total due:** ${card_values['total_due']}",
                                            }
                                        ]
                                    },
                                    {
                                        "items": [
                                            {
                                                "response_type": "text",
                                                "text": f"**Due date:** {card_values['due_date']}",
                                            }
                                        ]
                                    },
                                ]
                            },
                            {
                                "cells": [
                                    {
                                        "items": [
                                            {
                                                "response_type": "text",
                                                "text": f"**New charges:** ${card_values['new_charges']}",
                                            }
                                        ]
                                    },
                                    {
                                        "items": [
                                            {
                                                "response_type": "text",
                                                "text": f"**Last bill:** ${card_values['last_bill']}",
                                            }
                                        ]
                                    },
                                ]
                            },
                            {
                                "cells": [
                                    {
                                        "items": [
                                            {
                                                "response_type": "text",
                                                "text": f"**Plan (1 line):** ${card_values['plan_line']}",
                                            }
                                        ]
                                    },
                                    {
                                        "items": [
                                            {
                                                "response_type": "text",
                                                "text": f"**Administrative Fee:** {card_values['admin_fee']}",
                                            }
                                        ]
                                    },
                                ]
                            },
                            {
                                "cells": [
                                    {
                                        "items": [
                                            {
                                                "response_type": "text",
                                                "text": f"**Hotspot overage:** {card_values['hotspot']}",
                                            }
                                        ]
                                    },
                                    {
                                        "items": [
                                            {
                                                "response_type": "text",
                                                "text": f"**Taxes & surcharges:** {card_values['taxes']}",
                                            }
                                        ]
                                    },
                                ]
                            },
                            {
                                "cells": [
                                    {
                                        "items": [
                                            {
                                                "response_type": "text",
                                                "text": "**What increased:**",
                                            }
                                        ]
                                    },
                                    {
                                        "items": [
                                            {
                                                "response_type": "text",
                                                "text": card_values["what_increased"],
                                            }
                                        ]
                                    },
                                ]
                            },
                        ],
                    },
                ],
            }
        ]
    }


MOCK_USERS = [
    {
        "account_id": "A12345",
        "phone": "4695551234",
        "name": "John Doe",
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
        "bill_card_values": {
            "total_due": "126.55",
            "due_date": "Mar 3, 2026",
            "new_charges": "126.55",
            "last_bill": "88.12 (+$38.43)",
            "plan_line": "65.00",
            "admin_fee": "$15.00 (unchanged)",
            "hotspot": "$35.00 (new)",
            "taxes": "$11.55 (+$3.43)",
            "what_increased": "• Hotspot overage $35.00\n• Taxes/surcharges +$3.43",
        },
        "plan": "Unlimited Starter",
    },
    {
        "account_id": "A67890",
        "phone": "1234512345",
        "name": "Jane Smith",
        "bill": {
            "current_amount": 98.2,
            "due_date": "2026-03-10",
            "last_month": 90.45,
            "breakdown": {
                "plan": 65,
                "device_installment": 10,
                "international_roaming": 0,
                "late_fee": 0,
            },
        },
        "bill_card_values": {
            "total_due": "98.20",
            "due_date": "Mar 10, 2026",
            "new_charges": "98.20",
            "last_bill": "90.45 (+$7.75)",
            "plan_line": "65.00",
            "admin_fee": "$15.00 (unchanged)",
            "hotspot": "$5.00",
            "taxes": "$13.20 (+$2.75)",
            "what_increased": "• Extra hotspot data $5.00\n• Taxes/surcharges +$2.75",
        },
        "plan": "Unlimited Plus",
    },
]


def find_user_by_phone(phone):
    return next((user for user in MOCK_USERS if user["phone"] == phone), None)


def find_user_by_account(account_id):
    return next((user for user in MOCK_USERS if user["account_id"] == account_id), None)


@app.get("/api/health")
def health():
    return jsonify({"ok": True, "service": "verizon-mock-api"})


@app.post("/api/auth")
def auth():
    data = request.get_json(silent=True) or {}
    user = find_user_by_phone(data.get("phone"))
    if user:
        return jsonify(
            {
                "authenticated": True,
                "account_id": user["account_id"],
                "name": user["name"],
            }
        )
    return jsonify({"authenticated": False}), 401


@app.get("/api/billing/<account_id>")
def billing(account_id):
    user = find_user_by_account(account_id)
    if not user:
        return jsonify({"error": "Account not found"}), 404
    return jsonify(user["bill"])


@app.get("/api/billing/card/<account_id>")
def billing_card(account_id):
    user = find_user_by_account(account_id)
    if not user:
        return jsonify({"error": "Account not found"}), 404
    return jsonify(build_bill_card(user["bill_card_values"]))


@app.get("/api/plan/current")
def current_plan():
    default_user = MOCK_USERS[0]
    return jsonify({"plan": default_user["plan"], "price": 65})


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
