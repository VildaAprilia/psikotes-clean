# ===============================
# pages/5_Admin.py
# ===============================

import streamlit as st
import pandas as pd
import os
from io import BytesIO
import matplotlib.pyplot as plt

# REPORTLAB
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# DATABASE
from utils.sheets import read_all_results

# ================= CONFIG =================
st.set_page_config(page_title="Admin - Hasil Psikotes", page_icon="📊")

# ================= LOGIN =================
ADMIN_CREDENTIALS = {"admin": "12345", "vilda": "aprilia"}

if "admin_logged_in" not in st.session_state:
    st.session_state["admin_logged_in"] = False

if not st.session_state["admin_logged_in"]:
    st.title("🔐 Login Admin")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Login"):
        if u in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[u] == p:
            st.session_state["admin_logged_in"] = True
            st.rerun()
        else:
            st.error("Username / Password salah")
    st.stop()

@st.cache_data(ttl=10)
def load_data():
    return read_all_results()

df = load_data()

st.title("📋 Hasil Psikotes Peserta")
if st.button("🚪 Logout"):
    st.session_state["admin_logged_in"] = False
    st.rerun()

# ================= LOAD DATA =================
df = read_all_results()
if df is None or df.empty:
    st.warning("Belum ada data hasil tes.")
    st.stop()

df.columns = [c.lower().strip() for c in df.columns]
df = df.rename(columns={
    "nama": "Nama",
    "job_title": "Job Title",
    "subtes": "Subtes",
    "skor": "Skor",
    "keterangan": "Keterangan",
    "tanggal_tes": "Tanggal Tes",
    "foto_path": "Foto Path"
})

# ================= PILIH PESERTA =================
peserta_list = sorted(df["Nama"].dropna().unique())
peserta = st.selectbox("Pilih Peserta", peserta_list)
df_p = df[df["Nama"] == peserta].copy()

st.dataframe(df_p, width="stretch")

# ================= GRAFIK =================
fig, ax = plt.subplots(figsize=(7,4))
ax.barh(df_p["Subtes"], df_p["Skor"])
ax.set_xlim(0, 100)
ax.set_title(f"Psikogram - {peserta}")
st.pyplot(fig)


# ================= NORMALISASI =================
df_p["Subtes_norm"] = (
    df_p["Subtes"]
    .astype(str)
    .str.lower()
    .str.replace("_", " ")
    .str.strip()
)


# ================= HELPER =================
def ambil_nilai(aspek):
    aspek = aspek.lower().replace("_", " ").strip()
    row = df_p[df_p["Subtes_norm"].str.contains(aspek, na=False)]

    if row.empty:
        return "-", "-"

    skor = row.iloc[0]["Skor"]
    ket = row.iloc[0]["Keterangan"]

    if skor in [0, None, "", "0"]:
        return "-", "-"

    skor = int(skor)

    if "intelegensi" in aspek:
        if skor < 90:
            ket = "Di bawah rata-rata"
        elif skor <= 109:
            ket = "Rata-rata"
        elif skor <= 119:
            ket = "Di atas rata-rata"
        elif skor <= 129:
            ket = "Superior"
        else:
            ket = "Very Superior"

    return skor, ket if ket else "-"


# ================= STRUKTUR ASPEK =================
ASPEK = [
    ("I. INTELEGENSI", ["Intelegensi Umum"]),
    ("II. KESIAPAN KERJA", [
        "Logika", "Numerikal", "Persepsi", "Analisa Sintesa",
        "Spasial", "Verbal", "Daya Ingat", "Daya Tahan",
        "Motivasi", "Psikomotorik"
    ]),
    ("III. KECERDASAN EMOSI", [
        "Kemandirian", "Kepercayaan Diri", "Kerjasama",
        "Sosialisasi", "Stabilitas Emosi", "Tanggung Jawab"
    ]),
    ("IV. DOMINASI KERJA OTAK", ["Dominasi Otak"]),
    ("V. GAYA BEKERJA", ["Gaya Bekerja"]),
    ("VI. KEPRIBADIAN", [
        "Kepribadian RIASEC Model",
        "Kepribadian Sanguinis Melankolis Kholeris Plegmatis"
    ])
]


