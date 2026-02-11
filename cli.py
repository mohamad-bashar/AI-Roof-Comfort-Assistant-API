# FOR TESTING PUPOSES

import os
import pandas as pd
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. Setup
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    print("❌ Error: GOOGLE_API_KEY not found in .env")
    exit()

client = genai.Client(api_key=API_KEY)

# 2. Load Data (Exactly like your backend)
def load_data():
    try:
        df = pd.read_csv('flats.csv')
        print(f"✅ Loaded {len(df)} flats from CSV.")
        return df.to_string(index=False)
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return ""

flat_data = load_data()

# 3. Define the "Brain"
SYSTEM_PROMPT = f"""
You are the strict Sales AI called "Rashed" for a specific building called "Roof Comfort" your role to users is An Assistant (Yet You Work As A proffessional sales AI). 
You have access to exactly 8 flat types. Here is the ONLY data you know:

{flat_data}

### RULES & BEHAVIOR:
1. **Scope:** You ONLY answer about these flats and building amenities (Gym, Pool, Tennis Court) and Building Location. Refuse all other topics (coding, weather, general life) by saying "I can only help with Roof Comfort inquiries."
2. **Analysis:** - When asked for a specific size/room count, search the data above.
   - If a user asks for "100sqm" and you have 97sqm and 115sqm, suggest both as options.
   - Compare them: "Option A is larger, but Option B has a balcony."
   - Add usfull info : "In these 5 1 bedroom options the options B and D are the largest" etc...
3. **Amenities:** The building has a Gym [IMG-GYM], Pool [IMG-POOL], and Tennis Court [IMG-TENNIS]. Mention these only if relevant.
4. **FORMATTING (CRITICAL):**
   - Only when proposing a specific flat, you MUST end the sentence with its exact 'id' from the 'id' column in brackets. This is critical for the frontend to display images correctly and that is enough you dont need to mention any data about it just the title as the image that will be displayed instead of the brackets has all the data in the table in it.
   - Example: "The Type B is great. [1 Bedroom Type B]"
   - Never make up IDs. Only use the ones in the data.
   - Keep answers concise and professional.
   - If the user asks for data about the building you dont have simply point them to use the contact us page from the nav bar saying such data isnt available to you.
5. **Location:**
   - WADI AL SAFA, DUBAI
   - Wadi Al Safa is strategically located with easy access to major Dubai landmarks and amenities.
   - It's just a short drive from :
        Downtown Dubai
        Dubai Mall
        Burj Khalifa
        Dubai Hills Mall
"""

# 4. The Chat Loop
def start_chat():
    print("\n🏢 --- ROOF COMFORT AI CLI --- 🏢")
    print("Type 'quit' to exit.\n")

    # Chat History (Starts empty)
    chat_history = []

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit"]:
            break

        print("AI is thinking...", end="\r")

        try:
            # Prepare the message for the new SDK
            response = client.models.generate_content(
                model='gemini-2.5-flash', 
                contents=chat_history + [
                    types.Content(role="user", parts=[types.Part(text=user_input)])
                ],
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.3,
                )
            )

            ai_text = response.text
            print(f"AI:  {ai_text}\n")

            # Update History (Manual management for CLI)
            chat_history.append(types.Content(role="user", parts=[types.Part(text=user_input)]))
            chat_history.append(types.Content(role="model", parts=[types.Part(text=ai_text)]))

        except Exception as e:
            print(f"\n❌ API Error: {e}")

if __name__ == "__main__":
    start_chat()