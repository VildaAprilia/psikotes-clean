import streamlit as st

st.set_page_config(page_title="Terima Kasih", page_icon="🎉", layout="centered")

if "selesai" not in st.session_state:
    st.warning("⚠️ Anda belum menyelesaikan tes.")
    st.stop()

st.title("🎉 Terima Kasih Telah Menyelesaikan Tes Psikotes!")

st.markdown(
    """
    Kami mengucapkan **terima kasih** atas partisipasi Anda dalam tes psikotes ini.  
    Jawaban Anda telah tersimpan dengan aman dan akan diproses oleh admin untuk evaluasi hasil.
    
    ---
    Silakan **menutup halaman ini** atau kembali ke **beranda utama** jika diperlukan.
    """
)

if st.button("🏠 Kembali ke Beranda"):
    st.session_state.clear()
    st.switch_page("app.py")  # pastikan halaman utama bernama Home.py
