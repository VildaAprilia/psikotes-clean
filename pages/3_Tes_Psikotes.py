# pages/3_Tes_Psikotes.py
import streamlit as st
import importlib
import os
import glob
import pandas as pd
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

from utils.durations import DURASI_CUSTOM, DEFAULT_DURATION
from utils.job_mapping import resolve_subtests_for_job

st.set_page_config(page_title="Tes Psikotes", page_icon="🧩", layout="wide")

# jika sudah selesai, langsung tampilkan kosong dan pindah ke halaman terima kasih
if st.session_state.get("selesai", False):
    st.info("Tes sudah selesai. Mengarahkan ke halaman berikutnya...")
    st.switch_page("pages/4_Terima_Kasih.py")
    st.stop()

# basic validation
if "biodata" not in st.session_state or "daftar_tes" not in st.session_state:
    st.warning("⚠️ Silakan kembali ke halaman sebelumnya untuk mengisi biodata dan memilih tes.")
    st.stop()

biodata = st.session_state["biodata"]
daftar_tes = st.session_state["daftar_tes"]
tes_index = st.session_state.get("tes_index", 0)

# helper to get module name from subtest id
def subtest_to_module(sub_id):
    # examples:
    # "Kesiapan_Kerja_Logika" -> soal.Kesiapan_Kerja.Logika
    # "Intelegensi_Umum" -> soal.Intelegensi_Umum
    parts = sub_id.split("_")
    # try folder = parts[0] + '_' + parts[1] if folder exists
    if len(parts) >= 3:
        folder_candidate = f"{parts[0]}_{parts[1]}"
        sub_candidate = "_".join(parts[2:])
        folder_path = os.path.join("soal", folder_candidate)
        if os.path.isdir(folder_path):
            return f"soal.{folder_candidate}.{sub_candidate}"
    # fallback: maybe folder is first part only
    if len(parts) >= 2:
        folder_candidate = parts[0]
        sub_candidate = "_".join(parts[1:])
        folder_path = os.path.join("soal", folder_candidate)
        if os.path.isdir(folder_path):
            return f"soal.{folder_candidate}.{sub_candidate}"
    # lastly treat as single module
    return f"soal.{sub_id}"

def get_duration_for_sub(sub_id):
    if sub_id in DURASI_CUSTOM:
        return DURASI_CUSTOM[sub_id]
    tail = sub_id.split("_")[-1]
    return DURASI_CUSTOM.get(tail, DEFAULT_DURATION)

# init per-subtest timer
def init_timer_for_index(idx):
    st.session_state["tes_index"] = idx
    sub_id = daftar_tes[idx]
    dur = get_duration_for_sub(sub_id)
    now = datetime.now()
    st.session_state["sub_start"] = now
    st.session_state["sub_end"] = now + timedelta(minutes=dur)
    st.session_state["sub_duration_minutes"] = dur

if "sub_start" not in st.session_state or st.session_state.get("last_index") != tes_index:
    init_timer_for_index(tes_index)
    st.session_state["last_index"] = tes_index

# remaining time for current subtest
def remaining_seconds():
    delta = (st.session_state["sub_end"] - datetime.now()).total_seconds()
    return max(0, int(delta))

st_autorefresh(interval=1000, key="tick")
rem = remaining_seconds()
mins = rem // 60
secs = rem % 60

current_sub = daftar_tes[tes_index]
st.title(f"🧠 {current_sub.replace('_',' ')}")
st.markdown(f"Durasi subtes saat ini: **{st.session_state.get('sub_duration_minutes', '?')} menit**")

st.markdown(
    f"""
    <div style="position: fixed; top: 70px; right: 30px;
                background-color: #f0f2f6; border: 2px solid #0066cc;
                border-radius: 10px; padding: 10px 18px; font-size: 18px;
                font-weight: bold; color: #0066cc; z-index: 9999;">
        ⏰ Sisa Waktu Subtes: {mins:02d}:{secs:02d}
    </div>
    """, unsafe_allow_html=True)

# load module for current subtest only
soal_list = []
module_name = subtest_to_module(current_sub)
try:
    soal_module = importlib.import_module(module_name)
except ModuleNotFoundError:
    st.error(f"❌ Modul soal tidak ditemukan: {module_name}")
    soal_module = None

# collect soal_list from module if present
if soal_module and hasattr(soal_module, "soal_list"):
    for s in soal_module.soal_list:
        s["is_header"] = False
        soal_list.append(s)
