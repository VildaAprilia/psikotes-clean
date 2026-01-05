soal_list = [
    {
        "no": 1,
        "soal": "Bagaimana Anda menyelesaikan tugas jika tidak ada rekan kerja yang bisa membantu?",
        "jawaban_ideal": "Berusaha menyelesaikan sendiri dan mencari solusi alternatif",
        "opsi": ["Mandiri dan proaktif", "Cukup mandiri", "Sering bergantung pada orang lain", "Tidak mandiri dan pasif"],
        "skor": {
            4: "Mandiri dan proaktif",
            3: "Cukup mandiri",
            2: "Sering bergantung pada orang lain",
            1: "Tidak mandiri dan pasif"
        }
    },
    {
        "no": 2,
        "soal": "Apa yang Anda lakukan ketika harus mengambil keputusan mendadak di tempat kerja?",
        "jawaban_ideal": "Mengambil keputusan berdasarkan logika dan pengalaman",
        "opsi": ["Mandiri dan proaktif", "Cukup mandiri", "Sering bergantung pada orang lain", "Tidak mandiri dan pasif"],
        "skor": {
            4: "Mandiri dan proaktif",
            3: "Cukup mandiri",
            2: "Sering bergantung pada orang lain",
            1: "Tidak mandiri dan pasif"
        }
    },
    {
        "no": 3,
        "soal": "Bagaimana Anda mengatur waktu kerja tanpa perlu diingatkan oleh atasan?",
        "jawaban_ideal": "Membuat jadwal dan mematuhinya dengan disiplin",
        "opsi": ["Mandiri dan proaktif", "Cukup mandiri", "Sering bergantung pada orang lain", "Tidak mandiri dan pasif"],
        "skor": {
            4: "Mandiri dan proaktif",
            3: "Cukup mandiri",
            2: "Sering bergantung pada orang lain",
            1: "Tidak mandiri dan pasif"
        }
    },
    {
        "no": 4,
        "soal": "Jika diberi proyek individu, apa langkah pertama yang Anda ambil?",
        "jawaban_ideal": "Merencanakan langkah kerja dan menyiapkan kebutuhan",
        "opsi": ["Mandiri dan proaktif", "Cukup mandiri", "Sering bergantung pada orang lain", "Tidak mandiri dan pasif"],
        "skor": {
            4: "Mandiri dan proaktif",
            3: "Cukup mandiri",
            2: "Sering bergantung pada orang lain",
            1: "Tidak mandiri dan pasif"
        }
    },
    {
        "no": 5,
        "soal": "Bagaimana Anda bersikap ketika menghadapi masalah kerja yang belum pernah Anda alami?",
        "jawaban_ideal": "Mencari informasi dan solusi mandiri sebelum meminta bantuan",
        "opsi": ["Mandiri dan proaktif", "Cukup mandiri", "Sering bergantung pada orang lain", "Tidak mandiri dan pasif"],
        "skor": {
            4: "Mandiri dan proaktif",
            3: "Cukup mandiri",
            2: "Sering bergantung pada orang lain",
            1: "Tidak mandiri dan pasif"
        }
    },
    {
        "no": 6,
        "soal": "Jika Anda tidak setuju dengan cara kerja rekan lain, apa yang Anda lakukan?",
        "jawaban_ideal": "Menjalankan tugas sesuai pendapat sendiri dengan tetap sopan",
        "opsi": ["Mandiri dan proaktif", "Cukup mandiri", "Sering bergantung pada orang lain", "Tidak mandiri dan pasif"],
        "skor": {
            4: "Mandiri dan proaktif",
            3: "Cukup mandiri",
            2: "Sering bergantung pada orang lain",
            1: "Tidak mandiri dan pasif"
        }
    },
    {
        "no": 7,
        "soal": "Bagaimana cara Anda memastikan pekerjaan selesai tanpa bantuan orang lain?",
        "jawaban_ideal": "Bekerja fokus dan mengevaluasi hasil secara mandiri",
        "opsi": ["Mandiri dan proaktif", "Cukup mandiri", "Sering bergantung pada orang lain", "Tidak mandiri dan pasif"],
        "skor": {
            4: "Mandiri dan proaktif",
            3: "Cukup mandiri",
            2: "Sering bergantung pada orang lain",
            1: "Tidak mandiri dan pasif"
        }
    },
    {
        "no": 8,
        "soal": "Ketika bekerja dari rumah tanpa pengawasan langsung, bagaimana Anda menjaga produktivitas?",
        "jawaban_ideal": "Menetapkan target pribadi dan menjaga komitmen kerja",
        "opsi": ["Mandiri dan proaktif", "Cukup mandiri", "Sering bergantung pada orang lain", "Tidak mandiri dan pasif"],
        "skor": {
            4: "Mandiri dan proaktif",
            3: "Cukup mandiri",
            2: "Sering bergantung pada orang lain",
            1: "Tidak mandiri dan pasif"
        }
    },
    {
        "no": 9,
        "soal": "Bagaimana Anda menyikapi tanggung jawab pribadi dalam pekerjaan tim?",
        "jawaban_ideal": "Menjalankan bagian tugas dengan tanggung jawab penuh",
        "opsi": ["Mandiri dan proaktif", "Cukup mandiri", "Sering bergantung pada orang lain", "Tidak mandiri dan pasif"],
        "skor": {
            4: "Mandiri dan proaktif",
            3: "Cukup mandiri",
            2: "Sering bergantung pada orang lain",
            1: "Tidak mandiri dan pasif"
        }
    },
    {
        "no": 10,
        "soal": "Jika harus belajar keterampilan baru, apa yang Anda lakukan?",
        "jawaban_ideal": "Mencari referensi dan belajar secara mandiri",
        "opsi": ["Mandiri dan proaktif", "Cukup mandiri", "Sering bergantung pada orang lain", "Tidak mandiri dan pasif"],
        "skor": {
            4: "Mandiri dan proaktif",
            3: "Cukup mandiri",
            2: "Sering bergantung pada orang lain",
            1: "Tidak mandiri dan pasif"
        }
    }
]

SUBTES_ID = "Kecerdasan_Emosi_Kemandirian"   # HARUS sama persis dengan daftar_tes

def hitung_skor(jawaban_peserta):
    total = 0

    # loop semua soal
    for i, soal in enumerate(soal_list, start=1):
        
        key = f"{SUBTES_ID}_q{i}"
        jawaban = jawaban_peserta.get(key)

        if not jawaban:
            continue

        if "skor" in soal and isinstance(soal["skor"], dict):
            for nilai, teks in soal["skor"].items():
                if teks == jawaban:
                    total += int(nilai)
                    break

    if total >= 35:
        ket = "Sangat Baik"
    elif total >= 25:
        ket = "Baik"
    elif total >= 15:
        ket = "Cukup"
    else:
        ket = "Kurang"

    return {
        "skor": total,
        "keterangan": f"Tingkat Kemandirian = {ket}"
    }