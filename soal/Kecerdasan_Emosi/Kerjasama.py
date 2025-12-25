# soal_kecerdasan_emosi_kerjasama.py

SUBJUDUL = "KERJASAMA"

soal_list = [
    {
        "no": 1,
        "soal": "Apa yang Anda lakukan jika anggota tim tidak melaksanakan tugasnya dengan baik?",
        "jawaban_ideal": "Memberikan saran dan membantu memperbaiki hasil kerja",
        "opsi": ["Aktif berkontribusi dan solutif", "Kooperatif", "Netral", "Cenderung individualis"],
        "skor": {
            4: "Aktif berkontribusi dan solutif",
            3: "Kooperatif",
            2: "Netral",
            1: "Cenderung individualis"
        }
    },
    {
        "no": 2,
        "soal": "Bagaimana Anda bersikap ketika pendapat Anda tidak diterima oleh tim?",
        "jawaban_ideal": "Menerima dengan lapang dada dan tetap berkontribusi",
        "opsi": ["Aktif berkontribusi dan solutif", "Kooperatif", "Netral", "Cenderung individualis"],
        "skor": {
            4: "Aktif berkontribusi dan solutif",
            3: "Kooperatif",
            2: "Netral",
            1: "Cenderung individualis"
        }
    },
    {
        "no": 3,
        "soal": "Ketika bekerja dalam kelompok, apa hal terpenting bagi Anda?",
        "jawaban_ideal": "Kekompakan dan komunikasi yang baik",
        "opsi": ["Aktif berkontribusi dan solutif", "Kooperatif", "Netral", "Cenderung individualis"],
        "skor": {
            4: "Aktif berkontribusi dan solutif",
            3: "Kooperatif",
            2: "Netral",
            1: "Cenderung individualis"
        }
    },
    {
        "no": 4,
        "soal": "Bagaimana Anda membantu tim mencapai target bersama?",
        "jawaban_ideal": "Berkoordinasi dan memberikan dukungan aktif",
        "opsi": ["Aktif berkontribusi dan solutif", "Kooperatif", "Netral", "Cenderung individualis"],
        "skor": {
            4: "Aktif berkontribusi dan solutif",
            3: "Kooperatif",
            2: "Netral",
            1: "Cenderung individualis"
        }
    },
    {
        "no": 5,
        "soal": "Jika ada perbedaan pendapat antar anggota tim, apa langkah Anda?",
        "jawaban_ideal": "Menjadi penengah dan mencari solusi bersama",
        "opsi": ["Aktif berkontribusi dan solutif", "Kooperatif", "Netral", "Cenderung individualis"],
        "skor": {
            4: "Aktif berkontribusi dan solutif",
            3: "Kooperatif",
            2: "Netral",
            1: "Cenderung individualis"
        }
    },
    {
        "no": 6,
        "soal": "Bagaimana Anda merespons jika rekan kerja meminta bantuan padahal Anda juga sibuk?",
        "jawaban_ideal": "Membantu semampunya tanpa mengabaikan tugas sendiri",
        "opsi": ["Aktif berkontribusi dan solutif", "Kooperatif", "Netral", "Cenderung individualis"],
        "skor": {
            4: "Aktif berkontribusi dan solutif",
            3: "Kooperatif",
            2: "Netral",
            1: "Cenderung individualis"
        }
    },
    {
        "no": 7,
        "soal": "Ketika anggota tim mengalami kesulitan, apa yang Anda lakukan?",
        "jawaban_ideal": "Memberikan bantuan dan motivasi",
        "opsi": ["Aktif berkontribusi dan solutif", "Kooperatif", "Netral", "Cenderung individualis"],
        "skor": {
            4: "Aktif berkontribusi dan solutif",
            3: "Kooperatif",
            2: "Netral",
            1: "Cenderung individualis"
        }
    },
    {
        "no": 8,
        "soal": "Bagaimana cara Anda menjaga hubungan kerja yang harmonis dengan tim?",
        "jawaban_ideal": "Menjaga komunikasi terbuka dan menghormati satu sama lain",
        "opsi": ["Aktif berkontribusi dan solutif", "Kooperatif", "Netral", "Cenderung individualis"],
        "skor": {
            4: "Aktif berkontribusi dan solutif",
            3: "Kooperatif",
            2: "Netral",
            1: "Cenderung individualis"
        }
    },
    {
        "no": 9,
        "soal": "Apa yang Anda lakukan jika satu anggota tim mendapat pujian lebih dari Anda?",
        "jawaban_ideal": "Tetap menghargai dan mendukung rekan tersebut",
        "opsi": ["Aktif berkontribusi dan solutif", "Kooperatif", "Netral", "Cenderung individualis"],
        "skor": {
            4: "Aktif berkontribusi dan solutif",
            3: "Kooperatif",
            2: "Netral",
            1: "Cenderung individualis"
        }
    },
    {
        "no": 10,
        "soal": "Bagaimana Anda mengatasi konflik kecil dalam kelompok kerja?",
        "jawaban_ideal": "Menyelesaikan dengan komunikasi terbuka dan sikap dewasa",
        "opsi": ["Aktif berkontribusi dan solutif", "Kooperatif", "Netral", "Cenderung individualis"],
        "skor": {
            4: "Aktif berkontribusi dan solutif",
            3: "Kooperatif",
            2: "Netral",
            1: "Cenderung individualis"
        }
    }
]

SUBTES_ID = "Kecerdasan_Emosi_Kerjasama"

def hitung_skor(jawaban_peserta):
    total = 0

    for i, soal in enumerate(soal_list, start=1):
        key = f"{SUBTES_ID}_q{i}"
        jawaban = jawaban_peserta.get(key)

        if "skor" in soal:
            for nilai, teks in soal["skor"].items():
                if teks == jawaban:
                    total += int(nilai)
                    break

    # Penentuan kategori skor (boleh kamu ubah kalau ada standar sendiri)
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
        "keterangan": f"Tingkat Kerjasama = {ket}"
    }
