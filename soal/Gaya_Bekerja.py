# soal/Gaya_Bekerja.py
# Variabel yang harus ada: soal_list (list of dict)
# Format tiap dict: {"soal": str, "pilihan": [str, str], "jawaban_benar": str}

soal_list = [
    {"soal": "Saya lebih mudah memahami sesuatu jika dijelaskan secara lisan.",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Audio"},

    {"soal": "Saya lebih mudah mengingat sesuatu jika menuliskannya.",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Visual"},

    {"soal": "Saya belajar lebih cepat dengan mencoba langsung daripada hanya membaca.",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Kinestetik"},

    {"soal": "Saya suka mendengarkan instruksi daripada membacanya.",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Audio"},

    {"soal": "Saya lebih suka melihat gambar atau diagram daripada membaca teks panjang.",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Visual"},

    {"soal": "Saya memahami informasi lebih baik dengan mendengarkan penjelasan orang lain.",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Audio"},

    {"soal": "Saya suka menonton video tutorial dibandingkan membaca panduan tertulis.",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Visual"},

    {"soal": "Saya belajar dengan lebih baik saat menggerakkan tubuh atau beraktivitas.",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Kinestetik"},

    {"soal": "Saya suka mencatat informasi agar lebih mudah diingat.",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Visual"},

    {"soal": "Saya sering berbicara sendiri untuk mengingat sesuatu.",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Audio"},

    {"soal": "Saya suka belajar dengan menggunakan warna dan gambar.",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Visual"},

    {"soal": "Saya cepat memahami jika seseorang menunjukkan langsung caranya.",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Kinestetik"},

    {"soal": "Saya lebih mudah fokus saat mendengarkan musik pelan saat bekerja.",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Audio"},

    {"soal": "Saya sering meniru gerakan orang lain untuk belajar sesuatu.",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Kinestetik"},

    {"soal": "Saya lebih suka membaca teks daripada mendengarkan ceramah.",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Visual"},

    {"soal": "Saya cepat memahami ketika melihat contoh nyata.",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Kinestetik"},

    {"soal": "Saya lebih suka diskusi dibandingkan membaca materi sendiri.",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Audio"},

    {"soal": "Saya merasa perlu menyentuh atau mencoba alat untuk bisa paham.",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Kinestetik"},

    {"soal": "Saya lebih suka mendengarkan podcast atau audio learning.",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Audio"},

    {"soal": "Saya suka membuat mindmap atau sketsa untuk memahami konsep.",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Visual"}
]

# 🔹 Fungsi perhitungan skor
def hitung_skor(jawaban_peserta):
    audio = visual = kinestetik = 0

    for i, soal in enumerate(soal_list, start=1):
        key = f"Gaya_Bekerja_q{i}"
        jawaban = jawaban_peserta.get(key)
        if jawaban == "Ya":  # hanya hitung jika peserta menjawab "Ya"
            if soal["jawaban_benar"] == "Audio":
                audio += 1
            elif soal["jawaban_benar"] == "Visual":
                visual += 1
            elif soal["jawaban_benar"] == "Kinestetik":
                kinestetik += 1

    # Tentukan gaya dominan
    if audio > visual and audio > kinestetik:
        keterangan = "Gaya belajar dominan: Audio — mudah belajar dengan mendengar dan diskusi."
    elif visual > audio and visual > kinestetik:
        keterangan = "Gaya belajar dominan: Visual — mudah belajar dengan melihat gambar, diagram, dan tulisan."
    elif kinestetik > audio and kinestetik > visual:
        keterangan = "Gaya belajar dominan: Kinestetik — mudah belajar dengan praktik langsung dan pengalaman."
    else:
        keterangan = "Campuran — memiliki gaya belajar yang seimbang antara Audio, Visual, dan Kinestetik."

    total_skor = {"Audio": audio, "Visual": visual, "Kinestetik": kinestetik}
    return {"skor": max(audio, visual, kinestetik), "keterangan": keterangan, "rincian": total_skor}
