# utils/durations.py
# Sumber tunggal durasi per subtes kecil (key = bagian terakhir atau full id)
DEFAULT_DURATION = 5  # menit fallback

DURASI_CUSTOM = {
    # --- Kesiapan Kerja (per file) ---
    "Kesiapan_Kerja_Logika": 7,
    "Kesiapan_Kerja_Analisa_Sintesa": 7,
    "Kesiapan_Kerja_Verbal": 6,
    "Kesiapan_Kerja_Daya_Ingat": 6,
    "Kesiapan_Kerja_Daya_Tahan": 5,
    "Kesiapan_Kerja_Motivasi": 5,
    "Kesiapan_Kerja_Numerikal": 7,
    "Kesiapan_Kerja_Persepsi": 5,
    "Kesiapan_Kerja_Psikomotorik": 6,
    "Kesiapan_Kerja_Spasial": 7,

    # --- Kecerdasan Emosi (per file) ---
    "Kecerdasan_Emosi_Kemandirian": 4,
    "Kecerdasan_Emosi_Kepercayaan_Diri": 4,
    "Kecerdasan_Emosi_Kerjasama": 4,
    "Kecerdasan_Emosi_Sosialisasi": 4,  # prefer Sosialisasi (auto-mapped)
    "Kecerdasan_Emosi_Stabilitas_Emosi": 4,
    "Kecerdasan_Emosi_Tanggung_Jawab": 4,

    # --- Subtes tunggal (root soal/*.py) ---
    "Intelegensi_Umum": 10,
    "Dominasi_Otak": 5,
    "Gaya_Bekerja": 5,
    "Kepribadian_RIASEC_Model": 8,
    "Kepribadian_Sanguinis_Melankolis_Kholeris_Plegmatis": 8,
}
