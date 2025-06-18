import streamlit as st
from pathlib import Path
import os
import base64
from dotenv import load_dotenv
load_dotenv(override=True)

LOCAL_FOLDER_PATH = os.getenv("LOCAL_FOLDER_PATH")

def listSubFolder():
    base_path = Path(LOCAL_FOLDER_PATH)
    # List all subdirectories
    folders = [f.name for f in base_path.iterdir() if f.is_dir()]
    return base_path,folders

def embed_pdf(file_path: Path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
    pdf_display = f"""
        <iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>
    """
    st.markdown(pdf_display, unsafe_allow_html=True)

st.markdown("""
    <style>
    /* Greife auf Tab-Container zu und erlaube horizontales Scrollen */
    .stTabs [data-baseweb="tab-list"] {
        overflow-x: auto;
        white-space: nowrap;
        scrollbar-width: thin;
    }
    .stTabs [data-baseweb="tab"] {
        min-width: max-content;
    }
    </style>
""", unsafe_allow_html=True)

base_path, folders = listSubFolder()
if folders:
    tabs = st.tabs(folders)
    selected_pdf = None
    for i, folder_name in enumerate(folders):
        with tabs[i]:
            st.subheader(f"Saved PDF in folder {folder_name}")
            
            folder_path = base_path / folder_name
            files = [f.name for f in folder_path.iterdir() if f.is_file()]
            selected_pdf = st.selectbox("", files,key=f"pdf_select_{folder_name}")
            file_path = folder_path / selected_pdf
            embed_pdf(file_path)
        
    
    









