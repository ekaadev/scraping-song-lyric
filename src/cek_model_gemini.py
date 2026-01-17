import os
from dotenv import load_dotenv
from google import genai

# 1. Setup Path
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, "..", ".env")
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

print("--- 🔍 DAFTAR MODEL YANG TERSEDIA ---")

try:
    # Kita panggil list model
    # Dan kita print object-nya langsung atau atribut 'name' saja
    for model in client.models.list():
        # Biasanya format namanya adalah 'models/gemini-1.5-flash'
        print(f"👉 ID Model: {model.name}")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n--- SELESAI ---")