# soal_kepribadian_riasec.py
# ---------------------------------------------
# Tes Kepribadian RIASEC (Holland Model)
# ---------------------------------------------
# Panduan penilaian:
# Skor 4 = Sangat Sesuai
# Skor 3 = Cukup Sesuai
# Skor 2 = Sedikit Sesuai
# Skor 1 = Tidak Sesuai
# Tipe kepribadian dominan ditentukan dari total skor tertinggi tiap kategori (RIASEC).

import streamlit as st

# -------------------- DAFTAR SOAL --------------------
soal_list = [
    # ---------------- REALISTIC ----------------
    {"no": 1, "soal": "Saya suka bekerja dengan alat, mesin, atau kendaraan.", "tipe": "Realistic"},
    {"no": 2, "soal": "Saya lebih suka aktivitas di lapangan daripada di kantor.", "tipe": "Realistic"},
    {"no": 3, "soal": "Saya menikmati memperbaiki peralatan atau mesin yang rusak.", "tipe": "Realistic"},
    {"no": 4, "soal": "Saya suka pekerjaan yang melibatkan keterampilan tangan dan fisik.", "tipe": "Realistic"},
    {"no": 5, "soal": "Saya lebih suka instruksi yang jelas dan hasil kerja yang nyata.", "tipe": "Realistic"},
    {"no": 6, "soal": "Saya nyaman bekerja di luar ruangan atau lingkungan pabrik.", "tipe": "Realistic"},
    {"no": 7, "soal": "Saya suka melihat hasil kerja saya secara langsung dan konkret.", "tipe": "Realistic"},
    {"no": 8, "soal": "Saya menikmati tugas yang membutuhkan kekuatan dan ketepatan.", "tipe": "Realistic"},

    # ---------------- INVESTIGATIVE ----------------
    {"no": 9, "soal": "Saya senang menganalisis masalah dan mencari penyebabnya.", "tipe": "Investigative"},
    {"no": 10, "soal": "Saya suka melakukan penelitian untuk menemukan jawaban baru.", "tipe": "Investigative"},
    {"no": 11, "soal": "Saya menikmati memecahkan teka-teki logika atau angka.", "tipe": "Investigative"},
    {"no": 12, "soal": "Saya lebih suka berpikir kritis daripada mengikuti instruksi tanpa alasan.", "tipe": "Investigative"},
    {"no": 13, "soal": "Saya suka memahami bagaimana sesuatu bekerja secara detail.", "tipe": "Investigative"},
    {"no": 14, "soal": "Saya tertarik membaca buku atau artikel ilmiah.", "tipe": "Investigative"},
    {"no": 15, "soal": "Saya senang menguji ide atau hipotesis baru.", "tipe": "Investigative"},
    {"no": 16, "soal": "Saya suka membuat kesimpulan berdasarkan data yang saya temukan.", "tipe": "Investigative"},

    # ---------------- ARTISTIC ----------------
    {"no": 17, "soal": "Saya suka mengekspresikan diri melalui seni, tulisan, atau musik.", "tipe": "Artistic"},
    {"no": 18, "soal": "Saya menikmati bekerja di lingkungan yang bebas dan tidak kaku.", "tipe": "Artistic"},
    {"no": 19, "soal": "Saya suka menciptakan ide atau konsep baru yang unik.", "tipe": "Artistic"},
    {"no": 20, "soal": "Saya memiliki imajinasi yang kuat dalam memecahkan masalah.", "tipe": "Artistic"},
    {"no": 21, "soal": "Saya senang mendesain sesuatu agar tampak menarik.", "tipe": "Artistic"},
    {"no": 22, "soal": "Saya tidak terlalu suka pekerjaan yang terlalu teratur dan monoton.", "tipe": "Artistic"},
    {"no": 23, "soal": "Saya suka pekerjaan yang memberi kebebasan untuk berinovasi.", "tipe": "Artistic"},
    {"no": 24, "soal": "Saya tertarik pada bidang seni, desain, atau komunikasi visual.", "tipe": "Artistic"},

    # ---------------- SOCIAL ----------------
    {"no": 25, "soal": "Saya suka membantu orang lain menyelesaikan masalah mereka.", "tipe": "Social"},
    {"no": 26, "soal": "Saya merasa senang jika bisa mengajar atau membimbing orang lain.", "tipe": "Social"},
    {"no": 27, "soal": "Saya mudah berempati terhadap perasaan orang lain.", "tipe": "Social"},
    {"no": 28, "soal": "Saya suka bekerja sama dalam tim.", "tipe": "Social"},
    {"no": 29, "soal": "Saya senang berkomunikasi dan menjalin hubungan sosial.", "tipe": "Social"},
    {"no": 30, "soal": "Saya lebih suka pekerjaan yang melibatkan interaksi dengan manusia.", "tipe": "Social"},
    {"no": 31, "soal": "Saya merasa puas ketika bisa memberikan dampak positif bagi orang lain.", "tipe": "Social"},
    {"no": 32, "soal": "Saya mudah beradaptasi dengan berbagai karakter orang.", "tipe": "Social"},

    # ---------------- ENTERPRISING ----------------
    {"no": 33, "soal": "Saya suka memimpin orang lain dan mengambil tanggung jawab besar.", "tipe": "Enterprising"},
    {"no": 34, "soal": "Saya senang meyakinkan orang lain untuk menerima ide saya.", "tipe": "Enterprising"},
    {"no": 35, "soal": "Saya menikmati situasi kompetitif dan menantang.", "tipe": "Enterprising"},
    {"no": 36, "soal": "Saya percaya diri dalam mengambil keputusan penting.", "tipe": "Enterprising"},
    {"no": 37, "soal": "Saya suka mencari peluang baru dan membuat strategi sukses.", "tipe": "Enterprising"},
    {"no": 38, "soal": "Saya menikmati kegiatan yang berhubungan dengan penjualan atau promosi.", "tipe": "Enterprising"},
    {"no": 39, "soal": "Saya suka berbicara di depan umum dan mempengaruhi orang lain.", "tipe": "Enterprising"},
    {"no": 40, "soal": "Saya tertarik dengan posisi kepemimpinan atau manajemen.", "tipe": "Enterprising"},

    # ---------------- CONVENTIONAL ----------------
    {"no": 41, "soal": "Saya suka pekerjaan yang memiliki aturan dan prosedur yang jelas.", "tipe": "Conventional"},
    {"no": 42, "soal": "Saya menikmati menyusun data atau dokumen agar rapi dan teratur.", "tipe": "Conventional"},
    {"no": 43, "soal": "Saya lebih suka bekerja dengan angka, catatan, atau file.", "tipe": "Conventional"},
    {"no": 44, "soal": "Saya nyaman dengan pekerjaan administratif atau akuntansi.", "tipe": "Conventional"},
    {"no": 45, "soal": "Saya suka mengikuti instruksi dan menyelesaikan tugas sesuai prosedur.", "tipe": "Conventional"},
    {"no": 46, "soal": "Saya memperhatikan detail kecil agar pekerjaan tidak salah.", "tipe": "Conventional"},
    {"no": 47, "soal": "Saya kurang nyaman dengan lingkungan kerja yang tidak teratur.", "tipe": "Conventional"},
    {"no": 48, "soal": "Saya menikmati mengorganisir data dan mengatur sistem kerja.", "tipe": "Conventional"},
    {"no": 49, "soal": "Saya cenderung menyukai jadwal kerja yang tetap dan terencana.", "tipe": "Conventional"},
    {"no": 50, "soal": "Saya merasa puas jika pekerjaan selesai dengan rapi dan akurat.", "tipe": "Conventional"},
]


