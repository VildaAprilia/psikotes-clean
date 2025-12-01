# soal/Dominasi_Otak.py
# Variabel yang harus ada: soal_list (list of dict)
# Format tiap dict: {"soal": str, "pilihan": [str, str], "jawaban_benar": str}

soal_list = [
    {"soal": "Anda lebih suka bekerja dengan angka dan data dibandingkan menggambar atau mendesain?",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Otak Kiri"},

    {"soal": "Ketika menyelesaikan masalah, Anda lebih sering menggunakan logika daripada intuisi?",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Otak Kiri"},

    {"soal": "Anda lebih suka membuat daftar tugas secara rinci sebelum bekerja?",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Otak Kiri"},

    {"soal": "Anda mudah mengingat wajah seseorang daripada namanya?",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Otak Kanan"},

    {"soal": "Anda lebih menyukai pekerjaan yang terstruktur dan memiliki aturan jelas?",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Otak Kiri"},

    {"soal": "Anda lebih nyaman dengan ide kreatif dan imajinatif dibandingkan prosedur kerja yang ketat?",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Otak Kanan"},

    {"soal": "Anda lebih cepat memahami penjelasan melalui gambar dibandingkan teks panjang?",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Otak Kanan"},

    {"soal": "Anda senang menganalisis masalah secara logis sebelum mengambil keputusan?",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Otak Kiri"},

    {"soal": "Anda sering menggunakan perasaan untuk menilai suatu situasi?",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Otak Kanan"},

    {"soal": "Anda lebih suka bekerja dengan langkah sistematis dan runtut?",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Otak Kiri"},

    {"soal": "Anda cenderung memperhatikan detail kecil dalam pekerjaan?",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Otak Kiri"},

    {"soal": "Anda lebih tertarik dengan seni, musik, dan warna daripada angka dan perhitungan?",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Otak Kanan"},

    {"soal": "Ketika menghadapi masalah, Anda lebih sering mencari solusi kreatif daripada mengikuti prosedur baku?",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Otak Kanan"},

    {"soal": "Anda lebih nyaman dengan fakta dan data dibandingkan ide abstrak?",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Otak Kiri"},

    {"soal": "Anda lebih menyukai bekerja dalam pola yang fleksibel daripada aturan ketat?",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Otak Kanan"},

    {"soal": "Anda lebih cepat memahami sesuatu melalui pengalaman langsung daripada teori?",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Otak Kanan"},

    {"soal": "Anda merasa lebih nyaman dengan jadwal yang teratur dan terencana?",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Otak Kiri"},

    {"soal": "Anda lebih sering membuat keputusan berdasarkan intuisi dan perasaan?",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Otak Kanan"},

    {"soal": "Anda menikmati menyusun rencana detail untuk mencapai tujuan?",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Otak Kiri"},

    {"soal": "Anda lebih suka berpikir spontan dan mengikuti arus saat bekerja?",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Otak Kanan"},

    {"soal": "Anda lebih senang bekerja dalam angka, data, dan logika?",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Otak Kiri"},

    {"soal": "Anda menikmati pekerjaan yang menuntut kreativitas tinggi?",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Otak Kanan"},

    {"soal": "Anda merasa lebih produktif dalam lingkungan kerja yang tertib dan terorganisir?",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Otak Kiri"},

    {"soal": "Anda lebih mudah memahami konsep melalui visualisasi atau gambar?",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Otak Kanan"},

    {"soal": "Anda lebih percaya pada perasaan pertama Anda dalam mengambil keputusan?",
     "pilihan": ["Ya", "Tidak"], "jawaban_benar": "Otak Kanan"},
]

# 🔹 Fungsi perhitungan skor
def hitung_skor(jawaban_peserta):
    skor_otak_kiri = 0
    skor_otak_kanan = 0

    for i, soal in enumerate(soal_list, start=1):
        key = f"Dominasi_Otak_q{i}"
        jawaban = jawaban_peserta.get(key)
        if jawaban == "Ya":
            if soal["jawaban_benar"] == "Otak Kiri":
                skor_otak_kiri += 1
            else:
                skor_otak_kanan += 1

    if skor_otak_kiri > skor_otak_kanan:
        keterangan = "Dominan Otak Kiri — logis, analitis, sistematis"
    elif skor_otak_kanan > skor_otak_kiri:
        keterangan = "Dominan Otak Kanan — kreatif, intuitif, imajinatif"
    else:
        keterangan = "Seimbang antara Otak Kiri dan Otak Kanan"

    return {"skor": max(skor_otak_kiri, skor_otak_kanan), "keterangan": keterangan}
