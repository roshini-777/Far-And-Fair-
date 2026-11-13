import os
import sys
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "database"))
sys.path.insert(0, os.path.join(BASE_DIR, "backend"))

from db import fetch_all_stays, fetch_stay_by_id
from seed_data import seed_database
from logic import filter_stays, calculate_trip_budget

FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
CORS(app)

# Ensure database is initialized & populated on startup
seed_database(force=False)


def _parse_bool(val):
    return str(val).lower() in ("1", "true", "yes", "on")


@app.route("/")
def serve_index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/api/stays", methods=["GET"])
def get_stays():
    all_stays = fetch_all_stays()

    max_price_raw = request.args.get("max_price")
    max_persons_raw = request.args.get("max_persons")
    duration_raw = request.args.get("duration", 7)
    budget_raw = request.args.get("budget", 15000)

    params = {
        "destination": request.args.get("destination", ""),
        "type": request.args.get("type", "All"),
        "max_price": int(max_price_raw) if max_price_raw and max_price_raw.isdigit() else None,
        "max_persons": int(max_persons_raw) if max_persons_raw and max_persons_raw.isdigit() else None,
        "food_included": _parse_bool(request.args.get("food_included", "false")),
        "wifi": _parse_bool(request.args.get("wifi", "false")),
        "gym": _parse_bool(request.args.get("gym", "false")),
        "laundry": _parse_bool(request.args.get("laundry", "false")),
        "security": _parse_bool(request.args.get("security", "false")),
        "study_room": _parse_bool(request.args.get("study_room", "false")),
    }

    duration = int(duration_raw) if str(duration_raw).isdigit() else 7
    user_budget = int(budget_raw) if str(budget_raw).isdigit() else 15000

    filtered = filter_stays(all_stays, params)
    for stay in filtered:
        stay["budget_breakdown"] = calculate_trip_budget(stay, duration, user_budget)

    return jsonify({
        "count": len(filtered),
        "stays": filtered
    })


@app.route("/api/stays/<int:stay_id>", methods=["GET"])
def get_stay_detail(stay_id):
    stay = fetch_stay_by_id(stay_id)
    if not stay:
        return jsonify({"error": "Accommodation not found"}), 404

    duration = int(request.args.get("duration", 7))
    user_budget = int(request.args.get("budget", 15000))
    stay["budget_breakdown"] = calculate_trip_budget(stay, duration, user_budget)
    return jsonify(stay)


if __name__ == "__main__":
    print("Starting Far & Fair server at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
