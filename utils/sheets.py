import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import streamlit as st

SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
SPREADSHEET_ID = "1DCVAJHPbbyn06c4TNijqn-RT1A0DMsv0R_PIdQToycE"

def _get_client():
    creds_info = st.secrets["gcp_service_account"]
    creds = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
    return gspread.authorize(creds)

def append_result(nama, job_title, subtes, skor, keterangan, tanggal):
    client = _get_client()
    sheet = client.open_by_key(SPREADSHEET_ID).sheet1
    sheet.append_row([nama, job_title, subtes, skor, keterangan, tanggal],
                     value_input_option="USER_ENTERED")

def read_all_results():
    client = _get_client()
    sheet = client.open_by_key(SPREADSHEET_ID).sheet1
    rows = sheet.get_all_records()
    return pd.DataFrame(rows)
