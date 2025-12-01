# utils/scoring.py
import pandas as pd

def hitung_skor(jawaban_user, kunci_jawaban, poin_benar=4):
    """
    Menghitung total skor dari jawaban peserta.
    jawaban_user dan kunci_jawaban berbentuk list (panjang sama).
    """
    benar = sum([1 for j, k in zip(jawaban_user, kunci_jawaban) if j == k])
    total_skor = benar * poin_benar
    return total_skor


def simpan_hasil(nama, job_title, tes, skor, file_path="data/hasil_peserta.csv"):
    """
    Menyimpan hasil tes peserta ke file CSV.
    """
    df_baru = pd.DataFrame([{
        "Nama": nama,
        "Job Title": job_title,
        "Tes": tes,
        "Skor": skor
    }])

    try:
        df_lama = pd.read_csv(file_path)
        df = pd.concat([df_lama, df_baru], ignore_index=True)
    except FileNotFoundError:
        df = df_baru

    df.to_csv(file_path, index=False)
    return df
