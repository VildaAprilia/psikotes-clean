SUBJUDUL = "SOSIALISASI"

opsi_default = [
    "Asertif & mudah bergaul",
    "Cukup terbuka",
    "Pasif dalam bersosialisasi",
    "Menutup diri atau defensif"
]

soal_list = [
    {
        "no": 1,
        "soal": "Bagaimana Anda memulai percakapan dengan rekan kerja baru?",
        "jawaban_ideal": "Menyapa dengan ramah dan terbuka",
        "opsi": opsi_default
    },
    {
        "no": 2,
        "soal": "Jika rekan kerja Anda pendiam, apa yang Anda lakukan untuk membangun hubungan?",
        "jawaban_ideal": "Mendekatinya dengan sopan dan berbicara perlahan",
        "opsi": opsi_default
    },
    {
        "no": 3,
        "soal": "Bagaimana Anda berperilaku saat berada dalam kelompok baru di tempat kerja?",
        "jawaban_ideal": "Bersikap ramah dan aktif mengenalkan diri",
        "opsi": opsi_default
    },
    {
        "no": 4,
        "soal": "Ketika terjadi kesalahpahaman dengan rekan kerja, apa yang Anda lakukan?",
        "jawaban_ideal": "Berbicara secara terbuka dan mencari solusi bersama",
        "opsi": opsi_default
    },
    {
        "no": 5,
        "soal": "Bagaimana Anda merespons ajakan diskusi dari rekan kerja yang memiliki pendapat berbeda?",
        "jawaban_ideal": "Mendengarkan dengan sopan dan menghargai pendapat",
        "opsi": opsi_default
    },
    {
        "no": 6,
        "soal": "Apa yang Anda lakukan agar tetap akrab dengan tim kerja Anda?",
        "jawaban_ideal": "Melakukan komunikasi rutin dan menjaga kekompakan",
        "opsi": opsi_default
    },
    {
        "no": 7,
        "soal": "Bagaimana Anda menghadapi rekan kerja yang sulit diajak kerja sama?",
        "jawaban_ideal": "Tetap profesional dan fokus pada tujuan bersama",
        "opsi": opsi_default
    },
    {
        "no": 8,
        "soal": "Ketika berada di lingkungan kerja yang kompetitif, bagaimana cara Anda menjaga hubungan baik?",
        "jawaban_ideal": "Menghargai persaingan secara sehat dan menjaga sikap positif",
        "opsi": opsi_default
    },
    {
        "no": 9,
        "soal": "Bagaimana Anda bersikap terhadap rekan kerja yang baru bergabung dalam tim Anda?",
        "jawaban_ideal": "Menyambut dengan hangat dan membantu adaptasi",
        "opsi": opsi_default
    },
    {
        "no": 10,
        "soal": "Apa yang Anda lakukan jika merasa kurang cocok dengan kepribadian rekan kerja tertentu?",
        "jawaban_ideal": "Tetap profesional dan menjaga komunikasi baik",
        "opsi": opsi_default
    }
]

SUBTES_ID = "Kecerdasan_Emosi_Sosialisai"

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
        "keterangan": f"Tingkat Sosialisai = {ket}"
    }

