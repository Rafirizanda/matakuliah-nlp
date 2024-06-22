import streamlit as st
import pandas as pd
import base64
import random
import time
import datetime
import io
import os
import fitz  # PyMuPDF
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
from streamlit_tags import st_tags
from PIL import Image
import pymysql
import spacy
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter

# Load Spacy model
nlp = spacy.load('en_core_web_sm')

# Helper function to fetch YouTube video link
def fetch_yt_video(link):
    return link

# Helper function to create download link for data
def get_table_download_link(df, filename, text):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href

# Helper function to read PDF
def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()
    converter.close()
    fake_file_handle.close()
    return text

# Helper function to display PDF in Streamlit
def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# Helper function to extract keywords using TF-IDF
def extract_keywords_tfidf(text, num_keywords=20):
    # Preprocess text
    doc = nlp(text.lower())
    tokens = [token.text for token in doc if token.is_alpha and not token.is_stop]
    joined_tokens = ' '.join(tokens)
    
    # Apply TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([joined_tokens])
    feature_names = vectorizer.get_feature_names_out()
    tfidf_scores = tfidf_matrix.toarray()[0]
    
    # Get top keywords
    keywords_scores = list(zip(feature_names, tfidf_scores))
    sorted_keywords_scores = sorted(keywords_scores, key=lambda x: x[1], reverse=True)
    top_keywords = [keyword for keyword, score in sorted_keywords_scores[:num_keywords]]
    
    return top_keywords

# Connect to MySQL database
def init_connection():
    return pymysql.connect(host='localhost',
                           user='root',
                           password='rafi157287',
                           db='skripsi_db')

# Fetch data from the database
def fetch_data(query):
    conn = init_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Insert data into the database
def insert_data(data):
    conn = init_connection()
    with conn.cursor() as cursor:
        query = """
        INSERT INTO skripsi_data (nama_mahasiswa, judul_skripsi, abstract_score, timestamp, jumlah_halaman, fakultas, rekomendasi_video, rekomendasi_topik)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, data)
        conn.commit()
    conn.close()

# Main function
def main():
    st.title("Skripsi Abstract Analyzer")
    menu = ["User", "Admin"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "User":
        st.subheader("Upload Abstrak Skripsi")
        pdf_file = st.file_uploader("Upload PDF", type=["pdf"])

        if pdf_file is not None:
            file_path = os.path.join("Uploaded_Abstracts", pdf_file.name)
            with open(file_path, "wb") as f:
                f.write(pdf_file.getbuffer())

            show_pdf(file_path)

            raw_text = pdf_reader(file_path)
            st.write(raw_text)

            keywords = extract_keywords_tfidf(raw_text)
            st.write("Keywords: ", keywords)

            nama_mahasiswa = st.text_input("Nama Mahasiswa")
            judul_skripsi = st.text_input("Judul Skripsi")
            abstract_score = random.randint(50, 100)  # Dummy abstract score
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            jumlah_halaman = len(fitz.open(file_path))
            fakultas = st.selectbox("Fakultas", ["Fakultas Teknik", "FEB", "FISIP", "Fakultas Hukum", "Fakultas Keguruan dan Ilmu Pendidikan"])
            rekomendasi_video = fetch_yt_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")  # Dummy video link
            rekomendasi_topik = st_tags(label='Rekomendasi Topik', text='Press enter to add more', value=keywords, suggestions=["AI", "ML", "NLP", "Computer Vision", "Data Science"])

            if st.button("Simpan Data"):
                data = (nama_mahasiswa, judul_skripsi, abstract_score, timestamp, jumlah_halaman, fakultas, rekomendasi_video, ','.join(rekomendasi_topik))
                insert_data(data)
                st.success("Data berhasil disimpan")

    elif choice == "Admin":
        st.subheader("Admin Dashboard")
        query = "SELECT * FROM skripsi_data"
        try:
            df = fetch_data(query)
            st.dataframe(df)

            if st.button("Download Data"):
                st.markdown(get_table_download_link(df, "data_skripsi.csv", "Klik di sini untuk mengunduh data"), unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error fetching data: {e}")

if __name__ == '__main__':
    main()
