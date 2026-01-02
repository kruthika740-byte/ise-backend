from flask import Flask, request, jsonify
from flask_cors import CORS
import requests  # NEW
from bs4 import BeautifulSoup  # NEW

app = Flask(__name__)
CORS(app)

# 1. THE SALES PREDICTOR (Keep this)
@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.json
    stock = int(data.get('stock', 0))
    avg_sales = int(data.get('avg_sales', 1))
    days = stock // avg_sales
    return jsonify({
        "days_remaining": days,
        "status": "Critical" if days < 7 else "Healthy"
    })

# 2. THE SECURE VAULT (Keep this)
@app.route('/api/vault', methods=['POST'])
def vault():
    data = request.json
    if data.get('key') == "ise2025":
        return jsonify({"access": "Granted", "decrypted_message": "ISE_CONFIDENTIAL_2025"})
    return jsonify({"access": "Denied"})

# 3. THE REAL WEB SCRAPER (Update this section)
@app.route('/api/leads', methods=['GET'])
def get_leads():
    try:
        url = "https://news.ycombinator.com/show"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Scrape the top trending project title
        first_link = soup.select_one('.titleline > a')
        project_name = first_link.text if first_link else "No live data"
        
        return jsonify({
            "results": [{"company": project_name, "status": "Live from HN"}]
        })
    except Exception as e:
        return jsonify({"results": [{"company": "Offline Cache", "status": "Using Mock Data"}]})

if __name__ == '__main__':
    app.run(debug=True)
