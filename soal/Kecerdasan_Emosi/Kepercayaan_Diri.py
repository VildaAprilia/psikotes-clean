soal_list = [
    {
        "no": 1,
        "soal": "Bagaimana Anda bereaksi ketika diberi tanggung jawab besar di tempat kerja?",
        "jawaban_ideal": "Menerimanya dengan percaya diri dan tanggung jawab",
        "opsi": ["Sangat percaya diri & positif", "Cukup percaya diri", "Ragu-ragu", "Tidak yakin dan mudah cemas"],
        "skor": {
            4: "Sangat percaya diri & positif",
            3: "Cukup percaya diri",
            2: "Ragu-ragu",
            1: "Tidak yakin dan mudah cemas"
        }
    },
    {
        "no": 2,
        "soal": "Apa yang Anda lakukan jika atasan meminta Anda memimpin proyek baru?",
        "jawaban_ideal": "Menerima tantangan dan segera menyusun rencana kerja",
        "opsi": ["Sangat percaya diri & positif", "Cukup percaya diri", "Ragu-ragu", "Tidak yakin dan mudah cemas"],
        "skor": {
            4: "Sangat percaya diri & positif",
            3: "Cukup percaya diri",
            2: "Ragu-ragu",
            1: "Tidak yakin dan mudah cemas"
        }
    },
    {
        "no": 3,
        "soal": "Ketika ide Anda ditolak dalam rapat, bagaimana sikap Anda?",
        "jawaban_ideal": "Menerima dengan tenang dan memperbaiki ide di kesempatan berikutnya",
        "opsi": ["Sangat percaya diri & positif", "Cukup percaya diri", "Ragu-ragu", "Tidak yakin dan mudah cemas"],
        "skor": {
            4: "Sangat percaya diri & positif",
            3: "Cukup percaya diri",
            2: "Ragu-ragu",
            1: "Tidak yakin dan mudah cemas"
        }
    },
    {
        "no": 4,
        "soal": "Bagaimana Anda bersikap saat berbicara di depan banyak orang?",
        "jawaban_ideal": "Berbicara dengan tenang dan penuh keyakinan",
        "opsi": ["Sangat percaya diri & positif", "Cukup percaya diri", "Ragu-ragu", "Tidak yakin dan mudah cemas"],
        "skor": {
            4: "Sangat percaya diri & positif",
            3: "Cukup percaya diri",
            2: "Ragu-ragu",
            1: "Tidak yakin dan mudah cemas"
        }
    },
    {
        "no": 5,
        "soal": "Jika ada rekan kerja yang meragukan kemampuan Anda, apa yang Anda lakukan?",
        "jawaban_ideal": "Membuktikan kemampuan melalui hasil kerja",
        "opsi": ["Sangat percaya diri & positif", "Cukup percaya diri", "Ragu-ragu", "Tidak yakin dan mudah cemas"],
        "skor": {
            4: "Sangat percaya diri & positif",
            3: "Cukup percaya diri",
            2: "Ragu-ragu",
            1: "Tidak yakin dan mudah cemas"
        }
    },
    {
        "no": 6,
        "soal": "Bagaimana Anda mempersiapkan diri menghadapi wawancara penting?",
        "jawaban_ideal": "Mempersiapkan diri dengan latihan dan informasi yang cukup",
        "opsi": ["Sangat percaya diri & positif", "Cukup percaya diri", "Ragu-ragu", "Tidak yakin dan mudah cemas"],
        "skor": {
            4: "Sangat percaya diri & positif",
            3: "Cukup percaya diri",
            2: "Ragu-ragu",
            1: "Tidak yakin dan mudah cemas"
        }
    },
    {
        "no": 7,
        "soal": "Ketika menghadapi tugas baru yang belum pernah Anda kerjakan sebelumnya, apa yang Anda lakukan?",
        "jawaban_ideal": "Belajar dan mencari tahu agar mampu menyelesaikan dengan baik",
        "opsi": ["Sangat percaya diri & positif", "Cukup percaya diri", "Ragu-ragu", "Tidak yakin dan mudah cemas"],
        "skor": {
            4: "Sangat percaya diri & positif",
            3: "Cukup percaya diri",
            2: "Ragu-ragu",
            1: "Tidak yakin dan mudah cemas"
        }
    },
    {
        "no": 8,
        "soal": "Bagaimana Anda menanggapi keberhasilan rekan kerja lain dibanding diri Anda?",
        "jawaban_ideal": "Menghargai keberhasilan orang lain dan tetap fokus pada diri sendiri",
        "opsi": ["Sangat percaya diri & positif", "Cukup percaya diri", "Ragu-ragu", "Tidak yakin dan mudah cemas"],
        "skor": {
            4: "Sangat percaya diri & positif",
            3: "Cukup percaya diri",
            2: "Ragu-ragu",
            1: "Tidak yakin dan mudah cemas"
        }
    },
    {
        "no": 9,
        "soal": "Apa yang Anda lakukan ketika hasil kerja Anda dikritik oleh atasan?",
        "jawaban_ideal": "Menerima kritik dengan positif dan memperbaikinya",
        "opsi": ["Sangat percaya diri & positif", "Cukup percaya diri", "Ragu-ragu", "Tidak yakin dan mudah cemas"],
        "skor": {
            4: "Sangat percaya diri & positif",
            3: "Cukup percaya diri",
            2: "Ragu-ragu",
            1: "Tidak yakin dan mudah cemas"
        }
    },
    {
        "no": 10,
        "soal": "Bagaimana Anda menyikapi kegagalan yang pernah Anda alami?",
        "jawaban_ideal": "Menjadikannya pelajaran untuk tumbuh lebih baik",
        "opsi": ["Sangat percaya diri & positif", "Cukup percaya diri", "Ragu-ragu", "Tidak yakin dan mudah cemas"],
        "skor": {
            4: "Sangat percaya diri & positif",
            3: "Cukup percaya diri",
            2: "Ragu-ragu",
            1: "Tidak yakin dan mudah cemas"
        }
    }
]

SUBTES_ID = "Kecerdasan_Emosi_Kepercayaan_Diri"   # HARUS sama persis dengan daftar_tes

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
        "keterangan": f"Tingkat Kepercayaan Diri = {ket}"
    }
