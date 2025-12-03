# pages/3_Tes_Psikotes.py
import streamlit as st
import importlib
import os
import pandas as pd
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

from utils.durations import DURASI_CUSTOM, DEFAULT_DURATION

st.set_page_config(page_title="Tes Psikotes", page_icon="🧩", layout="wide")

# Jika sudah selesai
if st.session_state.get("selesai", False):
    st.info("Tes sudah selesai. Mengarahkan ke halaman berikutnya...")
    st.switch_page("pages/4_Terima_Kasih.py")
    st.stop()

# Basic validation
if "biodata" not in st.session_state or "daftar_tes" not in st.session_state:
    st.warning("⚠️ Silakan kembali untuk mengisi biodata dan memilih tes.")
    st.stop()

biodata = st.session_state["biodata"]
daftar_tes = st.session_state["daftar_tes"]
tes_index = st.session_state.get("tes_index", 0)

# Convert subtest id → module path
def subtest_to_module(sub_id):
    parts = sub_id.split("_")
    if len(parts) >= 3:
        folder_candidate = f"{parts[0]}_{parts[1]}"
        sub_candidate = "_".join(parts[2:])
        folder_path = os.path.join("soal", folder_candidate)
        if os.path.isdir(folder_path):
            return f"soal.{folder_candidate}.{sub_candidate}"
    if len(parts) >= 2:
        folder_candidate = parts[0]
        sub_candidate = "_".join(parts[1:])
        folder_path = os.path.join("soal", folder_candidate)
        if os.path.isdir(folder_path):
            return f"soal.{folder_candidate}.{sub_candidate}"
    return f"soal.{sub_id}"

# Ambil durasi subtes
def get_duration_for_sub(sub_id):
    if sub_id in DURASI_CUSTOM:
        return DURASI_CUSTOM[sub_id]
    tail = sub_id.split("_")[-1]
    return DURASI_CUSTOM.get(tail, DEFAULT_DURATION)

# ---------------------------------------------
#  TIMER GLOBAL (MENJUMLAHKAN SEMUA SUBTES)
# ---------------------------------------------
def init_global_timer():
    if "global_timer_initialized" in st.session_state:
        return

    total_minutes = 0
    for sub in daftar_tes:
        total_minutes += get_duration_for_sub(sub)

    now = datetime.now()
    st.session_state["global_start"] = now
    st.session_state["global_end"] = now + timedelta(minutes=total_minutes)
    st.session_state["global_total_minutes"] = total_minutes
    st.session_state["global_timer_initialized"] = True

# jalankan timer global sekali
init_global_timer()

# sisa waktu global
def remaining_seconds():
    delta = (st.session_state["global_end"] - datetime.now()).total_seconds()
    return max(0, int(delta))


# ---------------------------------------------
#               TAMPILKAN TIMER GLOBAL
# ---------------------------------------------
st_autorefresh(interval=1000, key="tick")

rem = remaining_seconds()
mins = rem // 60
secs = rem % 60

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

# identitas subtes aktif
current_sub = daftar_tes[tes_index]
st.title(f"🧠 {current_sub.replace('_',' ')}")

# Load module soal
soal_list = []
module_name = subtest_to_module(current_sub)

try:
    soal_module = importlib.import_module(module_name)
except ModuleNotFoundError:
    st.error(f"❌ Modul soal tidak ditemukan: {module_name}")
    soal_module = None

# ambil soal
if soal_module and hasattr(soal_module, "soal_list"):
    for s in soal_module.soal_list:
        s["is_header"] = s.get("is_header", False)
        soal_list.append(s)

import random

# acak sekali
order_key = f"order_{current_sub}"

if order_key not in st.session_state:
    indices = list(range(len(soal_list)))
    random.shuffle(indices)
    st.session_state[order_key] = indices

# tempat jawaban
if "jawaban_peserta" not in st.session_state:
    st.session_state["jawaban_peserta"] = {}

# ---------------------------------------------
#           RENDER SOAL
# ---------------------------------------------
nomor_visible = 0
indices_order = st.session_state.get(order_key, [])

for orig_idx in indices_order:
    if orig_idx >= len(soal_list):
        continue

    item = soal_list[orig_idx]

    # Header
    if item.get("is_header"):
        st.markdown(f"### {item['soal']}")
        continue

    nomor_visible += 1
    st.write(f"**{nomor_visible}. {item['soal']}**")

    # pilihan jawaban kosong dulu
    if "pilihan" in item and item["pilihan"]:
        pilihan = item["pilihan"]
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

    if index_param is not None:
        jawab = st.radio("Pilih jawaban:", pilihan, key=radio_key, index=index_param)
    else:
        jawab = st.radio("Pilih jawaban:", pilihan, key=radio_key, index=None)

    st.session_state["jawaban_peserta"][key] = jawab

    st.markdown("---")

# ---------------------------------------------
#         SIMPAN SKOR
# ---------------------------------------------
def save_subtest_result(sub_id):
    os.makedirs("data", exist_ok=True)

    skor = 0
    keterangan = "-"

    module_name = subtest_to_module(sub_id)
    try:
        m = importlib.import_module(module_name)
    except ModuleNotFoundError:
        m = None

    # custom scoring
    if m and hasattr(m, "hitung_skor"):
        try:
            res = m.hitung_skor(st.session_state["jawaban_peserta"])
            skor = res.get("skor", 0)
            keterangan = res.get("keterangan", "")
        except:
            skor = 0
            keterangan = "error_hitung"
    else:
        soal_temp = m.soal_list if m and hasattr(m, "soal_list") else []
        for i, it in enumerate(soal_temp, start=1):
            k = f"{sub_id}_q{i}"
            user_answer = st.session_state["jawaban_peserta"].get(k)

            if "jawaban_benar" in it:
                if user_answer == it["jawaban_benar"]:
                    skor += 4
            elif "skor" in it and isinstance(it["skor"], dict):
                for nilai, teks in it["skor"].items():
                    if teks == user_answer:
                        try:
                            skor += int(nilai)
                        except:
                            pass
                        break

    row = {
        "Nama": biodata.get("Nama", ""),
        "Job Title": biodata.get("Job Title", ""),
        "Subtes": sub_id,
        "Skor": skor,
        "Keterangan": keterangan,
        "Tanggal Tes": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    path = "data/hasil_peserta.csv"
    if os.path.exists(path):
        try:
            df_old = pd.read_csv(path)
            df_new = pd.DataFrame([row])
            df = pd.concat([df_old, df_new], ignore_index=True)
        except:
            df = pd.DataFrame([row])
    else:
        df = pd.DataFrame([row])

    df.to_csv(path, index=False)


# ---------------------------------------------
#      JIKA WAKTU GLOBAL HABIS
# ---------------------------------------------
if rem == 0:
    st.info("⏰ Waktu total habis — tes selesai.")
    save_subtest_result(current_sub)
    st.session_state["selesai"] = True
    st.rerun()


# ---------------------------------------------
#       NAVIGASI SUBTES
# ---------------------------------------------
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
            st.session_state["selesai"] = True
            st.switch_page("pages/4_Terima_Kasih.py")
