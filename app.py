from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 1. LEAD HUNTER ENGINE (GET)
@app.route('/api/leads', methods=['GET'])
def get_leads():
    return jsonify({
        "results": [{"company": "TechCorp", "email": "hr@techcorp.com", "industry": "AI"}],
        "ISE_Student": "Kruthika R"
    })

# 2. PREDICTIVE SALES ENGINE (POST)
@app.route('/api/predict', methods=['POST'])
def predict_sales():
    import random
    data = request.json
    stock = int(data.get('stock', 0))
    sales = int(data.get('avg_sales', 0))
    
    if sales > 0:
        days_left = round((stock / sales) * (0.95 + random.random() * 0.1), 1)
        status = "High Risk" if days_left < 7 else "Healthy"
    else:
        days_left, status = 0, "Invalid Data"

    return jsonify({"days_remaining": days_left, "status": status})

# 3. SECURE VAULT ENGINE (POST)
@app.route('/api/vault', methods=['POST'])
def access_vault():
    data = request.json
    secret_key = data.get('key', '').lower()
    
    # The 'Decryption' Logic
    if secret_key == "ise2025":
        return jsonify({
            "access": "Granted",
            "decrypted_message": "PROJECT_X: SECURE_ALPHA_v1",
            "security": "AES-256"
        })
    return jsonify({"access": "Denied", "decrypted_message": "********"})

if __name__ == '__main__':
    app.run(debug=True)
