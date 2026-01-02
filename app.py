from flask import Flask, request, jsonify
from flask_cors import CORS
from cryptography.fernet import Fernet
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

# 1. SECURITY MODULE SETUP
# In production, you would store this key in an Environment Variable
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# 2. SMART RESUME DATA (Knowledge Base)
RESUME_DATA = {
    "identity": {
        "name": "Kruthika R",
        "title": "Information Science Engineer",
        "location": "Bengaluru, India"
    },
    "skills": ["Python", "Flask", "Tailwind CSS", "AES-256 Encryption", "Web Scraping", "Cloud Deployment"],
    "projects": {
        "passport": "Digital Passport: A secure AES-256 encryption handshake system.",
        "hunter": "Lead Hunter: A real-time web scraper using BeautifulSoup4.",
        "ops": "Predictive Ops: A logistics engine for stock forecasting."
    },
    "education": "Information Science Engineering student with a focus on Full-Stack Security."
}

# --- SMART RESUME ENDPOINT ---
@app.route('/api/ask_resume', methods=['POST'])
def ask_resume():
    data = request.json
    query = data.get('query', '').lower()
    
    # Logic: Intelligent Keyword Mapping
    if any(word in query for word in ["skill", "know", "tech", "stack"]):
        answer = f"Kruthika is specialized in {', '.join(RESUME_DATA['skills'])}."
    elif any(word in query for word in ["project", "build", "create", "passport", "hunter"]):
        answer = f"Her main projects include: {RESUME_DATA['projects']['passport']} and {RESUME_DATA['projects']['hunter']}."
    elif any(word in query for word in ["education", "college", "study"]):
        answer = RESUME_DATA['education']
    elif any(word in query for word in ["contact", "hire", "email"]):
        answer = "You can reach Kruthika via the contact form on this website or through her LinkedIn profile."
    else:
        answer = "I'm Kruthika's AI Assistant. You can ask me about her skills, projects, or education!"

    return jsonify({"answer": answer})

# --- DIGITAL PASSPORT ENDPOINTS ---
@app.route('/api/vault/encrypt', methods=['POST'])
def encrypt_vault():
    content = request.json.get('content', '')
    token = cipher_suite.encrypt(content.encode())
    return jsonify({"hash": token.decode()})

@app.route('/api/vault/decrypt', methods=['POST'])
def decrypt_vault():
    hash_token = request.json.get('hash', '')
    try:
        decrypted_text = cipher_suite.decrypt(hash_token.encode()).decode()
        return jsonify({"content": decrypted_text})
    except:
        return jsonify({"content": "Error: Invalid Hash"}), 400

# --- LEAD HUNTER ENDPOINT ---
@app.route('/api/leads', methods=['GET'])
def get_leads():
    # Scraping a sample tech news title as a "Lead"
    url = "https://news.ycombinator.com/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    first_story = soup.find('span', class_='titleline').find('a').text
    return jsonify({"results": [{"company": first_story, "status": "New Opportunity"}]})

# --- PREDICTIVE OPS ENDPOINT ---
@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.json
    stock = float(data.get('stock', 0))
    avg_sales = float(data.get('avg_sales', 1))
    days_left = round(stock / avg_sales) if avg_sales > 0 else 0
    return jsonify({"days_remaining": days_left})

# --- HEALTH CHECK ---
@app.route('/')
def home():
    return jsonify({"status": "Online", "engineer": "Kruthika R", "role": "ISE"})

if __name__ == '__main__':
    app.run(debug=True)
