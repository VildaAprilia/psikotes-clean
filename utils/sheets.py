import gspread
from google.oauth2.service_account import Credentials
import streamlit as st
import pandas as pd

# ================== KONFIG ==================
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

SPREADSHEET_ID = "1DCVAJHPbbyn06c4TNijqn-RT1A0DMsv0R_PIdQToycE"

# ================== CLIENT ==================
@st.cache_resource
def _get_client():
    creds_info = st.secrets["gcp_service_account"]
    creds = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
    return gspread.authorize(creds)

@st.cache_resource
def _get_sheet():
    client = _get_client()
    return client.open_by_key(SPREADSHEET_ID).sheet1

# ================== APPEND (DIPAKAI TES) ==================
def append_result(subtes, skor, keterangan):
    sheet = _get_sheet()
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

# ================== READ (DIPAKAI ADMIN) ==================
def read_all_results():
    sheet = _get_sheet()
    data = sheet.get_all_records()

    if not data:
        return pd.DataFrame()

    return pd.DataFrame(data)
