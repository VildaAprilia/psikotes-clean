# utils/job_mapping.py
import os

# === ORIGINAL JOB MAPPING (per-subtes kecil seperti yang kamu kirim) ===
job_mapping = {
    "Kepala Bengkel": [
        "Intelegensi_Umum",
        "Kesiapan_Kerja_Logika",
        "Kesiapan_Kerja_Analisa_Sintesa",
        "Kesiapan_Kerja_Verbal",
        "Kecerdasan_Emosi_Stabilitas_Emosi",
        "Kecerdasan_Emosi_Kerjasama",
        "Kecerdasan_Emosi_Tanggung_Jawab",
        "Kepribadian_Sanguinis_Melankolis_Kholeris_Plegmatis",
        "Kepribadian_RIASEC_Model",
        "Dominasi_Otak",
    ],
    "Kepala Mekanik": [
        "Intelegensi_Umum",
        "Kesiapan_Kerja_Logika",
        "Kesiapan_Kerja_Analisa_Sintesa",
        "Kesiapan_Kerja_Spasial",
        "Kesiapan_Kerja_Persepsi",
        "Kesiapan_Kerja_Daya_Tahan",
        "Kecerdasan_Emosi_Kemandirian",
        "Kecerdasan_Emosi_Kepercayaan_Diri",
        "Kepribadian_Sanguinis_Melankolis_Kholeris_Plegmatis",
    ],
    "Service Advisor": [
        "Kesiapan_Kerja_Verbal",
        "Kesiapan_Kerja_Daya_Ingat",
        "Kesiapan_Kerja_Persepsi",
        "Kesiapan_Kerja_Logika",
        "Kecerdasan_Emosi_Stabilitas_Emosi",
        "Kecerdasan_Emosi_Sosialisasi",  # kept original spelling (will be normalized)
        "Kecerdasan_Emosi_Tanggung_Jawab",
        "Kepribadian_RIASEC_Model",
    ],
    "Front Desk": [
        "Kesiapan_Kerja_Verbal",
        "Kesiapan_Kerja_Daya_Ingat",
        "Kesiapan_Kerja_Persepsi",
        "Kesiapan_Kerja_Numerikal",
        "Kecerdasan_Emosi_Stabilitas_Emosi",
        "Kecerdasan_Emosi_Kerjasama",
        "Gaya_Bekerja",
    ],
    "Part Counter": [
        "Kesiapan_Kerja_Daya_Ingat",
        "Kesiapan_Kerja_Numerikal",
        "Kesiapan_Kerja_Persepsi",
        "Kesiapan_Kerja_Spasial",
        "Kesiapan_Kerja_Daya_Tahan",
        "Kecerdasan_Emosi_Tanggung_Jawab",
        "Gaya_Bekerja",
    ],
    "Kepala Dealer": [
        "Intelegensi_Umum",
        "Kesiapan_Kerja_Logika",
        "Kesiapan_Kerja_Analisa_Sintesa",
        "Kesiapan_Kerja_Verbal",
        "Kecerdasan_Emosi_Stabilitas_Emosi",
        "Kecerdasan_Emosi_Kepercayaan_Diri",
        "Kepribadian_Sanguinis_Melankolis_Kholeris_Plegmatis",
        "Kepribadian_RIASEC_Model",
        "Dominasi_Otak",
    ],
    "Admin CRM": [
        # "Kesiapan_Kerja_Daya_Ingat",
        # "Kesiapan_Kerja_Verbal",
        # "Kesiapan_Kerja_Numerikal",
        # "Kesiapan_Kerja_Persepsi",
        # "Kecerdasan_Emosi_Tanggung_Jawab",
        "Kecerdasan_Emosi_Sosialisasi",
        # "Gaya_Bekerja",
    ],
    "Mekanik": [
        "Kesiapan_Kerja_Psikomotorik",
        "Kesiapan_Kerja_Spasial",
        "Kesiapan_Kerja_Persepsi",
        "Kesiapan_Kerja_Daya_Tahan",
        "Kesiapan_Kerja_Logika",
        "Intelegensi_Umum",
        "Kecerdasan_Emosi_Kemandirian",
        "Kecerdasan_Emosi_Tanggung_Jawab",
    ],
}

# --- Helper: cek apakah subtes id valid (ada file/module) ---
def _normalize_subtes_name(sub_id):
    """
    Normalize common typos: Sosialisai -> Sosialisasi
    Return normalized id.
    """
    if sub_id == "Kecerdasan_Emosi_Sosialisasi":
        return "Kecerdasan_Emosi_Sosialisasi"
    # other normalizations can be added here
    return sub_id

def subtes_exists(sub_id):
    """
    sub_id examples:
      - Intelegensi_Umum  (file soal/Intelegensi_Umum.py)
      - Kesiapan_Kerja_Logika (file soal/Kesiapan_Kerja/Logika.py)
    """
    sub_id = _normalize_subtes_name(sub_id)
    # folder_sub format
    if "_" in sub_id:
        # split on the FIRST underscore that separates folder from rest (some names have multiple underscores)
        parts = sub_id.split("_")
        # try progressively: folder = parts[0] + "_" + ... until path exists
        # We assume folder names are two words for Kesiapan_Kerja, Kecerdasan_Emosi
        # Try folder = parts[0] + "_" + parts[1] if that folder exists
        if len(parts) >= 2:
            folder_candidate = f"{parts[0]}_{parts[1]}"
            sub_candidate = "_".join(parts[2:]) if len(parts) > 2 else ""
            folder_path = os.path.join("soal", folder_candidate)
            if os.path.isdir(folder_path) and sub_candidate:
                file_path = os.path.join(folder_path, f"{sub_candidate}.py")
                return os.path.isfile(file_path)
        # fallback: treat first part as folder
        folder_candidate = parts[0]
        sub_candidate = "_".join(parts[1:])
        folder_path = os.path.join("soal", folder_candidate)
        if os.path.isdir(folder_path) and sub_candidate:
            file_path = os.path.join(folder_path, f"{sub_candidate}.py")
            return os.path.isfile(file_path)
    # single module under soal/
    file_path = os.path.join("soal", f"{sub_id}.py")
    return os.path.isfile(file_path)

def resolve_subtests_for_job(job_title):
    """
    Return a list of normalized subtest IDs that both appear in job_mapping[job_title]
    and exist physically in the 'soal' folder structure (after normalization).
    """
    if job_title not in job_mapping:
        return []

    resolved = []
    for s in job_mapping[job_title]:
        s_norm = _normalize_subtes_name(s)
        if subtes_exists(s_norm):
            resolved.append(s_norm)
        else:
            # try alternate normalizations: if s includes Kesiapan_Kerja_... but folder uses Kesiapan_Kerja/
            # the subtes_exists already tries common cases; if still not exists, skip silently
            pass
    return resolved
