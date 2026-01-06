# pages/3_Tes_Psikotes.py
import streamlit as st
import importlib
import os
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

from utils.db import insert_hasil
from utils.sheets import append_result
from utils.durations import DURASI_CUSTOM, DEFAULT_DURATION

st.set_page_config(page_title="Tes Psikotes", page_icon="🧩", layout="wide")

# ================= VALIDASI =================
if "biodata" not in st.session_state or "daftar_tes" not in st.session_state:
    st.warning("⚠️ Silakan isi biodata dan pilih tes terlebih dahulu.")
    st.stop()

biodata = st.session_state["biodata"]
daftar_tes = st.session_state["daftar_tes"]

st.session_state.setdefault("tes_index", 0)
st.session_state.setdefault("jawaban_peserta", {})
st.session_state.setdefault("hasil_semua_subtes", [])
st.session_state.setdefault("sudah_simpan", False)

tes_index = st.session_state["tes_index"]
current_sub = daftar_tes[tes_index]

# ================= HELPER =================
def subtest_to_module(sub_id):
    parts = sub_id.split("_")
    if len(parts) >= 3:
        folder = f"{parts[0]}_{parts[1]}"
        sub = "_".join(parts[2:])
        if os.path.isdir(os.path.join("soal", folder)):
            return f"soal.{folder}.{sub}"
    return f"soal.{sub_id}"

def get_duration(sub_id):
    return DURASI_CUSTOM.get(sub_id, DEFAULT_DURATION)

# ================= TIMER GLOBAL =================
if "global_end" not in st.session_state:
    total_minutes = sum(get_duration(s) for s in daftar_tes)
    st.session_state["global_end"] = datetime.now() + timedelta(minutes=total_minutes)

def remaining_seconds():
    return max(0, int((st.session_state["global_end"] - datetime.now()).total_seconds()))

st_autorefresh(interval=1000, key="timer")

sisa = remaining_seconds()
m, s = sisa // 60, sisa % 60

st.markdown(
    f"""
    <div style="position:fixed; top:80px; right:40px;
    background:#f0f2f6; border:2px solid #0b5394;
    padding:12px 18px; border-radius:10px;
    font-size:18px; font-weight:bold;">
    ⏰ {m:02d}:{s:02d}
    </div>
    """,
    unsafe_allow_html=True
)

# ================= LOAD SOAL =================
module_name = subtest_to_module(current_sub)

try:
    soal_module = importlib.import_module(module_name)
except Exception:
    st.error(f"❌ Modul soal tidak ditemukan: {module_name}")
    st.stop()

soal_list = soal_module.soal_list

st.title(f"🧠 {current_sub.replace('_',' ')}")
st.markdown("---")

# ================= TAMPILKAN SOAL =================
for i, soal in enumerate(soal_list, start=1):
    st.write(f"**{i}. {soal['soal']}**")

    pilihan = (
        soal.get("opsi")
        or soal.get("pilihan")
        or list(soal.get("skor", {}).values())
    )

    key = f"{current_sub}_q{i}"
    st.session_state["jawaban_peserta"].setdefault(key, None)

    jawab = st.radio(
        "Pilih jawaban:",
        pilihan,
        index=pilihan.index(st.session_state["jawaban_peserta"][key])
        if st.session_state["jawaban_peserta"][key] in pilihan else None,
        key=f"radio_{key}"
    )

    st.session_state["jawaban_peserta"][key] = jawab
    st.markdown("---")

# ================= HITUNG & SIMPAN SUBTES =================
# ================= HITUNG & SIMPAN SUBTES (AMAN) =================
def save_subtest_result(sub_id):
    skor = 0
    keterangan = "-"

    module_path = subtest_to_module(sub_id)

    try:
        m = importlib.import_module(module_path)
    except Exception:
        m = None

    # Jika modul punya hitung_skor, pakai itu
    if m and hasattr(m, "hitung_skor"):
        try:
            res = m.hitung_skor(st.session_state["jawaban_peserta"])
            skor = res.get("skor", 0)
            keterangan = res.get("keterangan", "-")
        except Exception:
            skor = 0
            keterangan = "error_hitung"
    # Kalau tidak ada hitung_skor, lakukan perhitungan manual seperti kode lama
    else:
        soal_temp = m.soal_list if m and hasattr(m, "soal_list") else []

        for idx, it in enumerate(soal_temp):
            key = f"{sub_id}_q{idx+1}"
            ans = st.session_state["jawaban_peserta"].get(key)

            if "jawaban_benar" in it:
                if ans == it["jawaban_benar"]:
                    skor += 4

            elif "skor" in it and isinstance(it["skor"], dict):
                for nilai, teks in it["skor"].items():
                    if teks == ans:
                        skor += int(nilai)
                        break

    # Pastikan hasil_semua_subtes ada di session
    if "hasil_semua_subtes" not in st.session_state:
        st.session_state["hasil_semua_subtes"] = []

    # Hapus hasil lama subtes ini
    st.session_state["hasil_semua_subtes"] = [
        h for h in st.session_state["hasil_semua_subtes"]
        if h.get("subtes") != sub_id
    ]

    # Simpan hasil baru dengan flag sudah_simpan=False untuk Selesai nanti
    st.session_state["hasil_semua_subtes"].append({
        "subtes": sub_id,
        "skor": skor,
        "keterangan": keterangan,
        "sudah_simpan": False
    })

# ================= SIMPAN KE DB + SHEETS (SEKALI) =================
def simpan_semua_hasil_ke_sheets():
    if "hasil_semua_subtes" not in st.session_state:
        return

    nama_user = st.session_state["biodata"].get("Nama", "")
    job_user = st.session_state["biodata"].get("Job Title", "")
    tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for h in st.session_state["hasil_semua_subtes"]:
        # pakai flag per subtes supaya tidak double save
        if h.get("sudah_simpan"):
            continue

        insert_hasil(
            nama_user,
            job_user,
            h["subtes"],
            h["skor"],
            h["keterangan"],
            tanggal
        )

        append_result(
            h["subtes"],
            h["skor"],
            h["keterangan"]
        )

        # tandai subtes ini sudah tersimpan
        h["sudah_simpan"] = True

# ================= WAKTU HABIS =================
if sisa == 0:
    save_subtest_result(current_sub)
    simpan_semua_hasil()
    st.switch_page("pages/4_Terima_Kasih.py")

# ================= NAVIGASI =================
# Navigasi
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("⬅️ Kembali") and st.session_state["tes_index"] > 0:
        save_subtest_result(current_sub)
        st.session_state["tes_index"] -= 1

with col3:
    if st.session_state["tes_index"] < len(daftar_tes) - 1:
        if st.button("➡️ Lanjut"):
            save_subtest_result(current_sub)
            st.session_state["tes_index"] += 1
    else:
        if st.button("✅ Selesai"):
            save_subtest_result(current_sub)
            simpan_semua_hasil_ke_sheets()
            st.switch_page("4_Terima_Kasih")
