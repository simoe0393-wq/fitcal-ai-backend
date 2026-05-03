import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env file
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key or api_key == "your_google_key":
    print("❌ Error: GEMINI_API_KEY is not set correctly in .env file.")
    exit(1)

print(f"Testing Gemini API with key: {api_key[:10]}...")

try:
    genai.configure(api_key=api_key)
    # Trying gemini-flash-latest
    model = genai.GenerativeModel('gemini-flash-latest')
    response = model.generate_content("Say hello in one word.")
    
    if response.text:
        print(f"Success! Gemini responded: {response.text.strip()}")
    else:
        print("Error: Gemini returned an empty response.")
        
except Exception as e:
    print(f"Error during API call: {str(e)}")
