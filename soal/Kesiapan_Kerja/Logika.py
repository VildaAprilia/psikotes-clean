# soal/kesiapan_kerja/Logika.py

# Subjudul untuk seluruh subtes ini
SUBJUDUL = "LOGIKA"

soal_list = [
    {
        "soal": "Semua manajer adalah pegawai. Beberapa pegawai adalah wanita. Maka beberapa manajer adalah...?",
        "pilihan": ["Semua manajer wanita", "Beberapa manajer wanita", "Tidak dapat disimpulkan", "Semua pegawai wanita"],
        "jawaban_benar": "Tidak dapat disimpulkan"
    },
    {
        "soal": "Jika A lebih besar dari B dan B lebih besar dari C, maka A ... dari C.",
        "pilihan": ["Lebih besar", "Sama dengan", "Lebih kecil", "Tidak dapat ditentukan"],
        "jawaban_benar": "Lebih besar"
    },
    {
        "soal": "Semua burung bisa terbang. Penguin adalah burung. Maka penguin...?",
        "pilihan": ["Bisa terbang", "Tidak bisa terbang", "Semua burung bisa terbang", "Tidak dapat disimpulkan"],
        "jawaban_benar": "Tidak bisa terbang"
    },
    {
        "soal": "Jika setiap karyawan mendapat bonus, dan Dika adalah karyawan, maka Dika...?",
        "pilihan": ["Tidak mendapat bonus", "Mendapat bonus", "Hanya sebagian mendapat bonus", "Tidak dapat disimpulkan"],
        "jawaban_benar": "Mendapat bonus"
    },
    {
        "soal": "Jika 5 orang memerlukan 10 hari untuk menyelesaikan proyek, maka 10 orang memerlukan...?",
        "pilihan": ["20 hari", "10 hari", "5 hari", "1 hari"],
        "jawaban_benar": "5 hari"
    },
    {
        "soal": "Pernyataan yang salah dari berikut ini adalah:\nA. Semua segitiga punya tiga sisi\nB. Semua lingkaran punya sudut\nC. Semua persegi punya empat sisi",
        "pilihan": ["A. Semua segitiga punya tiga sisi", "B. Semua lingkaran punya sudut", "C. Semua persegi punya empat sisi", "Semua benar"],
        "jawaban_benar": "B. Semua lingkaran punya sudut"
    },
    {
        "soal": "Jika hari ini Rabu, maka dua hari setelah lusa adalah hari...?",
        "pilihan": ["Jumat", "Sabtu", "Minggu", "Kamis"],
        "jawaban_benar": "Sabtu"
    },
    {
        "soal": "Jika 3 mesin menyelesaikan pekerjaan dalam 6 jam, maka 6 mesin menyelesaikan dalam...?",
        "pilihan": ["12 jam", "6 jam", "3 jam", "1 jam"],
        "jawaban_benar": "3 jam"
    },
    {
        "soal": "Jika semua siswa rajin belajar, dan Rani tidak rajin belajar, maka Rani...?",
        "pilihan": ["Masih siswa", "Bukan siswa", "Tetap rajin", "Tidak dapat disimpulkan"],
        "jawaban_benar": "Bukan siswa"
    },
    {
        "soal": "Jika 4 > 3 dan 3 > 2, maka 4 ... 2.",
        "pilihan": ["Lebih besar dari", "Lebih kecil dari", "Sama dengan", "Tidak dapat ditentukan"],
        "jawaban_benar": "Lebih besar dari"
    },
    {
        "soal": "Semua apel adalah buah. Semua buah tumbuh di pohon. Maka semua apel...?",
        "pilihan": ["Tumbuh di pohon", "Tidak tumbuh di pohon", "Hanya sebagian tumbuh di pohon", "Tidak dapat ditentukan"],
        "jawaban_benar": "Tumbuh di pohon"
    },
    {
        "soal": "Jika ada 5 lampu dan 2 mati, berapa lampu yang masih menyala?",
        "pilihan": ["2", "3", "5", "7"],
        "jawaban_benar": "3"
    },
    {
        "soal": "Jika tidak semua kucing berwarna putih, maka kesimpulannya adalah...?",
        "pilihan": ["Semua kucing putih", "Semua kucing tidak putih", "Ada kucing yang tidak putih", "Tidak ada kesimpulan"],
        "jawaban_benar": "Ada kucing yang tidak putih"
    },
    {
        "soal": "Jika A benar maka B salah. Jika A salah maka B benar. Maka A dan B bersifat...?",
        "pilihan": ["Sama", "Berlawanan", "Acak", "Tidak dapat ditentukan"],
        "jawaban_benar": "Berlawanan"
    },
    {
        "soal": "Jika pagi hari suhu 25°C dan sore hari suhu naik 7°C, maka suhu sore hari...?",
        "pilihan": ["30°C", "32°C", "33°C", "25°C"],
        "jawaban_benar": "32°C"
    },
    {
        "soal": "Jika 2x = 10, maka nilai x adalah...?",
        "pilihan": ["2", "5", "10", "12"],
        "jawaban_benar": "5"
    },
    {
        "soal": "Budi lebih tinggi dari Andi, dan Andi lebih tinggi dari Cici. Siapa yang paling pendek?",
        "pilihan": ["Budi", "Andi", "Cici", "Tidak dapat ditentukan"],
        "jawaban_benar": "Cici"
    },
    {
        "soal": "Jika 1 tahun = 12 bulan, maka 3 tahun = ... bulan.",
        "pilihan": ["24", "36", "48", "12"],
        "jawaban_benar": "36"
    },
    {
        "soal": "Jika semua buku di rak adalah milik Andi, dan buku merah di meja bukan di rak, maka buku merah...?",
        "pilihan": ["Milik Andi", "Bukan milik Andi", "Tidak dapat ditentukan", "Milik teman"],
        "jawaban_benar": "Bukan milik Andi"
    },
    {
        "soal": "Urutan logis: Telur - Ayam - Anak ayam - ...",
        "pilihan": ["Ayam dewasa", "Telur lagi", "Anak ayam dewasa", "Tidak ada"],
        "jawaban_benar": "Ayam dewasa"
    },
    {
        "soal": "Jika 100 dibagi 5 hasilnya 20, maka 200 dibagi 10 hasilnya...?",
        "pilihan": ["10", "15", "20", "25"],
        "jawaban_benar": "20"
    },
    {
        "soal": "Jika A adalah ibu dari B, dan B adalah ibu dari C, maka hubungan A dengan C adalah...?",
        "pilihan": ["Ibu", "Nenek", "Kakek", "Saudara"],
        "jawaban_benar": "Nenek"
    },
    {
        "soal": "Kata yang berlawanan dengan 'benar' adalah...?",
        "pilihan": ["Salah", "Tidak benar", "Palsu", "Keliru"],
        "jawaban_benar": "Salah"
    },
    {
        "soal": "Jika 7 hari = 1 minggu, maka 28 hari = ... minggu.",
        "pilihan": ["2", "3", "4", "5"],
        "jawaban_benar": "4"
    },
    {
        "soal": "Jika tidak ada asap maka tidak ada api, maka jika ada api pasti ada...?",
        "pilihan": ["Asap", "Hujan", "Api lagi", "Tidak dapat ditentukan"],
        "jawaban_benar": "Asap"
    }
]
