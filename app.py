import streamlit as st
import pandas as pd
from docx import Document
import os

@st.cache_data
def load_index():
    return pd.read_csv("index.csv")

df = load_index()

st.title("📁 Question File Selector & Combiner")

code = st.text_input("Enter file code")
if 'selected_files' not in st.session_state:
    st.session_state.selected_files = []

if st.button("Add"):
    match = df[df['code'] == code.strip()]
    if not match.empty:
        file_info = match.iloc[0].to_dict()
        if file_info not in st.session_state.selected_files:
            st.session_state.selected_files.append(file_info)
    else:
        st.warning("Code not found in index.")

st.write("### ✅ Selected Files")
for i, item in enumerate(st.session_state.selected_files):
    col1, col2 = st.columns([4, 1])
    col1.write(f"{item['filename']}")
    if col2.button("❌ Remove", key=f"remove_{i}"):
        st.session_state.selected_files.pop(i)
        st.experimental_rerun()

if st.button("Generate") and st.session_state.selected_files:
    output_doc = Document()
    for item in st.session_state.selected_files:
        path = item['filepath']
        if os.path.exists(path):
            if path.endswith(".docx"):
                sub_doc = Document(path)
                for para in sub_doc.paragraphs:
                    output_doc.add_paragraph(para.text)
            elif path.endswith(".txt"):
                with open(path, 'r', encoding='utf-8') as f:
                    output_doc.add_paragraph(f.read())
        else:
            st.error(f"File not found: {path}")

    save_path = "combined_output.docx"
    output_doc.save(save_path)
    st.success(f"✔️ Document generated: {save_path}")
    with open(save_path, "rb") as f:
        st.download_button("📥 Download Combined DOCX", f, file_name="combined_output.docx")

