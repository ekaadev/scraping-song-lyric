import json
import time
import os
from lyricsgenius import Genius

# --- KONFIGURASI ---
# Pastikan token ini valid.
token = os.getenv("TOKEN")
if not token:
    raise ValueError("TOKEN tidak ditemukan di environment variables. Silakan set TOKEN di .env atau environment Anda.")
genius = Genius(token)

genius.remove_section_headers = True 
genius.verbose = False

# --- PERSIAPAN FOLDER DATASET ---
# Karena script ini ada di src/, kita asumsikan folder dataset sejajar dengan src/
# Atau berada di root project. Code ini akan membuat folder 'dataset' jika belum ada.
output_folder = "dataset"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"Folder '{output_folder}' berhasil dibuat.")

# --- DATASET LAGU ---
# Saya menambahkan field 'lang' agar model tahu bahasa inputnya
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
    {"title": "Fix You", "artist": "Coldplay", "lang": "en"}
]

# List untuk menampung data
raw_dataset = []
training_dataset = []

print(f"Memulai scraping untuk {len(list_songs)} lagu...")

# --- PROSES SCRAPING ---
for i, item in enumerate(list_songs):
    print(f"[{i+1}/{len(list_songs)}] Processing: {item['title']}...", end=" ")
    
    try:
        song = genius.search_song(item['title'], item['artist'])
        
        if song:
            print("OK")
            # Mengambil deskripsi lagu dari Genius (jika ada) sebagai 'interpretation'
            # Karena song.description kadang return dictionary/None, kita handle safely
            desc = "Tidak ada deskripsi tersedia."
            try:
                if song.description:
                    desc = song.description
            except:
                pass

            # Bersihkan lirik (hapus baris kosong berlebih)
            clean_lyrics = song.lyrics.strip() if song.lyrics else ""

            if clean_lyrics:
                # 1. Format RAW DATASET
                raw_entry = {
                    "title": item['title'],
                    "artist": item['artist'],
                    "language": item['lang'],
                    "lyrics": clean_lyrics,
                    "theme": "general", # Genius tidak selalu menyediakan theme spesifik via API simple
                    "interpretation": desc
                }
                raw_dataset.append(raw_entry)

                # 2. Format TRAINING DATASET
                # input_text: explain_lyric_meaning + lyrics
                # target_text: description/interpretation
                training_entry = {
                    "language": item['lang'],
                    "input_text": f"explain_lyric_meaning:\n{clean_lyrics[:3000]}", # Potong jika terlalu panjang
                    "target_text": desc
                }
                training_dataset.append(training_entry)
        else:
            print("Not Found")
            
    except Exception as e:
        print(f"Error: {e}")
    
    # Sleep agar tidak kena rate limit
    time.sleep(1.5)

# --- FUNGSI SAVE JSONL ---
def save_to_jsonl(data, filename):
    filepath = os.path.join(output_folder, filename)
    print(f"Menyimpan {len(data)} baris ke {filepath}...")
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for entry in data:
                json.dump(entry, f, ensure_ascii=False)
                f.write('\n') # Newline delimiter untuk JSONL
        print(" -> Berhasil.")
    except Exception as e:
        print(f" -> Gagal: {e}")

# --- EKSEKUSI PENYIMPANAN ---
save_to_jsonl(raw_dataset, "raw_lyrics_data.jsonl")
save_to_jsonl(training_dataset, "train_lyrics_finetune.jsonl")

print("\nSelesai! Cek folder 'dataset'.")