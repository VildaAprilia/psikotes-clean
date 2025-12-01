# pages/5_Admin.py
import streamlit as st
import pandas as pd
import os
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from io import BytesIO
import matplotlib.pyplot as plt
import re

# reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.utils import ImageReader

# ------------------- KONFIG HALAMAN -------------------
st.set_page_config(page_title="Admin - Hasil Psikotes", page_icon="📊")

# ------------------- LOGIN ADMIN -------------------
ADMIN_CREDENTIALS = {"admin": "12345", "vilda": "aprilia"}
if "admin_logged_in" not in st.session_state:
    st.session_state["admin_logged_in"] = False

if not st.session_state["admin_logged_in"]:
    st.title("🔐 Halaman Login Admin")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username] == password:
            st.session_state["admin_logged_in"] = True
            st.success("✅ Login berhasil.")
            st.rerun()
        else:
            st.error("❌ Username atau password salah.")
    st.stop()

st.title("📋 Hasil Psikotes Peserta")
if st.button("🚪 Logout"):
    st.session_state["admin_logged_in"] = False
    st.rerun()

# ------------------- LOAD DATA -------------------
os.makedirs("data", exist_ok=True)
file_path = "data/hasil_peserta.csv"
if not os.path.exists(file_path):
    st.warning("📂 Belum ada hasil tes yang tersimpan (data/hasil_peserta.csv).")
    st.stop()

try:
    df = pd.read_csv(file_path)
except Exception as e:
    st.error(f"Gagal membaca file: {e}")
    st.stop()

if df.empty:
    st.warning("⚠️ File hasil_peserta.csv kosong.")
    st.stop()

# ------------------- PILIH PESERTA -------------------
st.markdown("### 🔍 Pilih Peserta")
peserta_list = df["Nama"].unique().tolist()
peserta = st.selectbox("Pilih peserta:", peserta_list)

df_peserta = df[df["Nama"] == peserta].copy()
st.dataframe(df_peserta)

# ------------------- GRAFIK -------------------
st.markdown("### 📊 Grafik Psikogram")
fig, ax = plt.subplots(figsize=(7, 4))
ax.barh(df_peserta["Subtes"], df_peserta["Skor"], color="skyblue")
ax.set_xlabel("Skor")
ax.set_xlim(0, 100)
ax.set_ylabel("Aspek Psikologis")
ax.set_title(f"Psikogram - {peserta}")
plt.tight_layout()
st.pyplot(fig)

# ------------------- GET VALUE FUNCTION -------------------
def get_value_for_aspect(df_participant, aspect_name):
    df_participant["Subtes"] = (
        df_participant["Subtes"]
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace("_", " ")
    )
    aspect_name_clean = aspect_name.strip().lower().replace("_", " ")

    match = df_participant[
        df_participant["Subtes"].str.contains(rf"\b{re.escape(aspect_name_clean)}\b", na=False)
    ]
    if match.empty:
        skor = 0
        ket = "-"
    else:
        row = match.iloc[0]
        skor = row.get("Skor", 0)
        if pd.isna(skor):
            skor = 0
        ket = str(row.get("Keterangan", "")).strip()
        if ket == "":
            ket = "-"

    if skor == 0:
        return 0, "-"

    if "intelegensi" in aspect_name_clean:
        if skor < 90:
            ket = "Di bawah rata-rata"
        elif 90 <= skor <= 109:
            ket = "Rata-rata"
        elif 110 <= skor <= 119:
            ket = "Di atas rata-rata"
        elif 120 <= skor <= 129:
            ket = "Superior"
        else:
            ket = "Very Superior"
    elif any(x in aspect_name_clean for x in [
        "logika", "numerikal", "persepsi", "analisa", "spasial", "verbal",
        "daya ingat", "daya tahan", "motivasi", "psikomotorik"
    ]):
        ket = f"{int(skor)} / 100"
    elif "dominasi otak" in aspect_name_clean:
        ket = ket if ket not in ["", "-"] else ("Kanan" if skor >= 50 else "Kiri")
    else:
        if ket in ["", "-"] and skor > 0:
            ket = ""
    return int(skor), ket

