# FOR TESTING PUPOSES

import os
import pandas as pd
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompt_loader import load_system_prompt

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
SYSTEM_PROMPT = load_system_prompt(flat_data)

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
