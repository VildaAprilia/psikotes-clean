# pages/3_Tes_Psikotes.py
import streamlit as st
import importlib
import os
import pandas as pd
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

from utils.db import insert_hasil
from utils.sheets import append_result
from utils.durations import DURASI_CUSTOM, DEFAULT_DURATION

st.set_page_config(page_title="Tes Psikotes", page_icon="🧩", layout="wide")

# ========================= VALIDASI =========================
if "biodata" not in st.session_state or "daftar_tes" not in st.session_state:
    st.warning("⚠️ Silakan kembali untuk mengisi biodata dan memilih tes.")
    st.stop()

biodata = st.session_state["biodata"]
daftar_tes = st.session_state["daftar_tes"]

if "tes_index" not in st.session_state:
    st.session_state["tes_index"] = 0

tes_index = st.session_state["tes_index"]

# ========================= MAP SUBTES -> MODUL =========================
def subtest_to_module(sub_id):
    parts = sub_id.split("_")
    if len(parts) >= 3:
        folder_candidate = f"{parts[0]}_{parts[1]}"
        sub_candidate = "_".join(parts[2:])
        if os.path.isdir(os.path.join("soal", folder_candidate)):
            return f"soal.{folder_candidate}.{sub_candidate}"

    if len(parts) >= 2:
        folder_candidate = parts[0]
        sub_candidate = "_".join(parts[1:])
        if os.path.isdir(os.path.join("soal", folder_candidate)):
            return f"soal.{folder_candidate}.{sub_candidate}"

    return f"soal.{sub_id}"

# ========================= DURASI =========================
def get_duration_for_sub(sub_id):
    if sub_id in DURASI_CUSTOM:
        return DURASI_CUSTOM[sub_id]
    tail = sub_id.split("_")[-1]
    return DURASI_CUSTOM.get(tail, DEFAULT_DURATION)

# ========================= GLOBAL TIMER =========================
def init_global_timer():
    if "global_timer_initialized" in st.session_state:
        return

    total_minutes = sum(get_duration_for_sub(sub) for sub in daftar_tes)

    now = datetime.now()
    st.session_state["global_start"] = now
    st.session_state["global_end"] = now + timedelta(minutes=total_minutes)
    st.session_state["global_total_minutes"] = total_minutes
    st.session_state["global_timer_initialized"] = True

init_global_timer()

def remaining_seconds():
    delta = (st.session_state["global_end"] - datetime.now()).total_seconds()
    return max(0, int(delta))

st_autorefresh(interval=1000, key="tick")

rem = remaining_seconds()
mins, secs = rem // 60, rem % 60

st.markdown(
    f"""
    <div style="position: fixed; top: 70px; right: 30px;
                background-color: #f0f2f6; border: 2px solid #0066cc;
                border-radius: 10px; padding: 10px 18px; font-size: 18px;
                font-weight: bold; color: #0066cc; z-index: 9999;">
        ⏰ Sisa Waktu: {mins:02d}:{secs:02d}
    </div>
    """,
    unsafe_allow_html=True,
)

# ========================= LOAD SOAL =========================
current_sub = daftar_tes[tes_index]
st.title(f"🧠 {current_sub.replace('_',' ')}")

soal_list = []
module_name = subtest_to_module(current_sub)

try:
    soal_module = importlib.import_module(module_name)
except ModuleNotFoundError:
    soal_module = None
    st.error(f"❌ Modul soal tidak ditemukan: {module_name}")

if soal_module and hasattr(soal_module, "soal_list"):
    for s in soal_module.soal_list:
        s["is_header"] = s.get("is_header", False)
        soal_list.append(s)

import random
order_key = f"order_{current_sub}"

if order_key not in st.session_state:
    idx = list(range(len(soal_list)))
    random.shuffle(idx)
    st.session_state[order_key] = idx

if "jawaban_peserta" not in st.session_state:
    st.session_state["jawaban_peserta"] = {}