# ================= PDF PSIKOGRAM =================
def generate_pdf(nama):
    os.makedirs("hasil", exist_ok=True)
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    w, h = A4

    biodata = df_p.iloc[0]
    job = biodata.get("Job Title", "-")
    tgl = biodata.get("Tanggal Tes", "-")
    foto = biodata.get("Foto Path", "")

    # HEADER CORPORATE
    c.setFillColor(colors.darkblue)
    c.rect(0, h-70, w, 70, fill=True, stroke=False)

    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.white)
    c.drawString(40, h-40, "PSIKOGRAM HASIL PEMERIKSAAN PSIKOLOGI")

    # BIODATA
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, h-100, f"Nama           :  {nama}")
    c.drawString(40, h-120, f"Posisi Dilamar :  {job}")
    c.drawString(40, h-140, f"Tanggal Tes    :  {tgl}")

    # FOTO
    if foto and os.path.exists(foto):
        try:
            img = ImageReader(foto)
            c.drawImage(img, w-170, h-200, width=110, height=130, preserveAspectRatio=True, mask="auto")
            c.rect(w-175, h-205, 120, 140)
        except:
            pass

    style = ParagraphStyle(name="Normal", fontSize=9, leading=12, alignment=TA_LEFT)

    table_data = [[
        Paragraph("<b>No</b>", style),
        Paragraph("<b>Aspek Psikologis</b>", style),
        Paragraph("<b>Skor</b>", style),
        Paragraph("<b>Keterangan</b>", style),
    ]]

    no = 1
    for kategori, subs in ASPEK:
        table_data.append(["", Paragraph(f"<b>{kategori}</b>", style), "", ""])
        for s in subs:
            skor, ket = ambil_nilai(s)
            table_data.append([str(no), s, str(skor), ket])
            no += 1

    table = Table(table_data, colWidths=[1.2*cm, 6.8*cm, 2*cm, 6.8*cm], repeatRows=1)
    table.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.4, colors.grey),
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("ALIGN", (2,1), (2,-1), "CENTER"),
    ]))

    tw, th = table.wrap(w-80, h)
    y = h - 260 - th
    if y < 80:
        y = 80

    table.drawOn(c, 40, y)

    c.setFont("Helvetica", 8)
    c.drawString(
        40, 60,
        "Skala Inteligensi: <90 Dibawah rata-rata | 90–109 Rata-rata | 110–119 Di atas rata-rata | 120–129 Superior | >130 Very Superior"
    )

    c.showPage()
    c.save()
    buffer.seek(0)

    path = f"hasil/Hasil_Psikotes_{nama.replace(' ', '_')}.pdf"
    with open(path, "wb") as f:
        f.write(buffer.getbuffer())

    return buffer, path


if st.button("📄 Buat & Unduh PDF Psikogram"):
    buf, path = generate_pdf(peserta)
    st.download_button("⬇️ Download PDF", buf, os.path.basename(path), "application/pdf")


# ================= AI KORELASI =================
import openai

st.markdown("### 🧠 Analisis AI Korelasi Posisi Jabatan")

AI_ACTIVE = "OPENAI_API_KEY" in st.secrets

if "ai_korelasi" not in st.session_state:
    st.session_state["ai_korelasi"] = None


# ====== GENERATE AI ATAU INPUT MANUAL ======
if not AI_ACTIVE:
    st.info("⚠️ AI dimatikan karena tidak ada OPENAI_API_KEY.")
    st.session_state["ai_korelasi"] = st.text_area(
        "Tuliskan analisis korelasi secara manual:",
        st.session_state["ai_korelasi"] or ""
    )

else:
    if st.button("🔎 Generate Analisis Korelasi AI"):
        try:
            job = df_p.iloc[0].get("Job Title","-")
            summary = df_p[["Subtes","Skor"]].to_dict(orient="records")

            prompt = f"""
            Kamu adalah psikolog industri.
            Analisis hasil psikotes dan tentukan kecocokan kandidat
            dengan posisi {job}.

            Output format:
            Status: Priority / Rekomendasi / Dipertimbangkan / Tidak Direkomendasi
            Alasan:
            """

            client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role":"user","content":prompt}],
                temperature=0.4
            )

            st.session_state["ai_korelasi"] = res.choices[0].message.content.strip()
            st.success("Analisis AI berhasil dibuat ✅")

        except Exception as e:
            st.error(f"Gagal analisis: {e}")


# ====== PDF FUNCTION (PASTI DI LUAR IF) ======
def generate_pdf_korelasi(nama, ai_text):
    buffer = BytesIO()
    os.makedirs("hasil", exist_ok=True)

    biodata = df_p.iloc[0]
    job = biodata.get("Job Title","-")
    tanggal = biodata.get("Tanggal Tes","-")

    filename = f"hasil/Korelasi_{nama.replace(' ','_')}.pdf"

    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("LAPORAN KORELASI PSIKOTES & POSISI JABATAN", styles["Heading2"]))
    elements.append(Spacer(1,12))
    elements.append(Paragraph(f"<b>Nama:</b> {nama}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Posisi Dilamar:</b> {job}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Tanggal Tes:</b> {tanggal}", styles["Normal"]))
    elements.append(Spacer(1,12))
    elements.append(Paragraph(ai_text.replace("\n","<br/>"), styles["Normal"]))

    doc.build(elements)
    buffer.seek(0)

    with open(filename,"wb") as f:
        f.write(buffer.getbuffer())

    return buffer, filename


# ====== SHOW & DOWNLOAD ======
if st.session_state["ai_korelasi"]:
    st.subheader("📄 Hasil Analisis Korelasi")
    st.write(st.session_state["ai_korelasi"])

    if st.button("📄 Buat & Unduh PDF Korelasi"):
        buf, path = generate_pdf_korelasi(peserta, st.session_state["ai_korelasi"])
        st.download_button(
            "⬇️ Download PDF Korelasi",
            buf,
            os.path.basename(path),
            "application/pdf"
        )
