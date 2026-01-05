SUBJUDUL = "STABILITAS EMOSI"

opsi_default = [
    "Tenang dan rasional",
    "Cukup tenang",
    "Emosional tapi terkendali",
    "Mudah marah"
]

soal_list = [
    {
        "no": 1,
        "soal": "Bagaimana Anda bereaksi ketika mendapat kritik dari rekan kerja?",
        "jawaban_ideal": "Menerima dengan tenang dan mengevaluasi diri",
        "opsi": opsi_default
    },
    {
        "no": 2,
        "soal": "Ketika menghadapi situasi kerja yang menegangkan, apa yang Anda lakukan?",
        "jawaban_ideal": "Menarik napas dalam dan berpikir jernih",
        "opsi": opsi_default
    },
    {
        "no": 3,
        "soal": "Jika atasan memberikan tugas mendadak, bagaimana respons Anda?",
        "jawaban_ideal": "Menerima dengan tanggung jawab dan mengatur prioritas",
        "opsi": opsi_default
    },
    {
        "no": 4,
        "soal": "Bagaimana cara Anda menenangkan diri ketika merasa marah di tempat kerja?",
        "jawaban_ideal": "Menarik diri sejenak dan menenangkan pikiran",
        "opsi": opsi_default
    },
    {
        "no": 5,
        "soal": "Apa yang Anda lakukan ketika rekan kerja melakukan kesalahan yang berdampak pada Anda?",
        "jawaban_ideal": "Menegur dengan sopan dan mencari solusi bersama",
        "opsi": opsi_default
    },
    {
        "no": 6,
        "soal": "Bagaimana sikap Anda ketika target kerja tidak tercapai?",
        "jawaban_ideal": "Evaluasi penyebab dan mencoba lagi",
        "opsi": opsi_default
    },
    {
        "no": 7,
        "soal": "Ketika terjadi perbedaan pendapat dalam tim, apa yang Anda lakukan?",
        "jawaban_ideal": "Mendengarkan pendapat lain dan mencari kesepakatan",
        "opsi": opsi_default
    },
    {
        "no": 8,
        "soal": "Bagaimana Anda menyikapi tekanan kerja yang tinggi dalam waktu lama?",
        "jawaban_ideal": "Menjaga keseimbangan dan tetap fokus pada solusi",
        "opsi": opsi_default
    },
    {
        "no": 9,
        "soal": "Apa yang Anda lakukan ketika mengalami kegagalan dalam pekerjaan?",
        "jawaban_ideal": "Belajar dari pengalaman dan tetap bersemangat",
        "opsi": opsi_default
    },
    {
        "no": 10,
        "soal": "Bagaimana Anda mengontrol emosi ketika menghadapi pelanggan yang marah?",
        "jawaban_ideal": "Berbicara dengan tenang dan fokus menyelesaikan masalah",
        "opsi": opsi_default
    }
]

SUBTES_ID = "Kecerdasan_Emosi_Stabilitas_Emosi"   # HARUS sama persis dengan daftar_tes

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
        "keterangan": f"Tingkat Stabilitas Emosi = {ket}"
    }