# ========================= RENDER SOAL =========================
nomor_visible = 0
indices_order = st.session_state.get(order_key, [])

for orig_idx in indices_order:
    if orig_idx >= len(soal_list):
        continue

    item = soal_list[orig_idx]

    if item.get("is_header"):
        st.markdown(f"### {item['soal']}")
        continue

    nomor_visible += 1
    st.write(f"**{nomor_visible}. {item['soal']}**")

    if "pilihan" in item and item["pilihan"]:
        pilihan = item["pilihan"]
    elif "opsi" in item and item["opsi"]:
        pilihan = item["opsi"]
    elif "skor" in item and isinstance(item["skor"], dict):
        pilihan = list(item["skor"].values())
    else:
        pilihan = ["Tidak ada opsi"]

    key = f"{current_sub}_q{orig_idx+1}"

    if key not in st.session_state["jawaban_peserta"]:
        st.session_state["jawaban_peserta"][key] = None

    radio_key = f"radio_{current_sub}_{orig_idx+1}"
    prev = st.session_state["jawaban_peserta"].get(key)

    try:
        index_param = pilihan.index(prev) if prev in pilihan else None
    except:
        index_param = None

    jawab = st.radio("Pilih jawaban:", pilihan, key=radio_key, index=index_param)
    st.session_state["jawaban_peserta"][key] = jawab

    st.markdown("---")

# ========================= HITUNG & SIMPAN KE SESSION =========================
def save_subtest_result(sub_id):
    skor = 0
    keterangan = "-"

    module_path = subtest_to_module(sub_id)

    try:
        m = importlib.import_module(module_path)
    except:
        m = None

    if m and hasattr(m, "hitung_skor"):
        try:
            res = m.hitung_skor(st.session_state["jawaban_peserta"])
            skor = res.get("skor", 0)
            keterangan = res.get("keterangan", "-")
        except:
            skor = 0
            keterangan = "error_hitung"
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

    if "hasil_semua_subtes" not in st.session_state:
        st.session_state["hasil_semua_subtes"] = []

    st.session_state["hasil_semua_subtes"] = [
        h for h in st.session_state["hasil_semua_subtes"]
        if h["subtes"] != sub_id
    ]

    st.session_state["hasil_semua_subtes"].append({
        "subtes": sub_id,
        "skor": skor,
        "keterangan": keterangan
    })

# ========================= SIMPAN SEKALI KE DB + SHEETS =========================
def simpan_semua_hasil_ke_sheets():
    if "hasil_semua_subtes" not in st.session_state:
        return
    
    nama_user = biodata.get("Nama", "")
    job_user = biodata.get("Job Title", "")
    tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for h in st.session_state["hasil_semua_subtes"]:
        insert_hasil(nama_user, job_user, h["subtes"], h["skor"], h["keterangan"], tanggal)
        append_result(nama_user, job_user, h["subtes"], h["skor"], h["keterangan"], tanggal)

# ========================= WAKTU HABIS =========================
if rem == 0:
    st.info("⏰ Waktu total habis — tes selesai.")
    save_subtest_result(current_sub)
    simpan_semua_hasil_ke_sheets()
    st.session_state["selesai"] = True
    st.switch_page("pages/4_Terima_Kasih.py")

# ========================= NAVIGASI =========================
col1, col2, col3 = st.columns([1,2,1])

with col1:
    if st.button("⬅️ Kembali") and tes_index > 0:
        save_subtest_result(current_sub)
        st.session_state["tes_index"] -= 1
        st.rerun()

with col3:
    if tes_index < len(daftar_tes) - 1:
        if st.button("Lanjut ➡️"):
            save_subtest_result(current_sub)
            st.session_state["tes_index"] += 1
            st.rerun()
    else:
        if st.button("✅ Selesai"):
            save_subtest_result(current_sub)
            simpan_semua_hasil_ke_sheets()
            st.session_state["selesai"] = True
            st.switch_page("pages/4_Terima_Kasih.py")
