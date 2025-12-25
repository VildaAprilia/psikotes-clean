import streamlit as st
from utils.db import init_db
init_db()

# --- Konfigurasi halaman utama ---
st.set_page_config(page_title="Dashboard Tes Psikotes", page_icon="🧠", layout="centered")

st.title("🧠 Dashboard Tes Psikotes Online")
st.markdown("---")

st.markdown("""
Selamat datang di **Platform Tes Psikotes Online**.  
Silakan klik tombol di bawah untuk mengisi biodata sebelum memulai tes.

> Pastikan Anda mengisi data dengan benar, karena hasil tes akan disesuaikan dengan job title yang dipilih.
""")

# --- Tombol menuju halaman biodata ---
if st.button("➡️ Mulai Isi Biodata"):
    st.switch_page("pages/1_Biodata.py")

st.markdown("---")

st.caption("© 2025 Tes Psikotes Online — PT. Astra International Tbk. - Honda")