# -------------------- FUNGSI UNTUK TAMPILKAN DI STREAMLIT --------------------
def tampilkan_tes_riasec():
    st.title("🧠 Tes Kepribadian RIASEC (Holland Model)")
    st.markdown("""
    Silakan pilih tingkat kesesuaian Anda terhadap setiap pernyataan berikut:

    - 4️⃣ **Sangat Sesuai**  
    - 3️⃣ **Cukup Sesuai**  
    - 2️⃣ **Sedikit Sesuai**  
    - 1️⃣ **Tidak Sesuai**

    Tidak ada jawaban benar atau salah — pilih yang paling menggambarkan diri Anda.
    """)

    jawaban = {}

    with st.form("riasec_form"):
        for s in soal_list:
            jawaban[s["no"]] = st.radio(
                f"{s['no']}. {s['soal']}",
                options=[4, 3, 2, 1],
                format_func=lambda x: {
                    4: "Sangat Sesuai",
                    3: "Cukup Sesuai",
                    2: "Sedikit Sesuai",
                    1: "Tidak Sesuai",
                }[x],
                horizontal=True,
                key=f"soal_{s['no']}"
            )

        submitted = st.form_submit_button("✅ Selesai & Lihat Hasil")

    if submitted:
        import pandas as pd, os
        df = pd.DataFrame(soal_list)
        df["Skor"] = df["no"].map(jawaban)
        hasil = df.groupby("tipe")["Skor"].sum().to_dict()
        tipe_dominan = max(hasil, key=hasil.get)

        st.success(f"Tipe kepribadian dominan kamu adalah **{tipe_dominan}** 🎯")
        st.write("### Skor tiap kategori:")
        st.json(hasil)

        os.makedirs("data", exist_ok=True)
        df.to_csv("data/hasil_tes_riasec.csv", index=False)
        st.info("📂 Hasil tersimpan ke data/hasil_tes_riasec.csv")

# Jalankan langsung jika file ini dipanggil
if __name__ == "__main__":
    tampilkan_tes_riasec()
