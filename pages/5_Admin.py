# pages/5_Admin.py
import streamlit as st
import pandas as pd
import os
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Image  # added Image
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
st.set_page_config(page_title="Admin - Hasil Psikotes", page_icon="📊", layout="wide")

# ------------------- LOGIN ADMIN -------------------
ADMIN_CREDENTIALS = {"admin": "12345", "vilda": "aprilia"}
if "admin_logged_in" not in st.session_state:
    st.session_state["admin_logged_in"] = False

if not st.session_state["admin_logged_in"]:
    st.markdown("## 🔐 Halaman Login Admin")
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

# ------------------- HEADER (rapi) -------------------
left_h, right_h = st.columns([9, 1])
with left_h:
    st.markdown("## 📋  Hasil Psikotes Peserta")
with right_h:
    if st.button("🚪 Logout"):
        st.session_state["admin_logged_in"] = False
        st.rerun()

st.markdown("---")

# ------------------- LOAD DATA -------------------
os.makedirs("data", exist_ok=True)
biodata_path = "data/biodata.csv"
hasil_path = "data/hasil_peserta.csv"

# load biodata (optional)
df_bio = None
if os.path.exists(biodata_path):
    try:
        df_bio = pd.read_csv(biodata_path)
    except Exception:
        df_bio = None

# load hasil peserta (required)
if not os.path.exists(hasil_path):
    st.warning("📂 Belum ada hasil tes yang tersimpan (data/hasil_peserta.csv).")
    st.stop()

try:
    df = pd.read_csv(hasil_path)
except Exception as e:
    st.error(f"Gagal membaca file: {e}")
    st.stop()

if df.empty:
    st.warning("⚠️ File hasil_peserta.csv kosong.")
    st.stop()

# normalize columns (safety)
df.columns = [c.strip() for c in df.columns]

# ------------------- DOWNLOAD DATA CSV (rapi dua kolom) -------------------
st.markdown("### 📥 Download Data")
dcol1, dcol2 = st.columns([1, 1])
with dcol1:
    if df_bio is not None:
        st.download_button(
            label="⬇️ Download biodata.csv",
            data=df_bio.to_csv(index=False).encode("utf-8"),
            file_name="biodata.csv",
            mime="text/csv",
            use_container_width=True,
        )
    else:
        st.info("File biodata.csv tidak ditemukan (opsional).")
with dcol2:
    st.download_button(
        label="⬇️ Download hasil_peserta.csv",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="hasil_peserta.csv",
        mime="text/csv",
        use_container_width=True,
    )

st.markdown("---")

# ------------------- PILIH PESERTA (main content + sidebar kanan) -------------------
left_col, right_col = st.columns([3, 1])

with left_col:
    st.markdown("### 🔍 Pilih Peserta")
    peserta_list = df["Nama"].fillna("Unknown").unique().tolist()
    peserta = st.selectbox("Pilih peserta:", peserta_list)

    df_peserta = df[df["Nama"] == peserta].copy()
    if df_peserta.empty:
        st.warning("Data peserta kosong.")
    else:
        # show dataframe compact
        st.dataframe(df_peserta.reset_index(drop=True), use_container_width=True, height=300)

with right_col:
    st.markdown("### ℹ️ Info Peserta")
    if 'df_peserta' in locals() and not df_peserta.empty:
        row0 = df_peserta.iloc[0]
        st.write(f"**Nama**: {row0.get('Nama','-')}")
        st.write(f"**Job Title**: {row0.get('Job Title','-')}")
        st.write(f"**Tanggal Tes**: {row0.get('Tanggal Tes','-')}")
        # lama pengerjaan
        if "Lama Pengerjaan" in df_peserta.columns:
            st.success(f"⏳ Lama pengerjaan: {df_peserta.iloc[0]['Lama Pengerjaan']}")
        else:
            st.info("⏳ Lama pengerjaan: belum dicatat.")
        st.markdown("---")
        # small summary stats
        try:
            total_score = int(df_peserta["Skor"].sum())
        except Exception:
            total_score = None
        if total_score is not None:
            st.metric("Total Skor (subtes)", total_score)
        # Buttons PDF di kanan
        if st.button("📄 Buat & Unduh PDF Ringkasan"):
            try:
                pdf_buf, save_path = generate_pdf_full(peserta, df_peserta, None)
                st.success(f"PDF dibuat dan disimpan: {save_path}")
                st.download_button(
                    label=f"⬇️ Unduh PDF {peserta}",
                    data=pdf_buf.getvalue() if hasattr(pdf_buf, "getvalue") else pdf_buf,
                    file_name=os.path.basename(save_path),
                    mime="application/pdf",
                    use_container_width=True,
                )
            except Exception as e:
                st.error(f"Gagal membuat PDF: {e}")

        st.markdown("")
        if st.button("🧠 Analisis Korelasi Job & Psikotes"):
            try:
                # prepare prompt and call OpenAI
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

                pdf_buf, save_path = generate_pdf_korelasi(nama, df_peserta, ai_text)

                st.success(f"PDF Korelasi dibuat: {save_path}")
                st.download_button(
                    label=f"⬇️ Unduh PDF Korelasi {nama}",
                    data=pdf_buf.getvalue() if hasattr(pdf_buf, "getvalue") else pdf_buf,
                    file_name=os.path.basename(save_path),
                    mime="application/pdf",
                    use_container_width=True,
                )
            except Exception as e:
                st.error(f"Gagal membuat PDF Korelasi: {e}")

    else:
        st.info("Pilih peserta di kolom kiri untuk melihat detail.")

