import os
import openai
import streamlit as st
import docx  # Digunakan untuk memproses file DOCX
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv() # memuat variabel dari .env

# Konfigurasi API Key dan Endpoint dari Azure OpenAI
openai.api_type = "azure"
openai.api_key = os.getenv("AZURE_OPENAI_KEY")
openai.api_base = "https://openai-coba.openai.azure.com"  # Ganti dengan endpoint Azure Anda
openai.api_version = "2023-05-15"  # Sesuaikan versi API jika perlu

# Fungsi untuk mengekstrak teks dari file DOCX
def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

# Menyiapkan dokumen DOCX yang berisi informasi gizi
docx_file_path = "data/referensi/data1.docx"  # Ganti dengan path file DOCX Anda
documents = extract_text_from_docx(docx_file_path).split('\n')

# Fungsi untuk mencari informasi relevan menggunakan pencarian berbasis TF-IDF
def retrieve_relevant_documents(query, documents):
    # Menggunakan TF-IDF untuk mengubah dokumen dan query menjadi vektor
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)
    query_vector = vectorizer.transform([query])
    
    # Menghitung kesamaan kosinus antara query dan dokumen
    cosine_similarities = cosine_similarity(query_vector, tfidf_matrix)
    
    # Mengambil dokumen dengan kesamaan tertinggi
    most_relevant_document_index = cosine_similarities.argmax()
    return documents[most_relevant_document_index]

# Inisialisasi riwayat percakapan dengan pesan sistem
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Kamu adalah chatbot bernama Nutri1000, yang dirancang untuk membantu ibu hamil dan menyusui dalam memenuhi kebutuhan nutrisi mereka selama 1000 hari pertama kehidupan (HPK) si kecil. Panggillah lawan bicara dengan 'Bunda'. Misalnya: Halo bunda! Gunakan emoticon disetiap responmu. Tugasmu adalah memberikan informasi gizi, menjawab pertanyaan terkait kesehatan ibu hamil dan menyusui, serta memberikan saran yang berguna tentang pola makan yang sehat selama kehamilan dan menyusui. Kamu juga akan membantu ibu hamil dan menyusui memantau status gizi mereka dan memberikan rekomendasi makanan yang sesuai berdasarkan kebutuhannya. Pastikan kamu selalu ramah, informatif, dan empatik. Jangan memberikan informasi medis yang bersifat mendalam atau pengganti saran dari profesional medis. Fokuslah pada kebutuhan gizi ibu hamil dan menyusui serta memberikan saran praktis yang membantu mereka menjaga pola makan yang sehat. Kamu tidak boleh memberikan saran yang bertentangan dengan pedoman kesehatan atau makanan yang tidak aman selama kehamilan dan menyusui. Contoh: Jika pengguna bertanya tentang 'Apa yang bisa saya makan saat hamil?', kamu akan memberikan contoh makanan sehat yang sesuai untuk ibu hamil. Jika pengguna bertanya tentang 'Apa itu asam folat?', kamu akan menjelaskan manfaat asam folat selama kehamilan dan makanan yang kaya asam folat."}
    ]

# Tampilkan riwayat percakapan sebelumnya
for message in st.session_state.messages:
    if message["role"] != "system":  # Sembunyikan pesan sistem
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Proses input pengguna
if prompt := st.chat_input("Masukkan pertanyaan Anda"):
    # Tampilkan pesan pengguna di antarmuka
    with st.chat_message("user"):
        st.markdown(prompt)

    # Tambahkan pesan pengguna ke riwayat
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Langkah 1: Lakukan pencarian informasi relevan dari dokumen DOCX
    relevant_document = retrieve_relevant_documents(prompt, documents)

    # Langkah 2: Gabungkan hasil pencarian dengan pesan untuk OpenAI API
    full_prompt = f"Berikut adalah informasi relevan yang ditemukan:\n{relevant_document}\n\nTugas kamu adalah memberikan jawaban yang ramah dan informatif untuk ibu hamil atau menyusui berdasarkan informasi ini. Jawab pertanyaan ini: {prompt}"

    # Langkah 3: Panggil API Azure OpenAI untuk mendapatkan respons
    response = openai.ChatCompletion.create(
        deployment_id="gpt-4",  # Pastikan menggunakan deployment_id yang benar
        messages=[ 
            {"role": "system", "content": "Kamu adalah chatbot Nutri1000 yang membantu ibu hamil dan menyusui."},
            {"role": "user", "content": full_prompt}
        ],
        max_tokens=800
    )

    # Ambil respons asisten dan tampilkan di antarmuka
    assistant_message = response['choices'][0]['message']['content']
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
    with st.chat_message("assistant"):
        st.markdown(assistant_message)
