from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

# Connect to MongoDB (container name 'mongodb')
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017/")
client = MongoClient(MONGO_URI)
db = client["date_records_db"]
collection = db["dates"]

@app.route("/health", methods=["GET"])
def health_check():
    try:
        client.admin.command('ping')
        return jsonify({"status": "healthy"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500
        
@app.route("/save", methods=["POST"])
def save_data():
    try:
        data = request.get_json()
        date_value = data.get("date")

        if not date_value:
            return jsonify({"error": "Missing 'date' field"}), 400

        collection.insert_one({
            "date": date_value,
            "timestamp": datetime.utcnow()
        })
        return jsonify({"message": "Date saved successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/list", methods=["GET"])
def list_dates():
    try:
        records = list(collection.find({}, {"_id": 0}))
        return jsonify(records)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

