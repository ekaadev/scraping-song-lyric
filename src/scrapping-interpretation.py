import os
import json
import time
import sys
from dotenv import load_dotenv
from tqdm import tqdm
from google import genai
from google.genai import types
from google.genai.errors import ClientError

# 1. Setup Path
current_dir = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(current_dir, "..", "dataset", "raw_lyrics_data.jsonl")
OUTPUT_FILE = os.path.join(current_dir, "..", "dataset", "dataset_training_ready.jsonl")

# 2. Load API Key
env_path = os.path.join(current_dir, "..", ".env")
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("API Key tidak ditemukan. Cek file .env anda.")

client = genai.Client(api_key=api_key)

# --- KONFIGURASI MODEL ---
ACTIVE_MODEL = "models/gemini-2.5-flash"

def countdown(seconds):
    """Hitung mundur visual jika kena limit"""
    for i in range(seconds, 0, -1):
        sys.stdout.write(f"\r⏳ Limit Harian/Menit. Tunggu {i}s... ")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\r🚀 Lanjut...                        \n")

def process_dataset():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: File input tidak ditemukan di {INPUT_FILE}")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print(f"✅ Menggunakan Model: {ACTIVE_MODEL}")
    print(f"🚀 Memproses {len(lines)} lagu...")

    # --- PERBAIKAN 1: SMART RESUME ---
    # Kita hanya anggap selesai JIKA target_text TIDAK KOSONG.
    processed_lyrics = set()
    if os.path.exists(OUTPUT_FILE):
        print("🔍 Memeriksa file output yang ada (mencari data kosong)...")
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f_out:
            for line in f_out:
                try:
                    existing_data = json.loads(line)
                    t_text = existing_data.get("target_text", "").strip()
                    
                    # HANYA masukan ke daftar "selesai" jika text lebih dari 10 karakter
                    if t_text and len(t_text) > 10:
                        snippet = existing_data['input_text'].replace("explain_lyric_meaning: ", "")[:50]
                        processed_lyrics.add(snippet)
                except:
                    continue
    
    print(f"⏭️  Melewati {len(processed_lyrics)} lagu yang SUDAH VALID. Sisanya (termasuk yang kosong) akan diulang.\n")

    # Buka file dengan mode append
    with open(OUTPUT_FILE, 'a', encoding='utf-8', buffering=1) as outfile:
        
        # Gunakan tqdm
        pbar = tqdm(lines, desc="Processing")
        
        for line in pbar:
            try:
                data = json.loads(line)
                lyrics = data.get("lyrics", "")
                title = data.get("title", "Unknown")
                
                if not lyrics: continue

                # Skip jika sudah ada di daftar VALID
                if lyrics[:50] in processed_lyrics:
                    continue 

                current_interpretation = data.get("interpretation", "")
                target_explanation = ""
                
                # Logic Generate
                if not current_interpretation or current_interpretation == "Tidak ada deskripsi tersedia.":
                    prompt = f"Judul: {data.get('title', 'Lagu')}\nLirik:\n{lyrics}"
                    
                    # Tampilkan judul di progress bar
                    pbar.set_description(f"AI: {title[:15]}...")
                    
                    max_retries = 3
                    for attempt in range(max_retries):
                        try:
                            response = client.models.generate_content(
                                model=ACTIVE_MODEL,
                                contents=prompt,
                                config=types.GenerateContentConfig(
                                    system_instruction="""
                                    Kamu adalah ahli sastra musik. Tugasmu:
                                    1. Jelaskan makna lirik secara mendalam (emosi & metafora).
                                    2. Langsung bahas intinya per bait atau per tema.
                                    3. JANGAN menulis intro basa-basi atau kesimpulan yang mengulang.
                                    4. Buatlah padat, maksimal 300 kata.
                                    Gunakan format Markdown (bold/list).
                                    """,
                                    safety_settings=[
                                        types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_NONE"),
                                        types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_NONE"),
                                        types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_NONE"),
                                        types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_NONE"),
                                    ]
                                )
                            )
                            
                            if response.text:
                                target_explanation = response.text.strip()
                                time.sleep(2) # Wajib sleep agak lama untuk 2.5 Flash
                                break 
                            else:
                                target_explanation = "" # Kosong
                                break

                        except ClientError as e:
                            # Tangkap Error Limit (429)
                            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                                countdown(40) # Tunggu 40 detik
                                continue
                            else:
                                # Error lain, skip lagu ini
                                target_explanation = ""
                                break
                        except Exception:
                            time.sleep(1)
                            continue
                else:
                    target_explanation = current_interpretation

                # --- PERBAIKAN 2: EMPTY GUARD ---
                # JANGAN tulis jika hasilnya kosong atau terlalu pendek
                if not target_explanation or len(target_explanation) < 10:
                    # pbar.set_description(f"⚠️ Skip Kosong: {title[:10]}")
                    continue

                final_data = {
                    "input_text": f"explain_lyric_meaning: {lyrics}",
                    "target_text": target_explanation
                }

                outfile.write(json.dumps(final_data, ensure_ascii=False) + "\n")
                outfile.flush()
                os.fsync(outfile.fileno()) # Paksa simpan ke harddisk

                pbar.set_description("Processing")

            except json.JSONDecodeError:
                continue

    print(f"\n🎉 Selesai! Data siap di: {OUTPUT_FILE}")

if __name__ == "__main__":
    process_dataset()