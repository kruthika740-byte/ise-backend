from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from cryptography.fernet import Fernet # New: Encryption library

app = Flask(__name__)
CORS(app)

# --- SECURITY SETUP ---
# This generates a unique key for the session to handle your "Digital Passport"
key = Fernet.generate_key()
cipher_suite = Fernet(key)

@app.route('/')
def home():
    return jsonify({
        "ISE_Student": "Kruthika R",
        "system_status": "Operational",
        "modules": ["Predictor", "Vault", "Scraper"]
    })

# --- 1. THE SALES PREDICTOR (Data Science Logic) ---
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

# --- 2. THE DIGITAL PASSPORT (Advanced Security Logic) ---
# Encrypts a message into a secure hash
@app.route('/api/vault/encrypt', methods=['POST'])
def encrypt_passport():
    data = request.json
    text_to_hide = data.get('content', '')
    if not text_to_hide:
        return jsonify({"status": "Error", "hash": "No data provided"})
    
    encrypted_text = cipher_suite.encrypt(text_to_hide.encode())
    return jsonify({
        "status": "Encrypted",
        "hash": encrypted_text.decode()
    })

# Decrypts a secure hash back into the original message
@app.route('/api/vault/decrypt', methods=['POST'])
def decrypt_passport():
    data = request.json
    hash_to_decode = data.get('hash', '')
    try:
        decrypted_text = cipher_suite.decrypt(hash_to_decode.encode())
        return jsonify({
            "status": "Decrypted",
            "content": decrypted_text.decode()
        })
    except Exception:
        return jsonify({"status": "Error", "content": "Invalid Hash"})

# --- 3. THE LIVE LEAD HUNTER (Web Scraping Logic) ---
@app.route('/api/leads', methods=['GET'])
def get_leads():
    try:
        url = "https://news.ycombinator.com/show"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Scrape the top trending project title from Hacker News
        first_link = soup.select_one('.titleline > a')
        project_name = first_link.text if first_link else "TechCorp Systems"
        
        return jsonify({
            "results": [{"company": project_name, "status": "Live from HN"}]
        })
    except Exception as e:
        return jsonify({"results": [{"company": "TechCorp", "status": "Offline Cache"}]})

if __name__ == '__main__':
    app.run(debug=True)