# ------------------- GENERATE PDF RINGKAS -------------------
def generate_pdf_full(nama, df_participant, fig):
    os.makedirs("hasil", exist_ok=True)
    filename = f"hasil/Hasil_Psikotes_{nama.replace(' ', '_')}.pdf"
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    biodata_row = df_participant.iloc[0]
    tgl_tes = biodata_row.get("Tanggal Tes", "—")
    pendidikan = biodata_row.get("Job Title", "—")
    foto_path = biodata_row.get("Foto Path", "")

    # --- HEADER ---
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, height - 50, "PSIKOGRAM HASIL PEMERIKSAAN PSIKOLOGI")
    c.setFont("Helvetica", 10)
    c.drawString(40, height - 75, f"Nama : {nama}")
    c.drawString(300, height - 75, f"Pendidikan : {pendidikan}")
    c.drawString(40, height - 90, f"Tanggal Tes : {tgl_tes}")

    # --- FOTO PESERTA ---
    if foto_path and os.path.exists(foto_path):
        try:
            img = ImageReader(foto_path)
            c.drawImage(img, width - 150, height - 150, width=80, height=90, preserveAspectRatio=True, mask='auto')
        except:
            pass

    # --- TABEL HASIL ---
    aspek = [
        ("I. INTELEGENSI", [("Intelegensi Umum", "")]),
        ("II. KESIAPAN KERJA", [
            ("Logika",""),("Numerikal",""),("Persepsi",""),("Analisa Sintesa",""),
            ("Spasial",""),("Verbal",""),("Daya Ingat",""),("Daya Tahan",""),
            ("Motivasi",""),("Psikomotorik","")
        ]),
        ("III. KECERDASAN EMOSI", [
            ("Kemandirian",""),("Kepercayaan Diri",""),("Kerjasama",""),
            ("Sosialisasi",""),("Stabilitas Emosi",""),("Tanggung Jawab","")
        ]),
        ("IV. DOMINASI KERJA OTAK", [("Dominasi Otak","")]),
        ("V. GAYA BEKERJA", [("Gaya Bekerja","")]),
        ("VI. KEPRIBADIAN", [
            ("Kepribadian RIASEC Model",""),
            ("Kepribadian Sanguinis Melankolis Kholeris Plegmatis","")
        ])
    ]

    style_normal = ParagraphStyle(name="Normal", fontName="Helvetica", fontSize=9, leading=11, alignment=TA_LEFT)
    style_bold = ParagraphStyle(name="Bold", fontName="Helvetica-Bold", fontSize=9, leading=11)

    table_data = [[Paragraph("<b>No</b>", style_bold),
                   Paragraph("<b>Aspek Psikologis</b>", style_bold),
                   Paragraph("<b>Skor</b>", style_bold),
                   Paragraph("<b>Keterangan</b>", style_bold)]]
    no = 1

    for kategori, subtes_list in aspek:
        table_data.append(["", Paragraph(f"<b>{kategori}</b>", style_bold), "", ""])
        for subtes, _ in subtes_list:
            skor, ket = get_value_for_aspect(df_participant, subtes)
            table_data.append([Paragraph(str(no), style_normal),
                               Paragraph(subtes, style_normal),
                               Paragraph(str(skor), style_normal),
                               Paragraph(ket, style_normal)])
            no += 1

    table = Table(table_data, colWidths=[1.0*cm, 6.0*cm, 2.0*cm, 7.5*cm])
    table.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.3, colors.grey),
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("ALIGN", (2,1), (2,-1), "CENTER"),
        ("LEFTPADDING", (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING", (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
    ]))

    w,h = table.wrap(width-80, height)
    table_y = max(100, height - h - 170)
    table.drawOn(c, 40, table_y)

    # --- FOOTER ---
    c.setFont("Helvetica", 8)
    c.drawString(40, 60, "Skala Inteligensi: <90 Di bawah rata-rata | 90–109 Rata-rata | 110–119 Di atas rata-rata | 120–129 Superior | >130 Very Superior")

    c.showPage()
    c.save()
    buffer.seek(0)

    with open(filename, "wb") as f:
        f.write(buffer.getbuffer())

    return buffer, filename

