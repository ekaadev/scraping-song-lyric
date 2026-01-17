import json
import time
import os
from lyricsgenius import Genius
from dotenv import load_dotenv

# Load env agar token aman
load_dotenv()

# --- KONFIGURASI ---
token = os.getenv("GENIUS_ACCESS_TOKEN")
if not token:
    # Fallback jika tidak ada di .env (sebaiknya gunakan .env)
    token = "MASUKKAN_TOKEN_MANUAL_JIKA_PERLU"

genius = Genius(token)
genius.remove_section_headers = True 
genius.verbose = False

# --- PERSIAPAN FOLDER & FILE ---
output_folder = "dataset"
raw_filename = "raw_lyrics_data.jsonl"
raw_filepath = os.path.join(output_folder, raw_filename)

if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"Folder '{output_folder}' berhasil dibuat.")

# --- LOAD DATA YANG SUDAH ADA (PENTING: Agar data manualmu tidak tertimpa) ---
existing_songs = set()

if os.path.exists(raw_filepath):
    print(f"Mengecek database lama di {raw_filename}...")
    try:
        with open(raw_filepath, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    # Key unik: title + artist (lowercase)
                    key = f"{data['title'].strip().lower()}-{data['artist'].strip().lower()}"
                    existing_songs.add(key)
                except:
                    continue
        print(f"-> Ditemukan {len(existing_songs)} lagu yang sudah tersimpan.")
    except Exception as e:
        print(f"-> Gagal membaca file lama: {e}")
else:
    print("-> Belum ada database lama. Akan membuat baru.")

# --- DATASET LAGU ---
list_songs = [
    # === TOP 50 INDONESIA (Language: id) ===
    {"title": "Sedia Aku Sebelum Hujan", "artist": "Idgitaf", "lang": "id"},
    {"title": "Kota Ini Tak Sama Tanpamu", "artist": "Nadhif Basalamah", "lang": "id"},
    {"title": "Bergema Sampai Selamanya", "artist": "Nadhif Basalamah", "lang": "id"},
    {"title": "Everything U Are", "artist": "Hindia", "lang": "id"},
    {"title": "Monolog", "artist": "Pamungkas", "lang": "id"},
    {"title": "Lesung Pipi", "artist": "Raim Laode", "lang": "id"},
    {"title": "Dan", "artist": "Sheila On 7", "lang": "id"},
    {"title": "Nina", "artist": "The Feast", "lang": "id"},
    {"title": "Tarot", "artist": ".Feast", "lang": "id"},
    {"title": "Orang Baru Lebe Gacor", "artist": "Ecko Show", "lang": "id"},
    {"title": "Kita Usahakan Lagi", "artist": "Batas Senja", "lang": "id"},
    {"title": "Tetap Bukan Kamu", "artist": "Raisa", "lang": "id"},
    {"title": "Gala Bunga Matahari", "artist": "Sal Priadi", "lang": "id"},
    {"title": "Dari Planet Lain", "artist": "Sal Priadi", "lang": "id"},
    {"title": "Satu Bulan", "artist": "Bernadya", "lang": "id"},
    {"title": "Untungnya, Hidup Harus Tetap Berjalan", "artist": "Bernadya", "lang": "id"},
    {"title": "Kata Mereka Ini Berlebihan", "artist": "Bernadya", "lang": "id"},
    {"title": "Mati-Matian", "artist": "Mahalini", "lang": "id"},
    {"title": "Bunga Hati", "artist": "Salma Salsabil", "lang": "id"},
    {"title": "Boleh Juga", "artist": "Salma Salsabil", "lang": "id"},
    {"title": "Sialan", "artist": "Juicy Luicy", "lang": "id"},
    {"title": "Asing", "artist": "Juicy Luicy", "lang": "id"},
    {"title": "Bermuara", "artist": "Rizky Febian", "lang": "id"},
    {"title": "Kupu-Kupu", "artist": "Tiara Andini", "lang": "id"},
    {"title": "Pernikahan Kita", "artist": "Tiara Andini", "lang": "id"},
    {"title": "Tak Dianggap", "artist": "Lyodra", "lang": "id"},
    {"title": "Ego", "artist": "Lyodra", "lang": "id"},
    {"title": "Angin", "artist": "Lomba Sihir", "lang": "id"},
    {"title": "Cincin", "artist": "Hindia", "lang": "id"},
    {"title": "Evaluasi", "artist": "Hindia", "lang": "id"},
    {"title": "Tawan Hati", "artist": "Awdella", "lang": "id"},
    {"title": "Penjaga Hati", "artist": "Nadhif Basalamah", "lang": "id"},
    {"title": "Nanti Kita Seperti Ini", "artist": "Batas Senja", "lang": "id"},
    {"title": "Sial", "artist": "Mahalini", "lang": "id"},
    {"title": "Sisa Rasa", "artist": "Mahalini", "lang": "id"},
    {"title": "Jiwa Yang Bersedih", "artist": "Ghea Indrawari", "lang": "id"},
    {"title": "Nemen", "artist": "GildCoustic", "lang": "id"},
    {"title": "Dumes", "artist": "Denny Caknan", "lang": "id"},
    {"title": "Cinderella", "artist": "Radja", "lang": "id"},
    {"title": "Pupus", "artist": "Dewa 19", "lang": "id"},
    {"title": "Kangen", "artist": "Dewa 19", "lang": "id"},
    {"title": "Risalah Hati", "artist": "Dewa 19", "lang": "id"},
    {"title": "Seberapa Pantas", "artist": "Sheila On 7", "lang": "id"},
    {"title": "Hati-Hati di Jalan", "artist": "Tulus", "lang": "id"},
    {"title": "Interaksi", "artist": "Tulus", "lang": "id"},
    {"title": "Runtuh", "artist": "Feby Putri", "lang": "id"},
    {"title": "Komang", "artist": "Raim Laode", "lang": "id"},
    {"title": "Bertaut", "artist": "Nadin Amizah", "lang": "id"},
    {"title": "Rayuan Perempuan Gila", "artist": "Nadin Amizah", "lang": "id"},
    {"title": "Melukis Senja", "artist": "Budi Doremi", "lang": "id"},

    # === TOP 50 GLOBAL / BARAT (Language: en) ===
    {"title": "Die With A Smile", "artist": "Lady Gaga & Bruno Mars", "lang": "en"},
    {"title": "APT.", "artist": "ROSE & Bruno Mars", "lang": "en"},
    {"title": "Birds of a Feather", "artist": "Billie Eilish", "lang": "en"},
    {"title": "Espresso", "artist": "Sabrina Carpenter", "lang": "en"},
    {"title": "Please Please Please", "artist": "Sabrina Carpenter", "lang": "en"},
    {"title": "Taste", "artist": "Sabrina Carpenter", "lang": "en"},
    {"title": "Good Luck, Babe!", "artist": "Chappell Roan", "lang": "en"},
    {"title": "Beautiful Things", "artist": "Benson Boone", "lang": "en"},
    {"title": "Too Sweet", "artist": "Hozier", "lang": "en"},
    {"title": "We Can't Be Friends (Wait for Your Love)", "artist": "Ariana Grande", "lang": "en"},
    {"title": "End of Beginning", "artist": "Djo", "lang": "en"},
    {"title": "Fortnight", "artist": "Taylor Swift", "lang": "en"},
    {"title": "I Can Do It With a Broken Heart", "artist": "Taylor Swift", "lang": "en"},
    {"title": "Cruel Summer", "artist": "Taylor Swift", "lang": "en"},
    {"title": "Gata Only", "artist": "FloyyMenor", "lang": "en"},
    {"title": "Lunch", "artist": "Billie Eilish", "lang": "en"},
    {"title": "Chihiro", "artist": "Billie Eilish", "lang": "en"},
    {"title": "Si Antes Te Hubiera Conocido", "artist": "Karol G", "lang": "en"},
    {"title": "Not Like Us", "artist": "Kendrick Lamar", "lang": "en"},
    {"title": "Million Dollar Baby", "artist": "Tommy Richman", "lang": "en"},
    {"title": "A Bar Song (Tipsy)", "artist": "Shaboozey", "lang": "en"},
    {"title": "I Had Some Help", "artist": "Post Malone feat. Morgan Wallen", "lang": "en"},
    {"title": "Lose Control", "artist": "Teddy Swims", "lang": "en"},
    {"title": "Greedy", "artist": "Tate McRae", "lang": "en"},
    {"title": "Strangers", "artist": "Kenya Grace", "lang": "en"},
    {"title": "Stick Season", "artist": "Noah Kahan", "lang": "en"},
    {"title": "Vampire", "artist": "Olivia Rodrigo", "lang": "en"},
    {"title": "Deja Vu", "artist": "Olivia Rodrigo", "lang": "en"},
    {"title": "Kill Bill", "artist": "SZA", "lang": "en"},
    {"title": "Snooze", "artist": "SZA", "lang": "en"},
    {"title": "Flowers", "artist": "Miley Cyrus", "lang": "en"},
    {"title": "As It Was", "artist": "Harry Styles", "lang": "en"},
    {"title": "Daylight", "artist": "Harry Styles", "lang": "en"},
    {"title": "Golden Hour", "artist": "JVKE", "lang": "en"},
    {"title": "Until I Found You", "artist": "Stephen Sanchez", "lang": "en"},
    {"title": "Glimpse of Us", "artist": "Joji", "lang": "en"},
    {"title": "Die For You", "artist": "The Weeknd", "lang": "en"},
    {"title": "Starboy", "artist": "The Weeknd", "lang": "en"},
    {"title": "Blinding Lights", "artist": "The Weeknd", "lang": "en"},
    {"title": "Creepin'", "artist": "Metro Boomin", "lang": "en"},
    {"title": "Seven", "artist": "Jungkook", "lang": "en"},
    {"title": "Standing Next to You", "artist": "Jungkook", "lang": "en"},
    {"title": "Paint The Town Red", "artist": "Doja Cat", "lang": "en"},
    {"title": "Water", "artist": "Tyla", "lang": "en"},
    {"title": "Perfect", "artist": "Ed Sheeran", "lang": "en"},
    {"title": "Shape of You", "artist": "Ed Sheeran", "lang": "en"},
    {"title": "Someone You Loved", "artist": "Lewis Capaldi", "lang": "en"},
    {"title": "Yellow", "artist": "Coldplay", "lang": "en"},
    {"title": "Viva La Vida", "artist": "Coldplay", "lang": "en"},
    {"title": "Fix You", "artist": "Coldplay", "lang": "en"},

    # List Tambahan (BATCH 2)
    {"title": "Tak Segampang Itu", "artist": "Anggi Marito", "lang": "id"},
    {"title": "Rumah Singgah", "artist": "Fabio Asher", "lang": "id"},
    {"title": "Dunia Tipu-Tipu", "artist": "Yura Yunita", "lang": "id"},
    {"title": "Bercinta Lewat Kata", "artist": "Donne Maula", "lang": "id"},
    {"title": "Asmalibrasi", "artist": "Soegi Bornean", "lang": "id"},
    {"title": "Waktu Yang Salah", "artist": "Fiersa Besari", "lang": "id"},
    {"title": "Peri Cintaku", "artist": "Ziva Magnolya", "lang": "id"},
    {"title": "Lantas", "artist": "Juicy Luicy", "lang": "id"},
    {"title": "Satu-Satu", "artist": "Idgitaf", "lang": "id"},
    {"title": "Duka", "artist": "Last Child", "lang": "id"},
    {"title": "My Love Mine All Mine", "artist": "Mitski", "lang": "en"},
    {"title": "I Wanna Be Yours", "artist": "Arctic Monkeys", "lang": "en"},
    {"title": "Sweater Weather", "artist": "The Neighbourhood", "lang": "en"},
    {"title": "Heat Waves", "artist": "Glass Animals", "lang": "en"},
    {"title": "Dandelions", "artist": "Ruth B.", "lang": "en"},
    {"title": "Night Changes", "artist": "One Direction", "lang": "en"},
    {"title": "Levitating", "artist": "Dua Lipa", "lang": "en"},
    {"title": "Easy On Me", "artist": "Adele", "lang": "en"},
    {"title": "Unholy", "artist": "Sam Smith & Kim Petras", "lang": "en"},
    {"title": "Heather", "artist": "Conan Gray", "lang": "en"}
]

# Variabel penampung data BARU saja
new_raw_data = []

print(f"\nMemulai proses validasi dan scraping untuk {len(list_songs)} lagu...")

# --- PROSES SCRAPING ---
for i, item in enumerate(list_songs):
    current_key = f"{item['title'].strip().lower()}-{item['artist'].strip().lower()}"
    
    print(f"[{i+1}/{len(list_songs)}] {item['title']} - {item['artist']} ...", end=" ")

    # CEK APAKAH SUDAH ADA?
    if current_key in existing_songs:
        print("SUDAH ADA. (Skip)")
        continue # Lanjut ke lagu berikutnya, tidak usah scraping
    
    # JIKA BELUM ADA, LANJUT SCRAPING
    try:
        print("Scraping...", end=" ")
        song = genius.search_song(item['title'], item['artist'])
        
        if song:
            print("OK!")
            
            # Ambil deskripsi (default dari Genius)
            # Nanti bisa kamu timpa/perbaiki sendiri pakai script AI
            desc = "Tidak ada deskripsi tersedia."
            try:
                if song.description:
                    desc = song.description
            except:
                pass

            clean_lyrics = song.lyrics.strip() if song.lyrics else ""

            if clean_lyrics:
                # Siapkan RAW entry saja
                raw_entry = {
                    "title": item['title'],
                    "artist": item['artist'],
                    "language": item['lang'],
                    "lyrics": clean_lyrics,
                    "theme": "general",
                    "interpretation": desc
                }
                new_raw_data.append(raw_entry)
        else:
            print("Not Found di Genius.")
            
    except Exception as e:
        print(f"Error: {e}")
    
    # Sleep agar tidak kena rate limit
    time.sleep(1.5)

# --- FUNGSI APPEND JSONL ---
def append_to_jsonl(new_data, filepath):
    if not new_data:
        print(f"Tidak ada data baru untuk disimpan di {filepath}.")
        return

    print(f"Menambahkan {len(new_data)} data BARU ke {filepath}...")
    try:
        # Gunakan mode 'a' (append) untuk menambah di baris bawah
        with open(filepath, 'a', encoding='utf-8') as f:
            for entry in new_data:
                json.dump(entry, f, ensure_ascii=False)
                f.write('\n') 
        print(" -> Berhasil ditambahkan.")
    except Exception as e:
        print(f" -> Gagal menyimpan: {e}")

# --- EKSEKUSI PENYIMPANAN ---
# Simpan hanya jika ada data baru
if new_raw_data:
    append_to_jsonl(new_raw_data, raw_filepath)
else:
    print("\nSemua lagu dalam list sudah ada di database. Tidak ada yang perlu disimpan.")

print("\nSelesai! Cek folder 'dataset'.")