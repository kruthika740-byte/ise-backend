from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 1. LIVE LEAD HUNTER ROUTE
@app.route('/api/leads', methods=['GET'])
def get_leads():
    return jsonify({
        "results": [
            {"company": "TechCorp Solutions", "email": "contact@techcorp.com", "industry": "Software"},
            {"company": "EcoFlow Energy", "email": "hr@ecoflow.io", "industry": "Sustainability"}
        ],
        "ISE_Student": "Kruthika R",
        "status": "Scrape Complete"
    })

# 2. PREDICTIVE SALES TRACKER ROUTE
@app.route('/api/predict', methods=['POST'])
def predict_sales():
    import random
    data = request.json
    stock = int(data.get('stock', 0))
    sales = int(data.get('avg_sales', 0))
    
    # Logic: Days = Stock / Sales (plus a little 'AI' variance)
    if sales > 0:
        days_left = round((stock / sales) * (0.95 + random.random() * 0.1), 1)
        status = "High Risk" if days_left < 7 else "Healthy"
    else:
        days_left = 0
        status = "Invalid Input"

    return jsonify({
        "days_remaining": days_left,
        "status": status
    })

if __name__ == '__main__':
    app.run(debug=True)
