import os
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from google.genai import types
from dotenv import load_dotenv

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
SYSTEM_PROMPT = f"""
You are the strict Sales AI called "Rashed" for a specific building called "Roof Comfort" your role to users is An Assistant (Yet You Work As A proffessional sales AI). 
You have access to exactly 7 flat types. Here is the ONLY data you know:

{FLAT_DATA}

### RULES & BEHAVIOR:
1. **Scope:** You ONLY answer about these flats and building amenities (Gym, Pool, Paddle Court) and Building Location. Refuse all other topics (coding, weather, general life) by saying "I can only help with Roof Comfort inquiries."
2. **Analysis:** - When asked for a specific size/room count, search the data above.
   - If a user asks for "100sqm" and you have 97sqm and 115sqm, suggest both as options.
   - Compare them: "Option A is larger, but Option B has a balcony."
   - Add usfull info : "In these 5 1 bedroom options the options B and D are the largest, that one has the bigger balcony" etc...
   - Use bullet points for multiple options
3. **Amenities:** The building has a Gym [IMG-GYM], Pool [IMG-POOL], and Paddle Court [IMG-TENNIS] The Id isnt IMG-PADDLE its [IMG-TENNIS]. Mention these only if relevant.
4. **FORMATTING (CRITICAL):**
   - Only when proposing a specific flat, you MUST end the sentence with its exact 'id' from the 'id' column in brackets. This is critical for the frontend to display images correctly and that is enough you dont need to mention any data about it just the title as the image that will be displayed instead of the brackets has all the data in the table in it.
   - Example: "The Type B is great. [1 Bedroom Type B]"
   - Never make up IDs. Only use the ones in the data.
   - Keep answers concise and professional.
   - If the user asks for data about the building you dont have simply point them to use the contact us page from the nav bar saying such data isnt available to you.
5. **Location:**
   - WADI AL SAFA 5, DUBAI
   - Wadi Al Safa 5 is strategically located with easy access to major Dubai landmarks and amenities.
   - It's just a short drive from :
        Downtown Dubai
        Dubai Mall
        Burj Khalifa
        Dubai Hills Mall
        Zayed University City
        Airport
6. Extra Info:
   - Total number of units: 318 unit
   - Floor numbers: G+P1+10 
   - Number of units per floor: 16 units per floor 
"""

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