st.markdown("---")

# ------------------- GRAFIK BESAR DI BAWAH (full width) -------------------
if 'df_peserta' in locals() and not df_peserta.empty:
    st.markdown("### 📊 Grafik Psikogram")
    fig, ax = plt.subplots(figsize=(10, 4))
    try:
        ax.barh(df_peserta["Subtes"], df_peserta["Skor"], color="skyblue")
        ax.set_xlabel("Skor")
        ax.set_xlim(0, max(100, int(df_peserta["Skor"].max()) + 10))
        ax.set_ylabel("Aspek Psikologis")
        ax.set_title(f"Psikogram - {peserta}")
        plt.tight_layout()
        st.pyplot(fig)
    except Exception:
        st.info("Tidak ada data grafik untuk peserta ini.")

# ------------------- HELPERS yang sudah ada (tidak diubah fungsi) -------------------
def get_value_for_aspect(df_participant, aspect_name):
    df_copy = df_participant.copy()
    df_copy["Subtes"] = (
        df_copy["Subtes"].astype(str).str.strip().str.lower().str.replace("_", " ")
    )
    aspect_name_clean = aspect_name.strip().lower().replace("_", " ")
    match = df_copy[
        df_copy["Subtes"].str.contains(rf"\b{re.escape(aspect_name_clean)}\b", na=False)
    ]
    if match.empty:
        return 0, "-"
    row = match.iloc[0]
    skor = row.get("Skor", 0)
    if pd.isna(skor):
        skor = 0
    ket = str(row.get("Keterangan", "")).strip() or "-"
    if skor == 0:
        return 0, ket
    if "intelegensi" in aspect_name_clean:
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
    return int(skor), ket

def generate_pdf_full(nama, df_participant, fig):
    # keep original implementation but safe-guarded: returns BytesIO buffer and filename
    os.makedirs("hasil", exist_ok=True)
    filename = f"hasil/Hasil_Psikotes_{nama.replace(' ', '_')}.pdf"
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    biodata_row = df_participant.iloc[0]
    tgl_tes = biodata_row.get("Tanggal Tes", "—")
    pendidikan = biodata_row.get("Job Title", "—")
    foto_path = biodata_row.get("Foto Path", "")

    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, height - 50, "PSIKOGRAM HASIL PEMERIKSAAN PSIKOLOGI")
    c.setFont("Helvetica", 10)
    c.drawString(40, height - 75, f"Nama : {nama}")
    c.drawString(300, height - 75, f"Pendidikan : {pendidikan}")
    c.drawString(40, height - 90, f"Tanggal Tes : {tgl_tes}")

    if foto_path and os.path.exists(foto_path):
        try:
            img = ImageReader(foto_path)
            c.drawImage(img, width - 150, height - 150, width=80, height=90, preserveAspectRatio=True)
        except:
            pass

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
    ]))

    w, h = table.wrap(width - 80, height)
    table.drawOn(c, 40, height - h - 180)

    c.showPage()
    c.save()
    buffer.seek(0)

    with open(filename, "wb") as f:
        f.write(buffer.getbuffer())

    return buffer, filename

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

    elements.append(Paragraph("LAPORAN KORELASI PSIKOTES & PEKERJAAN", style_bold))
    elements.append(Spacer(1, 0.5*cm))
    elements.append(Paragraph(f"<b>Nama :</b> {nama}", style_normal))
    elements.append(Paragraph(f"<b>Job Dilamar :</b> {job_title}", style_normal))
    elements.append(Paragraph(f"<b>Tanggal Tes :</b> {tgl_tes}", style_normal))
    elements.append(Spacer(1, 0.5*cm))

    if foto_path and os.path.exists(foto_path):
        try:
            img = Image(foto_path, width=6*cm, height=7*cm)
            elements.append(img)
            elements.append(Spacer(1, 0.5*cm))
        except Exception:
            pass

    if ai_text.strip() == "":
        ai_text = "Tidak ada hasil analisis AI."
    elements.append(Paragraph(ai_text.replace("\n", "<br />"), style_normal))

    doc.build(elements)
    buffer.seek(0)

    with open(filename, "wb") as f:
        f.write(buffer.getbuffer())

    return buffer, filename
