import sqlite3
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "data", "psikotes.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS hasil_peserta (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT,
        job_title TEXT,
        subtes TEXT,
        skor INTEGER,
        keterangan TEXT,
        tanggal_tes TEXT
    )
    """)
    conn.commit()
    conn.close()

def insert_hasil(nama, job_title, subtes, skor, keterangan, tanggal):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    INSERT INTO hasil_peserta (nama, job_title, subtes, skor, keterangan, tanggal_tes)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (nama, job_title, subtes, skor, keterangan, tanggal))
    conn.commit()
    conn.close()

def get_all_hasil():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM hasil_peserta", conn)
    conn.close()
    return df
