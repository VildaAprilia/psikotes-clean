import streamlit as st
import os
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Biodata Peserta", page_icon="🧾", layout="centered")

st.title("📋 Formulir Biodata Peserta")

with st.form("biodata_form"):
    nama = st.text_input("Nama Lengkap")
    email = st.text_input("Email")
    usia = st.number_input("Usia", min_value=1, max_value=100, step=1)
    jenis_kelamin = st.selectbox("Jenis Kelamin", ["", "Laki-laki", "Perempuan"])
    pendidikan = st.selectbox("Pendidikan Terakhir", ["", "SMA/SMK", "D3", "S1", "S2"])
    jurusan = st.text_input("Jurusan")
    no_hp = st.text_input("No. HP")
    job_title = st.selectbox(
        "Job Title",
        ["", "Kepala Bengkel", "Kepala Mekanik", "Service Advisor", "Front Desk", 
         "Part Counter", "Kepala Dealer", "Admin CRM", "Mekanik"],
    )

    st.markdown("### 🖼️ Foto Peserta")
    st.write("Kamu bisa **unggah foto** atau **ambil langsung dari kamera** di bawah ini.")

    # Folder simpan foto
    os.makedirs("foto_peserta", exist_ok=True)

    # Opsi 1: Ambil dari kamera
    foto_kamera = st.camera_input("Ambil foto dengan kamera (opsional)")

    # Opsi 2: Upload dari file
    foto_upload = st.file_uploader("Atau unggah foto (format: JPG/PNG)", type=["jpg", "jpeg", "png"])

    submitted = st.form_submit_button("💾 Simpan dan Lanjut Tes")

# ---- Setelah submit ----
if submitted:
    if not nama or not email or not job_title:
        st.warning("⚠️ Harap lengkapi semua data wajib (Nama, Email, dan Job Title).")
    else:
        # Tentukan file foto
        foto_path = ""
        if foto_kamera is not None:
            foto_path = f"foto_peserta/{nama.replace(' ', '_')}_kamera_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
            with open(foto_path, "wb") as f:
                f.write(foto_kamera.getbuffer())
        elif foto_upload is not None:
            ext = os.path.splitext(foto_upload.name)[1]
            foto_path = f"foto_peserta/{nama.replace(' ', '_')}_upload_{datetime.now().strftime('%Y%m%d%H%M%S')}{ext}"
            with open(foto_path, "wb") as f:
                f.write(foto_upload.getbuffer())

        # Simpan biodata ke session
        biodata_dict = {
            "Nama": nama,
            "Email": email,
            "Usia": usia,
            "Jenis Kelamin": jenis_kelamin,
            "Pendidikan": pendidikan,
            "Jurusan": jurusan,
            "No HP": no_hp,
            "Job Title": job_title,
            "Foto Path": foto_path,
            "Tanggal Submit": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.session_state["biodata"] = biodata_dict
        st.session_state["biodata_selesai"] = True

        # ---- Simpan ke CSV ----
        os.makedirs("data", exist_ok=True)
        file_csv = "data/biodata.csv"
        if os.path.exists(file_csv):
            df_bio = pd.read_csv(file_csv)
            # Cek apakah nama/email sudah ada, jika ada update, jika tidak tambah
            if ((df_bio["Nama"] == nama) & (df_bio["Email"] == email)).any():
                df_bio.loc[(df_bio["Nama"] == nama) & (df_bio["Email"] == email), :] = pd.DataFrame([biodata_dict])
            else:
                df_bio = pd.concat([df_bio, pd.DataFrame([biodata_dict])], ignore_index=True)
        else:
            df_bio = pd.DataFrame([biodata_dict])

        df_bio.to_csv(file_csv, index=False)

        st.success("✅ Biodata tersimpan!")
        st.rerun()

# ---- Setelah biodata tersimpan ----
if st.session_state.get("biodata_selesai", False):
    st.success("✅ Terima kasih! Data Anda telah disimpan.")
    
    foto_path = st.session_state["biodata"].get("Foto Path")
    if foto_path and os.path.exists(foto_path):
        st.image(foto_path, caption="Foto peserta", width=200)

    st.info("Klik tombol di bawah untuk melanjutkan ke halaman tes.")
    if st.button("➡️ Lanjut ke Halaman Tes"):
        st.switch_page("pages/2_Pilih_Tes.py")
