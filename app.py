import os
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from google.genai import types
from dotenv import load_dotenv
from prompt_loader import load_system_prompt

# 1. Setup & Security
load_dotenv() # Loads API key from .env file
app = Flask(__name__)
CORS(app) # Allows your frontend to talk to this backend

# Configure Gemini
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# 2. Load and Format Data (Runs once when server starts)
def load_context():
    try:
        df = pd.read_csv('flats.csv')
        # Convert CSV to a clean string representation for the AI
        data_string = df.to_string(index=False)
        return data_string
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return "Error: Could not load flat data."

FLAT_DATA = load_context()

# 3. The "Brain" - System Instructions
SYSTEM_PROMPT = load_system_prompt(FLAT_DATA)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    raw_history = data.get('history', [])

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # 3. NEW CHAT STRUCTURE
        # The new SDK handles history slightly differently. 
        # We need to convert your JS history into the format the new SDK expects.
        formatted_history = []
        
        # Convert incoming JSON history to Google's "Content" format
        for msg in raw_history:
            role = "user" if msg['role'] == "user" else "model"
            formatted_history.append(
                types.Content(
                    role=role,
                    parts=[types.Part(text=msg['parts'][0]['text'])]
                )
            )

        # 4. GENERATE CONTENT
        # In the new SDK, we use client.models.generate_content
        # We send the system prompt in the 'config'
        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=formatted_history + [
                types.Content(role="user", parts=[types.Part(text=user_message)])
            ],
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.3 # Keep it factual
            )
        )

        return jsonify({
            "response": response.text
        })

    except Exception as e:
        print(f"API Error: {e}")
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)
