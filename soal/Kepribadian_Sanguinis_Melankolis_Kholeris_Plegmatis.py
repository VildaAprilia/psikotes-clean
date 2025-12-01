# ============================================
# SOAL SUB TES: KEPRIBADIAN
# (Sanguinis, Melankolis, Kholeris, Plegmatis)
# ============================================

import streamlit as st

soal_list = [
    # ------------------- SANGUINIS -------------------
    {"no": 1, "soal": "Saya mudah bergaul dan senang menjadi pusat perhatian.", "kepribadian": "Sanguinis"},
    {"no": 2, "soal": "Saya sering merasa bersemangat dan optimis dalam segala situasi.", "kepribadian": "Sanguinis"},
    {"no": 3, "soal": "Saya suka berbicara dan bercerita kepada orang lain.", "kepribadian": "Sanguinis"},
    {"no": 4, "soal": "Saya mudah menyesuaikan diri dalam kelompok baru.", "kepribadian": "Sanguinis"},
    {"no": 5, "soal": "Saya sering membuat suasana menjadi lebih ceria.", "kepribadian": "Sanguinis"},
    {"no": 6, "soal": "Saya mudah bersemangat tetapi juga mudah bosan.", "kepribadian": "Sanguinis"},
    {"no": 7, "soal": "Saya suka berbagi ide dan cerita tanpa terlalu memikirkan detail.", "kepribadian": "Sanguinis"},
    {"no": 8, "soal": "Saya cenderung spontan dan ekspresif dalam bertindak.", "kepribadian": "Sanguinis"},

    # ------------------- MELANKOLIS -------------------
    {"no": 9, "soal": "Saya suka merencanakan sesuatu dengan detail dan teliti.", "kepribadian": "Melankolis"},
    {"no": 10, "soal": "Saya berusaha melakukan segala hal dengan sempurna.", "kepribadian": "Melankolis"},
    {"no": 11, "soal": "Saya cenderung berhati-hati dalam mengambil keputusan.", "kepribadian": "Melankolis"},
    {"no": 12, "soal": "Saya merasa terganggu jika pekerjaan dilakukan asal-asalan.", "kepribadian": "Melankolis"},
    {"no": 13, "soal": "Saya lebih suka bekerja sendirian agar hasilnya rapi dan sesuai rencana.", "kepribadian": "Melankolis"},
    {"no": 14, "soal": "Saya sering memikirkan kemungkinan terburuk sebelum bertindak.", "kepribadian": "Melankolis"},
    {"no": 15, "soal": "Saya sulit merasa puas terhadap hasil kerja sendiri.", "kepribadian": "Melankolis"},
    {"no": 16, "soal": "Saya sangat memperhatikan detail kecil dalam pekerjaan.", "kepribadian": "Melankolis"},

    # ------------------- KHOLERIS -------------------
    {"no": 17, "soal": "Saya suka memimpin dan mengarahkan orang lain.", "kepribadian": "Kholeris"},
    {"no": 18, "soal": "Saya cepat mengambil keputusan dan bertindak tegas.", "kepribadian": "Kholeris"},
    {"no": 19, "soal": "Saya termotivasi oleh tantangan dan target tinggi.", "kepribadian": "Kholeris"},
    {"no": 20, "soal": "Saya tidak mudah dipengaruhi oleh orang lain.", "kepribadian": "Kholeris"},
    {"no": 21, "soal": "Saya suka menjadi orang yang bertanggung jawab atas hasil akhir.", "kepribadian": "Kholeris"},
    {"no": 22, "soal": "Saya sering memotivasi orang lain untuk bekerja lebih keras.", "kepribadian": "Kholeris"},
    {"no": 23, "soal": "Saya tidak takut menghadapi konflik demi tujuan yang jelas.", "kepribadian": "Kholeris"},
    {"no": 24, "soal": "Saya lebih fokus pada hasil dibandingkan proses.", "kepribadian": "Kholeris"},

    # ------------------- PLEGMATIS -------------------
    {"no": 25, "soal": "Saya cenderung tenang dan tidak mudah tersulut emosi.", "kepribadian": "Plegmatis"},
    {"no": 26, "soal": "Saya lebih memilih menghindari konflik dengan orang lain.", "kepribadian": "Plegmatis"},
    {"no": 27, "soal": "Saya bisa bekerja dengan sabar meskipun dalam situasi sulit.", "kepribadian": "Plegmatis"},
    {"no": 28, "soal": "Saya tidak suka terburu-buru dalam mengambil keputusan.", "kepribadian": "Plegmatis"},
    {"no": 29, "soal": "Saya merasa nyaman dengan rutinitas yang stabil.", "kepribadian": "Plegmatis"},
    {"no": 30, "soal": "Saya lebih memilih mendengarkan daripada berbicara.", "kepribadian": "Plegmatis"},
    {"no": 31, "soal": "Saya mudah menyesuaikan diri tanpa menimbulkan masalah.", "kepribadian": "Plegmatis"},
    {"no": 32, "soal": "Saya berusaha menjaga kedamaian dalam hubungan sosial.", "kepribadian": "Plegmatis"},
]

# -------------------- FUNGSI UNTUK STREAMLIT --------------------
def tampilkan_tes_kepribadian():
    st.title("🧩 Tes Kepribadian (Sanguinis, Melankolis, Kholeris, Plegmatis)")
    st.markdown("""
    Silakan isi berdasarkan kesesuaian dengan diri Anda:

    - 4️⃣ **Sangat Sesuai**  
    - 3️⃣ **Cukup Sesuai**  
    - 2️⃣ **Sedikit Sesuai**  
    - 1️⃣ **Tidak Sesuai**
    """)

    jawaban = {}

    with st.form("kepribadian_form"):
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

        submitted = st.form_submit_button("✅ Selesai & Simpan Hasil")

    if submitted:
        import pandas as pd, os
        df = pd.DataFrame(soal_list)
        df["Skor"] = df["no"].map(jawaban)
        hasil = df.groupby("kepribadian")["Skor"].sum().to_dict()
        tipe_dominan = max(hasil, key=hasil.get)

        st.success(f"Tipe kepribadian dominan kamu adalah **{tipe_dominan}** 🎯")
        st.write("### Skor Tiap Tipe:")
        st.json(hasil)

        os.makedirs("data", exist_ok=True)
        df.to_csv("data/hasil_tes_kepribadian.csv", index=False)
        st.info("📂 Hasil tersimpan ke data/hasil_tes_kepribadian.csv")

# Jalankan langsung jika file dipanggil
if __name__ == "__main__":
    tampilkan_tes_kepribadian()