elif soal_module and hasattr(soal_module, "hitung_skor"):
    # module provides custom scoring; but still may not expose soal_list
    # we will rely on hitung_skor when saving
    soal_list = []

if not soal_list and not hasattr(soal_module, "hitung_skor"):
    st.warning("⚠️ Modul soal tidak menyediakan soal_list atau hitung_skor. Periksa file soal.")

# init jawaban store
if "jawaban_peserta" not in st.session_state:
    st.session_state["jawaban_peserta"] = {}

# render soal
nomor = 0
for item in soal_list:
    if item.get("is_header"):
        st.markdown(f"### {item['soal']}")
        continue
    nomor += 1
    st.write(f"**{nomor}. {item['soal']}**")
    pilihan = item.get("pilihan", [])
    key = f"{current_sub}_q{nomor}"
    if key not in st.session_state["jawaban_peserta"]:
        st.session_state["jawaban_peserta"][key] = None
    selected = st.session_state["jawaban_peserta"].get(key)
    index0 = None  
    radio_key = f"radio_{current_sub}_{nomor}"
    jawab = st.radio("Pilih jawaban:", pilihan, key=radio_key, index=index0)
    st.session_state["jawaban_peserta"][key] = jawab

st.markdown("---")

# saving for a single subtest (used on auto-advance or finish)
def save_subtest_result(sub_id):
    """
    Calculate score for one subtest (sub_id) using:
      - module.hitung_skor(...) if exists
      - else compare soal_list's jawaban_benar
    Append to CSV (data/hasil_peserta.csv)
    """
    os.makedirs("data", exist_ok=True)
    skor = 0
    keterangan = "-"
    module_name = subtest_to_module(sub_id)
    try:
        m = importlib.import_module(module_name)
    except ModuleNotFoundError:
        m = None

    if m and hasattr(m, "hitung_skor"):
        try:
            res = m.hitung_skor(st.session_state["jawaban_peserta"])
            skor = res.get("skor", 0)
            keterangan = res.get("keterangan", "")
        except Exception:
            skor = 0
            keterangan = "error_hitung"
    else:
        # load soal_list from module file (if module is folder/sub or single)
        soal_temp = []
        # try to load from module if available
        if m and hasattr(m, "soal_list"):
            soal_temp = m.soal_list
        else:
            # try to find file physically and import to get soal_list
            # sub_id -> module path handled earlier, but already attempted
            soal_temp = []

        for i, it in enumerate(soal_temp, start=1):
            k = f"{sub_id}_q{i}"
            if st.session_state["jawaban_peserta"].get(k) == it.get("jawaban_benar"):
                skor += 4

    # append to CSV
    row = {
        "Nama": biodata.get("Nama",""),
        "Job Title": biodata.get("Job Title",""),
        "Subtes": sub_id,
        "Skor": skor,
        "Keterangan": keterangan,
        "Tanggal Tes": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    path = "data/hasil_peserta.csv"
    if os.path.exists(path):
        df_old = pd.read_csv(path)
        df_new = pd.DataFrame([row])
        df = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df = pd.DataFrame([row])
    df.to_csv(path, index=False)

# auto-advance when time up
if rem == 0:
    st.info("Waktu subtes habis — menyimpan dan lanjut...")
    save_subtest_result(current_sub)
    if tes_index < len(daftar_tes) - 1:
        # init_timer_for_index = None  # no-op placeholder (we re-call below)
        # set next index and re-init timer
        st.session_state["tes_index"] = tes_index + 1
        st.rerun()
    else:
        st.success("Semua subtes selesai. Menyimpan hasil akhir...")
        st.session_state["selesai"] = True
        st.rerun()

# manual navigation buttons
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("⬅️ Kembali") and tes_index > 0:
        # optionally save current before going back
        save_subtest_result(current_sub)
        st.session_state["tes_index"] = tes_index - 1
        st.rerun()

with col3:
    if tes_index < len(daftar_tes) - 1:
        if st.button("Lanjut ➡️"):
            save_subtest_result(current_sub)
            st.session_state["tes_index"] = tes_index + 1
            st.rerun()
    else:
        if st.button("✅ Selesai"):
            save_subtest_result(current_sub)
            st.session_state["selesai"] = True
            st.switch_page("pages/4_Terima_Kasih.py")


