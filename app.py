from flask import Flask, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
# CORS allows your GitHub portfolio to fetch data from this local server
CORS(app) 

# This is your "Lead Hunting" API Endpoint
@app.route('/api/leads', methods=['GET'])
def get_leads():
    try:
        # Simulated database of business leads
        database = [
            {"company": "TechStream", "email": "contact@techstream.io", "industry": "IT"},
            {"company": "Global Logistics", "email": "info@globallog.com", "industry": "Shipping"},
            {"company": "Creative Pulse", "email": "hello@cpulse.design", "industry": "Marketing"},
            {"company": "Eco-Build", "email": "sales@ecobuild.net", "industry": "Construction"}
        ]
        
        # Logic: Randomly select 2 leads from the database
        found_leads = random.sample(database, k=2)
        
        # Return the data as a JSON response
        return jsonify({
            "status": "success",
            "ISE_Student": "Kruthika R",
            "results": found_leads
        })
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    # Running on port 5000 with debug mode enabled
    app.run(debug=True, port=5000)