import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = "AIzaSyDOTKHzQiLSVSO2Qy_bb0cAFT9I-goj4lE"

app = Flask(__name__)

# Function to process user query using Google Gemini API
def process_query(user_input):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateText?key={GEMINI_API_KEY}"
    payload = {
        "prompt": {"text": f"Identify if the user is asking about latest phone models: {user_input}"},
        "temperature": 0.7
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get("candidates", [{}])[0].get("output", "")
    return "Error processing query"

# Function to fetch latest phone models from an API
def fetch_latest_phones():
    url = "https://api.mockphone.com/latest"  # Replace with a real API if available
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {"error": "Failed to fetch phone data"}

# Flask route to handle API requests
@app.route("/latest-phones", methods=["GET"])
def latest_phones():
    user_query = request.args.get("query", "What’s the latest phone model?")
    ai_response = process_query(user_query)
    
    if "latest phone" in ai_response.lower():
        phone_data = fetch_latest_phones()
        if "error" in phone_data:
            return jsonify({"error": "Could not retrieve phone data."})
        return jsonify({"latest_phones": [phone["name"] for phone in phone_data]})
    
    return jsonify({"message": "I'm not sure, could you rephrase your question?"})

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
