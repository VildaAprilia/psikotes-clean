import streamlit as st
import importlib
import os
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

from utils.db import insert_hasil
from utils.durations import DURASI_CUSTOM, DEFAULT_DURATION

st.set_page_config(page_title="Tes Psikotes", page_icon="🧠", layout="wide")

# ================= VALIDASI =================
if "biodata" not in st.session_state or "daftar_tes" not in st.session_state:
    st.warning("⚠️ Silakan isi biodata dan pilih tes terlebih dahulu.")
    st.stop()

biodata = st.session_state["biodata"]
daftar_tes = st.session_state["daftar_tes"]

if "tes_index" not in st.session_state:
    st.session_state["tes_index"] = 0

if "jawaban_peserta" not in st.session_state:
    st.session_state["jawaban_peserta"] = {}

if "hasil_semua_subtes" not in st.session_state:
    st.session_state["hasil_semua_subtes"] = []

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
except Exception as e:
    st.error(f"❌ Gagal memuat soal: {module_name}")
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
        key=key
    )

    st.session_state["jawaban_peserta"][key] = jawab
    st.markdown("---")

# ================= HITUNG SKOR SUBTES =================
def hitung_dan_simpan_subtes(sub_id):
    module = importlib.import_module(subtest_to_module(sub_id))
    hasil = module.hitung_skor(st.session_state["jawaban_peserta"])

    # HAPUS HASIL LAMA SUBTES INI
    st.session_state["hasil_semua_subtes"] = [
        h for h in st.session_state["hasil_semua_subtes"]
        if h["subtes"] != sub_id
    ]

    st.session_state["hasil_semua_subtes"].append({
        "subtes": sub_id,
        "skor": hasil["skor"],
        "keterangan": hasil["keterangan"]
    })

# ================= WAKTU HABIS =================
if sisa == 0:
    hitung_dan_simpan_subtes(current_sub)

    for h in st.session_state["hasil_semua_subtes"]:
        insert_hasil(
            biodata["Nama"],
            biodata["Job Title"],
            h["subtes"],
            h["skor"],
            h["keterangan"],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

    st.switch_page("pages/4_Terima_Kasih.py")

# ================= NAVIGASI =================
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("⬅️ Kembali") and tes_index > 0:
        hitung_dan_simpan_subtes(current_sub)
        st.session_state["tes_index"] -= 1
        st.rerun()

with col3:
    if tes_index < len(daftar_tes) - 1:
        if st.button("➡️ Lanjut"):
            hitung_dan_simpan_subtes(current_sub)
            st.session_state["tes_index"] += 1
            st.rerun()
    else:
        if st.button("✅ Selesai"):
            hitung_dan_simpan_subtes(current_sub)

            for h in st.session_state["hasil_semua_subtes"]:
                insert_hasil(
                    biodata["Nama"],
                    biodata["Job Title"],
                    h["subtes"],
                    h["skor"],
                    h["keterangan"],
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )

            st.switch_page("pages/4_Terima_Kasih.py")