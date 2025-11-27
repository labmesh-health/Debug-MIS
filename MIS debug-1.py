import streamlit as st
import pandas as pd
import pdfplumber
import re
from datetime import datetime
from io import BytesIO

st.set_page_config(page_title="LAB MIS Full Debug", layout="wide")
st.title("LAB MIS – Full Counter Parsing Debug")

# ---------- helpers ----------
def extract_date_from_text(text: str):
    for line in text.split("\n")[:6]:
        match = re.search(r"(\d{2}/\d{2}/\d{4})\s+(\d{2}:\d{2})", line)
        if match:
            date_str, time_str = match.groups()
            try:
                return datetime.strptime(f"{date_str} {time_str}", "%d/%m/%Y %H:%M")
            except Exception:
                continue
    return None

# ---------- TEST COUNTER (page 1 etc.) ----------
def parse_test_counter(pdf_bytes: bytes) -> pd.DataFrame:
    header_line = "Test ACN Routine Rerun STAT Calib. QC Total Count"
    rows = []

    with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            date = extract_date_from_text(text)
            lines = text.split("\n")

            for i, line in enumerate(lines):
                if line.strip() == header_line:
                    for data_line in lines[i + 1:]:
                        dl = data_line.strip()
                        if not dl or dl.lower().startswith(("total", "unit:", "system:")):
                            break
                        parts = re.split(r"\s+", dl)
                        if len(parts) < 8:
                            continue
                        test_name = parts[0]
                        acn = parts[1]
                        routine = parts[2]
                        rerun = parts[3]
                        stat = parts[4]
                        calib = parts[5]
                        qc = parts[6]
                        total = parts[7]
                        rows.append({
                            "Test": test_name,
                            "ACN": acn,
                            "Routine": routine,
                            "Rerun": rerun,
                            "STAT": stat,
                            "Calibrator": calib,
                            "QC": qc,
                            "Total Count": total,
                            "Date": date,
                        })

    df = pd.DataFrame(rows)
    if not df.empty:
        for col in ["Routine", "Rerun", "STAT", "Calibrator", "QC", "Total Count"]:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
        df["Date"] = pd.to_datetime(df["Date"])
    return df

# ---------- SAMPLE COUNTER (page 5) ----------
def parse_sample_counter(pdf_bytes: bytes) -> pd.DataFrame:
    header_line = "Unit: Routine Rerun STAT Total Count"
    headers = ["Unit", "Routine", "Rerun", "STAT", "Total Count"]
    rows = []

    with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            date = extract_date_from_text(text)
            lines = text.split("\n")

            for i, line in enumerate(lines):
                if line.strip() == header_line:
                    for dl in lines[i + 1:]:
                        dl = dl.strip()
                        if (not dl or
                            dl.lower().startswith(("total count", "measuring cells counter",
                                                   "system:", "unit:"))):
                            break
                        parts = re.split(r"\s+", dl)
                        if len(parts) < 5:
                            continue
                        unit = parts[0]
                        routine = parts[1]
                        rerun = parts[2]
                        stat = parts[3]
                        total = parts[4]
                        rows.append({
                            "Unit": unit,
                            "Routine": routine,
                            "Rerun": rerun,
                            "STAT": stat,
                            "Total Count": total,
                            "Date": date,
                        })

    df = pd.DataFrame(rows)
    if not df.empty
