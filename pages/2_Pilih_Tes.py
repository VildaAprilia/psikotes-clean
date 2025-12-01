# pages/2_Pilih_Tes.py
import streamlit as st
import pandas as pd
from utils.job_mapping import resolve_subtests_for_job
from utils.durations import DURASI_CUSTOM, DEFAULT_DURATION

st.set_page_config(page_title="Pilih Tes", page_icon="🧠", layout="centered")
st.title("🧭 Daftar Tes Psikotes")
st.markdown("---")

if "biodata" not in st.session_state:
    st.warning("⚠️ Silakan isi biodata terlebih dahulu.")
    st.stop()

biodata = st.session_state["biodata"]
job = biodata.get("Job Title", "")
st.subheader(f"Halo, {biodata.get('Nama','')} 👋")
st.write(f"Job Title: **{job}**")
st.markdown("---")

# Resolve subtests for this job (only existing ones)
daftar_tes = resolve_subtests_for_job(job)

if not daftar_tes:
    st.warning("⚠️ Belum ada subtes valid untuk posisi ini (atau file soal belum tersedia).")
    # optionally allow fallback to all subtests or stop
    st.stop()

# Prepare table with durations (lookup full id then tail)
def lookup_duration(sub_id):
    if sub_id in DURASI_CUSTOM:
        return DURASI_CUSTOM[sub_id]
    # try tail (after first two parts if folder name contains underscore)
    tail = sub_id.split("_")[-1]
    if tail in DURASI_CUSTOM:
        return DURASI_CUSTOM[tail]
    return DEFAULT_DURATION

data = []
total = 0
for s in daftar_tes:
    dur = lookup_duration(s)
    total += dur
    data.append({"Nama Subtes": s.replace("_", " "), "Durasi (menit)": dur})

st.success(f"📋 Anda akan mengikuti **{len(daftar_tes)} subtes**:")
st.dataframe(pd.DataFrame(data), hide_index=True)
st.info(f"🕒 Total durasi (jika dijumlah): **{total} menit**")
st.markdown("---")

if st.button("🚀 Mulai Tes Sekarang"):
    st.session_state["daftar_tes"] = daftar_tes
    st.session_state["tes_index"] = 0
    st.session_state["show_confirm"] = False
    
    # 🔥 RESET STATUS TES
    st.session_state["selesai"] = False
    st.session_state["jawaban_peserta"] = {}
    st.session_state.pop("sub_start", None)
    st.session_state.pop("sub_end", None)
    st.session_state.pop("last_index", None)
    
    st.switch_page("pages/3_Tes_Psikotes.py")
