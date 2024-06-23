HELLO WHAT'S UP!!
MY NAME IS MUHAMMAD RAFI RIZANDA(2115061098) AND ANISSA ZHAFIRAH FROM UNIVERSITAS LAMPUNG, INFORMATICS ENGINEERING MAJOR 6TH SEMESTER. 
THIS IS MY PORTFOLIO PROJECT FOR SUBJECT NATURAL LANGUAGE PROCESSING

Here's the list of the project and what inside them:
1. App.py
   Project that we build from the tutorial youtube videos (https://www.youtube.com/playlist?list=PLZLuc8eJafeEuR-7X5pb6xgGOPosuVty0).
   The Project was about AI Resume Analyzer, The creation of the AI ​​Resume Analyzer is explained in a video series on YouTube consisting of several main steps.
   First, the application was built using Python by utilizing the Streamlit library for the user interface. Resume data is uploaded and processed to extract
   information using an NLP model such as spaCy. Then, the extracted information is compared with relevant job descriptions to assess fit. The results of the
   analysis are displayed back to the user with suggestions for improvements to improve the quality of the resume. This video includes a detailed walkthrough from
   setting up the development environment to deployment and final evaluation of the application.
   
3. Courses.py
   Kode di atas adalah sebuah daftar kursus online yang dikategorikan berdasarkan berbagai topik seperti ilmu data, pengembangan web, pengembangan aplikasi
   Android,     pengembangan aplikasi iOS, dan desain UI/UX. Setiap kategori memiliki beberapa kursus yang tercantum dengan nama kursus dan tautan ke kursus
   tersebut. Selain itu,    terdapat juga dua daftar video yang berisi tautan video tentang cara membuat resume dan mempersiapkan wawancara. Fungsi dari kode ini
   adalah untuk menyediakan referensi yang terorganisir dan mudah diakses bagi individu yang mencari kursus dan video edukatif dalam bidang-bidang tersebut,
   sehingga memudahkan mereka dalam memilih dan mengakses materi yang relevan untuk pengembangan keterampilan dan karier mereka.


**Project deeplearning.py**
   
Penjelasan Umum : Penelitian ini bertujuan untuk mengimplementasikan Natural Language Processing (NLP) dalam sebuah website yang dapat membuat resume AI dari
bagian abstrak jurnal skripsi. Website ini akan dikembangkan menggunakan bahasa pemrograman Python dan menggunakan SQLWorkbench untuk penyimpanan data. Model
NLP yang diimplementasikan dirancang untuk mengekstraksi informasi penting seperti rating dan score akumulasi abstrak jurnal tersebut, nama penulis oleh, judul
abstrak, hasil/isi, keyword, fakultas, dan rekomendasi topic dari abstrak jurnal yang diunggah dalam format PDF. Pengguna hanya perlu mengunggah file PDF
abstrak jurnal, dan sistem akan secara otomatis mendeteksi serta menghasilkan resume yang disajikan dalam beberapa poin utama.

Daftar Pustaka Python :
Tentu, berikut adalah penjelasan singkat untuk setiap pustaka:

1. **Scikit-learn (Sklearn)**:
   - **Penjelasan**: Pustaka machine learning untuk Python.
   - **Fungsi**: Algoritma machine learning, evaluasi model, preprocessing data.

2. **spaCy**:
   - **Penjelasan**: Pustaka NLP yang cepat dan canggih.
   - **Fungsi**: Pemrosesan teks, ekstraksi informasi, NLP.

3. **RE (Regular Expression)**:
   - **Penjelasan**: Modul untuk ekspresi reguler di Python.
   - **Fungsi**: Pencocokan dan manipulasi teks.

4. **fitz (PyMuPDF)**:
   - **Penjelasan**: Pustaka untuk bekerja dengan PDF.
   - **Fungsi**: Membaca, memanipulasi, dan menganalisis dokumen PDF.

5. **pdfminer3**:
   - **Penjelasan**: Pustaka untuk ekstraksi teks dari PDF.
   - **Fungsi**: Ekstraksi teks dan metadata dari file PDF.

6. **pymysql**:
   - **Penjelasan**: Pustaka untuk koneksi ke database MySQL dari Python.
   - **Fungsi**: Menjalankan kueri SQL, manajemen database.

7. **streamlit**:
   - **Penjelasan**: Framework untuk membangun aplikasi web interaktif dengan Python.
   - **Fungsi**: Membuat dashboard dan aplikasi data.

8. **pandas**:
   - **Penjelasan**: Pustaka untuk manipulasi dan analisis data.
   - **Fungsi**: DataFrame, pembersihan data, analisis data.

9. **TF-IDF (Term Frequency-Inverse Document Frequency)**:
   - **Penjelasan**: Teknik statistik untuk mengevaluasi pentingnya kata dalam dokumen.
   - **Fungsi**: Pemeringkatan relevansi kata dalam teks untuk pencarian informasi.
  
**Alur Kode NLP** : Untuk memproses data dari file PDF, langkah pertama adalah pra-pemrosesan teks. Proses ini dimulai dengan ekstraksi teks menggunakan pustaka seperti PyMuPDF, pdfminer, atau PyPDF2. Setelah teks diekstrak, karakter spesial seperti tanda baca dan simbol yang tidak relevan dihapus, dan semua huruf diubah menjadi huruf kecil untuk konsistensi. Selanjutnya, teks dipecah menjadi unit-unit kata yang lebih kecil melalui proses tokenisasi. Setelah pra-pemrosesan, kata kunci dikenali dengan metode statistik seperti Term Frequency (TF), yang menghitung frekuensi kemunculan setiap kata, dan Inverse Document Frequency (IDF), yang menentukan seberapa umum atau jarang sebuah kata muncul di sejumlah dokumen. Kombinasi TF dan IDF menghasilkan TF-IDF, yang membantu menemukan kata-kata signifikan yang sering muncul di dokumen tertentu tetapi jarang di dokumen lain. Akhirnya, dari daftar kata yang telah diidentifikasi, kata kunci yang paling relevan dipilih berdasarkan kriteria seperti frekuensi kemunculan. 

**FILE PPT PROJECT**
https://bit.ly/PPT_NLP_Project
**FILE JURNAL NLP**
https://bit.ly/Jurnal_NLP_Project

Referensi Jurnal
[1] Andika, R., & Setiawan, E. (2021). Implementasi Named Entity Recognition untuk 
Ekstraksi Informasi pada Artikel Ilmiah Berbahasa Indonesia. Jurnal Ilmu Komputer dan 
Informasi, 14(2), 67-75. https://doi.org/10.21609/jiki.v14i2.945
[2] Bird, S., Klein, E., & Loper, E. (2009). Natural Language Processing with Python: 
Analyzing Text with the Natural Language Toolkit. O'Reilly Media.
[3] Fauzi, A., & Wijayanto, H. (2020). Penggunaan Metode TF-IDF dan K-Means untuk 
Klasifikasi Dokumen Abstrak Jurnal. Jurnal Pengembangan Teknologi Informasi dan Ilmu 
Komputer, 4(6), 212-219. https://doi.org/10.25126/jptiik.46221
[4] Hartono, Y., & Sutrisno, E. (2019). Penerapan Natural Language Processing untuk 
Pembuatan Ringkasan Otomatis Artikel Ilmiah. Jurnal Teknologi Informasi dan Komunikasi, 
8(3), 145-153. https://doi.org/10.25126/jtik.83145
[5] Puspitasari, D., & Ramadhani, F. (2020). Analisis Sentimen pada Abstrak Jurnal 
Menggunakan Metode Naive Bayes dan NLP. Jurnal Sistem Informasi, 16(1), 33-40. 
https://doi.org/10.21609/jsi.v16i1.903
[6] Rahayu, T., & Syafitri, W. (2019). Implementasi Algoritma Support Vector Machine dan 
Natural Language Processing untuk Klasifikasi Teks Abstrak Jurnal. Jurnal Teknologi 
Informasi,5(2), 22-28. https://doi.org/10.32493/jti.v5i2.324
[7] Santoso, B., & Pratama, Y. (2021). Penggunaan Natural Language Processing dan Algoritma 
Clustering untuk Ekstraksi Informasi pada Abstrak Jurnal. Jurnal Ilmiah Teknik Informatika 
Komputer dan Sistem Informasi, 7(4), 198-205. https://doi.org/10.35671/jitiks.v7i4.787
