"""
SDA4 Mock API Service
Provides predictable responses for workshop challenges
"""

from flask import Flask, jsonify, request
import random
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "service": "SDA4 Mock API",
        "status": "running",
        "endpoints": [
            "/weather/<city>",
            "/currency/<base>",
            "/news",
            "/random-status",
            "/slow"
        ]
    })

@app.route('/weather/<city>', methods=['GET'])
def get_weather(city):
    """
    Mock weather API - returns predictable data based on city
    """
    # Deterministic temperature based on city name length
    temp = 10 + (len(city) % 20)
    
    cities_data = {
        "berne": {"temp": 18, "condition": "sunny"},
        "geneva": {"temp": 19, "condition": "sunny"},
        "luzern": {"temp": 20, "condition": "sunny"},
        "stuttgart": {"temp": 21, "condition": "sunny"},
        "frankfurt": {"temp": 22, "condition": "sunny"},
        "munich": {"temp": 23, "condition": "sunny"},
        "hamburg": {"temp": 24, "condition": "sunny"},
        "cologne": {"temp": 25, "condition": "sunny"},
        "dusseldorf": {"temp": 26, "condition": "sunny"},
        "zurich": {"temp": 22, "condition": "sunny"},
        "basel": {"temp": 20, "condition": "sunny"},
        "zurich": {"temp": 22, "condition": "sunny"},
        "london": {"temp": 15, "condition": "rainy"},
        "paris": {"temp": 18, "condition": "cloudy"},
        "berlin": {"temp": 16, "condition": "windy"},
        "rome": {"temp": 25, "condition": "sunny"}
    }
    
    city_lower = city.lower()
    if city_lower in cities_data:
        data = cities_data[city_lower]
    else:
        data = {"temp": temp, "condition": "variable"}
    
    return jsonify({
        "city": city,
        "temperature": data["temp"],
        "condition": data["condition"],
        "humidity": random.randint(40, 80),
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/currency/<base>', methods=['GET'])
def get_currency(base):
    """
    Mock currency API - returns fixed exchange rates
    """
    rates = {
        "USD": {"EUR": 0.85, "GBP": 0.73, "CHF": 0.88, "JPY": 110.5},
        "EUR": {"USD": 1.18, "GBP": 0.86, "CHF": 1.03, "JPY": 130.2},
        "CHF": {"USD": 1.14, "EUR": 0.97, "GBP": 0.83, "JPY": 125.8}
    }
    
    base_upper = base.upper()
    if base_upper not in rates:
        return jsonify({"error": f"Currency {base} not supported"}), 400
    
    return jsonify({
        "base": base_upper,
        "rates": rates[base_upper],
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/news', methods=['GET'])
def get_news():
    """
    Mock news API - returns fake headlines
    """
    headlines = [
        "Local University Teaches Cloud Architecture",
        "Students Master n8n Workflows",
        "New Study Shows Benefits of Structured Logging",
        "Microservices Architecture Gains Popularity",
        "API Integration Simplifies Business Processes",
        "Cloud Computing Revolutionizes Industries",
        "AI-Powered Automation Enhances Efficiency",
        "Blockchain Technology Disrupts Traditional Systems",
        "Quantum Computing Opens New Possibilities",
        "Cybersecurity Threats Remain a Major Concern",
        "Cloud Infrastructure Optimization for Cost Savings",
        "Edge Computing Enables Real-Time Data Processing"
    ]
    
    return jsonify({
        "headlines": random.sample(headlines, 3),
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/random-status', methods=['GET'])
def random_status():
    """
    Randomly returns 200 or 500 (for testing error handling)
    """
    if random.random() > 0.5:
        return jsonify({
            "status": "success",
            "message": "Request succeeded"
        }), 200
    else:
        return jsonify({
            "status": "error",
            "message": "Random failure for testing"
        }), 500

@app.route('/slow', methods=['GET'])
def slow_endpoint():
    """
    Simulates slow API response (for timeout testing)
    """
    import time
    delay = int(request.args.get('delay', 3))
    time.sleep(delay)
    
    return jsonify({
        "message": f"Response delayed by {delay} seconds",
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/echo', methods=['POST'])
def echo():
    """
    Echoes back the request body (useful for webhook testing)
    """
    data = request.get_json()
    return jsonify({
        "echo": data,
        "received_at": datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
