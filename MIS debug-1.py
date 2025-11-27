import streamlit as st
import pdfplumber
from io import BytesIO

st.set_page_config(page_title="LAB MIS RAW DEBUG", layout="wide")
st.title("LAB MIS – RAW PDF DEBUG")

uploaded_file = st.file_uploader("Upload Detailed Test Counter PDF", type=["pdf"])

if uploaded_file:
    pdf_bytes = uploaded_file.read()

    with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
        for page_idx, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            lines = text.split("\n")
            st.subheader(f"Page {page_idx+1} – first 80 lines")
            st.write(lines[:80])
else:
    st.info("Upload the Detailed Test Counter PDF.")