# ------------------- BUTTON PDF RINGKAS -------------------
if st.button("📄 Buat & Unduh PDF Ringkasan"):
    try:
        pdf_buf, save_path = generate_pdf_full(peserta, df_peserta, fig)
        st.success(f"PDF dibuat dan disimpan: {save_path}")
        st.download_button(label=f"⬇️ Unduh PDF {peserta}",
                           data=pdf_buf,
                           file_name=os.path.basename(save_path),
                           mime="application/pdf")
    except Exception as e:
        st.error(f"Gagal membuat PDF: {e}")

# ------------------- GENERATE PDF KORELASI -------------------
import openai

def generate_pdf_korelasi(nama, df_participant, ai_text):
    os.makedirs("hasil", exist_ok=True)
    filename = f"hasil/Korelasi_Job_{nama.replace(' ', '_')}.pdf"
    buffer = BytesIO()

    biodata_row = df_participant.iloc[0]
    job_title = biodata_row.get("Job Title", "Tidak diketahui")
    tgl_tes = biodata_row.get("Tanggal Tes", "—")
    foto_path = biodata_row.get("Foto Path", "")

    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    elements = []
    styles = getSampleStyleSheet()
    style_normal = styles["Normal"]
    style_bold = styles["Heading2"]

    # --- HEADER ---
    elements.append(Paragraph("LAPORAN KORELASI PSIKOTES & PEKERJAAN", style_bold))
    elements.append(Spacer(1, 0.5*cm))
    elements.append(Paragraph(f"<b>Nama :</b> {nama}", style_normal))
    elements.append(Paragraph(f"<b>Job Dilamar :</b> {job_title}", style_normal))
    elements.append(Paragraph(f"<b>Tanggal Tes :</b> {tgl_tes}", style_normal))
    elements.append(Spacer(1, 0.5*cm))

    # --- FOTO ---
    if foto_path and os.path.exists(foto_path):
        try:
            img = Image(foto_path, width=6*cm, height=7*cm)
            elements.append(img)
            elements.append(Spacer(1, 0.5*cm))
        except Exception as e:
            print("Gagal menampilkan foto:", e)

    # --- ANALISIS AI (wrap otomatis) ---
    if ai_text.strip() == "":
        ai_text = "Tidak ada hasil analisis AI."
    elements.append(Paragraph(ai_text.replace("\n", "<br />"), style_normal))

    # --- BUILD PDF ---
    doc.build(elements)
    buffer.seek(0)

    with open(filename, "wb") as f:
        f.write(buffer.getbuffer())

    return buffer, filename

# ------------------- BUTTON AI KORELASI -------------------
if st.button("🧠 Analisis Korelasi Job & Psikotes"):
    try:
        # --- Ambil data peserta & buat prompt AI ---
        biodata_row = df_peserta.iloc[0]
        job_title = biodata_row.get("Job Title", "Tidak diketahui")
        nama = biodata_row.get("Nama", "Peserta")
        summary = df_peserta[["Subtes", "Skor"]].to_dict(orient="records")

        ai_prompt = f"""
        Kamu adalah psikolog industri. Analisis hasil psikotes peserta bernama {nama},
        yang melamar posisi {job_title}. Tentukan status rekomendasi: 
        (Priority, Rekomendasi, Dipertimbangkan, atau Tidak Direkomendasi) 
        dan beri penjelasan ringkas. Data hasil tes: {summary}
        """

        # --- Panggil OpenAI ---
        import openai
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Kamu adalah psikolog kerja."},
                {"role": "user", "content": ai_prompt}
            ],
            temperature=0.7
        )
        ai_text = response.choices[0].message.content.strip()

        # --- Buat PDF ---
        pdf_buf, save_path = generate_pdf_korelasi(nama, df_peserta, ai_text)

        st.success(f"PDF Korelasi dibuat dan disimpan: {save_path}")
        st.download_button(
            label=f"⬇️ Unduh PDF Korelasi {nama}",
            data=pdf_buf,
            file_name=os.path.basename(save_path),
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"Gagal membuat PDF Korelasi: {e}")

