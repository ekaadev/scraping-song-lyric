# Create Dataset LME

## Flow Create Dataset
```
1. Hit endpoint /search pada Genius API dengan parameter query yang sudah di list.
2. Ambil objek song.url dari response Genius API.
3. Hit endpoint song.url untuk mendapatkan halaman lirik lagu.
4. Parse halaman lirik lagu untuk mendapatkan teks lirik.
5. Simpan teks lirik ke dalam dataset dengan format yang diinginkan
```

## List Lagu untuk Query Genius API