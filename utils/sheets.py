import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import streamlit as st

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

SPREADSHEET_ID = "1DCVAJHPbbyn06c4TNijqn-RT1A0DMsv0R_PIdQToycE"

def _get_client():
    creds_info = st.secrets["gcp_service_account"]
    creds = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
    return gspread.authorize(creds)

# ================== SIMPAN HASIL TES ==================
def append_result(subtes, skor, keterangan):
    client = _get_client()
    sheet = client.open_by_key(SPREADSHEET_ID).sheet1

    biodata = st.session_state.get("biodata", {})

    sheet.append_row([
        biodata.get("Nama", ""),
        biodata.get("No HP", ""),
        biodata.get("Job Title", ""),
        biodata.get("Tempat Pendaftaran", ""),
        subtes,
        skor,
        keterangan,
        biodata.get("Tanggal Submit", "")
    ], value_input_option="USER_ENTERED")

# ================== READ ==================
def read_all_results():
    client = _get_client()
    sheet = client.open_by_key(SPREADSHEET_ID).sheet1
    rows = sheet.get_all_records()
    return pd.DataFrame(rows)