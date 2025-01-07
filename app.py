from flask import Flask, render_template, jsonify
from pymongo import MongoClient
from scraper import scrape_trending_data
import os
from dotenv import load_dotenv
from bson import ObjectId

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["twitter_trends"]
collection = db["trends"]

def serialize_objectid(data):
    """Convert ObjectId to string for JSON serialization."""
    if isinstance(data, ObjectId):
        return str(data)
    if isinstance(data, dict):
        return {key: serialize_objectid(value) for key, value in data.items()}
    if isinstance(data, list):
        return [serialize_objectid(item) for item in data]
    return data


@app.route('/')
def home():
    """Render the main HTML page."""
    return render_template('index.html')


@app.route('/run-scraper', methods=['GET'])
def scrape_and_fetch():
    """Run the scraper, store the data in MongoDB, and return it."""
    try:
        latest_data = scrape_trending_data()

        latest_data_serialized = serialize_objectid(latest_data)

        response = {
            "date_time": latest_data_serialized.get("date"),
            "ip_address": latest_data_serialized.get("ip_address"),
            "trends": [
                {"name": trend['name'], "posts": trend['posts']}
                for trend in latest_data_serialized.get("trends", [])
            ],
            "mongo_record": latest_data_serialized,
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
