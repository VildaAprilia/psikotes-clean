SUBJUDUL = "TANGGUNG JAWAB"

opsi_default = [
    "Bertanggung jawab penuh & proaktif",
    "Cukup bertanggung jawab",
    "Reaktif",
    "Menghindar dari tanggung jawab"
]

soal_list = [
    {
        "no": 1,
        "soal": "Bagaimana Anda menyikapi kesalahan yang Anda buat dalam pekerjaan?",
        "jawaban_ideal": "Mengakui kesalahan dan memperbaikinya",
        "opsi": opsi_default
    },
    {
        "no": 2,
        "soal": "Apa yang Anda lakukan jika atasan tidak ada, tetapi pekerjaan harus diselesaikan segera?",
        "jawaban_ideal": "Mengambil inisiatif untuk menyelesaikannya",
        "opsi": opsi_default
    },
    {
        "no": 3,
        "soal": "Jika Anda lupa mengirim laporan penting, tindakan yang tepat adalah...?",
        "jawaban_ideal": "Segera meminta maaf dan mengirim laporan secepatnya",
        "opsi": opsi_default
    },
    {
        "no": 4,
        "soal": "Bagaimana Anda memastikan pekerjaan Anda selesai tepat waktu?",
        "jawaban_ideal": "Membuat perencanaan dan disiplin dalam bekerja",
        "opsi": opsi_default
    },
    {
        "no": 5,
        "soal": "Ketika diberi tugas tambahan di luar tanggung jawab utama, apa sikap Anda?",
        "jawaban_ideal": "Menerima dengan tanggung jawab dan tetap berusaha maksimal",
        "opsi": opsi_default
    },
    {
        "no": 6,
        "soal": "Jika rekan kerja melakukan kesalahan, tetapi tim Anda disalahkan, apa yang Anda lakukan?",
        "jawaban_ideal": "Menjelaskan dengan jujur dan mencari solusi bersama",
        "opsi": opsi_default
    },
    {
        "no": 7,
        "soal": "Apa yang Anda lakukan jika hasil kerja Anda tidak sesuai harapan perusahaan?",
        "jawaban_ideal": "Memperbaiki kekurangan dan belajar dari pengalaman",
        "opsi": opsi_default
    },
    {
        "no": 8,
        "soal": "Bagaimana sikap Anda terhadap aturan dan kebijakan perusahaan?",
        "jawaban_ideal": "Mematuhi aturan sebagai bentuk profesionalisme",
        "opsi": opsi_default
    },
    {
        "no": 9,
        "soal": "Jika Anda tidak setuju dengan keputusan atasan, tetapi harus melaksanakannya, bagaimana tindakan Anda?",
        "jawaban_ideal": "Melaksanakan tugas dengan tetap menghormati keputusan",
        "opsi": opsi_default
    },
    {
        "no": 10,
        "soal": "Bagaimana Anda menunjukkan rasa tanggung jawab dalam pekerjaan sehari-hari?",
        "jawaban_ideal": "Menyelesaikan tugas dengan teliti dan konsisten",
        "opsi": opsi_default
    }
]

SUBTES_ID = "Kecerdasan_Emosi_Tanggung_Jawab"

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
        "keterangan": f"Tingkat Tanggung Jawab = {ket}"
    }
