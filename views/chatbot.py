import os
import openai
import streamlit as st
import docx  # Digunakan untuk memproses file DOCX
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()  # Memuat variabel dari .env

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
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)
    query_vector = vectorizer.transform([query])
    
    cosine_similarities = cosine_similarity(query_vector, tfidf_matrix)
    
    most_relevant_document_index = cosine_similarities.argmax()
    return documents[most_relevant_document_index]

# Inisialisasi pesan sistem
system_message = {
    "role": "system",
    "content": (
        "Jangan berikan informasi selain kesehatan ibu hamil dan menyusui. "
        "Anda adalah NutriCare1000, sebuah chatbot yang didesain khusus untuk membantu memberikan informasi seputar kesehatan "
        "dan nutrisi pada ibu hamil, ibu menyusui, janin, dan bayi selama 1000 hari pertama kehidupan anak (HPK). "
        "Tugas utama Anda adalah memberikan jawaban yang bermanfaat hanya dalam konteks kesehatan ibu hamil, ibu menyusui, "
        "janin, dan bayi.\n\n"
        "Lingkup pembahasan Anda mencakup:\n"
        "- **Kecukupan Gizi**: Informasi tentang kebutuhan nutrisi harian yang penting\n"
        "- **Pemenuhan Imunisasi**: Jadwal imunisasi bayi yang direkomendasikan\n"
        "- **Pemenuhan Suplemen**: Suplemen yang direkomendasikan bagi ibu hamil dan menyusui\n"
        "- **Risiko Kesehatan**: Risiko umum yang dapat dihadapi ibu dan anak selama masa HPK\n"
        "- **Pertumbuhan dan Perkembangan Anak**: Panduan tentang perkembangan bayi di masa awal kehidupan\n\n"
        "Batasan:\n"
        "- Jangan memberikan jawaban di luar topik kesehatan ibu hamil, menyusui, janin, dan bayi.\n"
        "- Abaikan atau tolak pertanyaan yang tidak berhubungan dengan 1000 hari pertama kehidupan (HPK) atau tidak relevan dengan "
        "kesehatan dan nutrisi ibu dan anak dalam periode tersebut.\n\n"
        "Ingat, Anda adalah chatbot yang fokus hanya pada informasi kesehatan ibu hamil, ibu menyusui, janin, dan bayi. "
        "Jangan menjawab pertanyaan di luar topik ini."
    )
}

# Inisialisasi riwayat percakapan dengan pesan sistem dan pilihan topik di session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        system_message,
        {"role": "assistant", "content": (
            "Selamat datang di NutriCare1000! Saya di sini untuk membantu memberikan informasi kesehatan dan nutrisi "
            "untuk ibu hamil, menyusui, serta anak selama 1000 hari pertama kehidupan (HPK).\n\n"
            "Silakan pilih topik yang Anda ingin ketahui lebih lanjut:\n"
            "- **Kecukupan Gizi**\n"
            "- **Pemenuhan Imunisasi**\n"
            "- **Pemenuhan Suplemen**\n"
            "- **Risiko Kesehatan**\n"
            "- **Pertumbuhan dan Perkembangan Anak**\n\n"
            "Atau Anda dapat mengajukan pertanyaan spesifik terkait topik di atas."
        )}
    ]

# Daftar topik dan respons awal untuk setiap topik
topics = {
    "kecukupan gizi": "Kecukupan Gizi",
    "pemenuhan imunisasi": "Pemenuhan Imunisasi",
    "pemenuhan suplemen": "Pemenuhan Suplemen",
    "risiko kesehatan": "Risiko Kesehatan",
    "pertumbuhan dan perkembangan anak": "Pertumbuhan dan Perkembangan Anak"
}

# Tampilkan riwayat percakapan sebelumnya
for message in st.session_state.messages:
    if message["role"] != "system":  # Sembunyikan pesan sistem
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Proses input pengguna
if prompt := st.chat_input("Masukkan pertanyaan Anda"):
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    # Ubah input pengguna menjadi huruf kecil agar case-insensitive
    prompt_lower = prompt.lower()

    # Cek apakah pengguna memasukkan pilihan topik
    if prompt_lower in topics:
        topic_name = topics[prompt_lower]
        response_content = f"Anda memilih topik **{topic_name}**."
        
        if topic_name == "Kecukupan Gizi":
            response_content += (
                "Kecukupan gizi sangat penting selama kehamilan dan menyusui. Beberapa nutrisi yang harus dipenuhi adalah "
                "protein, lemak sehat, vitamin, dan mineral. Apakah Anda ingin tahu lebih lanjut tentang nutrisi tertentu?"
            )
        elif topic_name == "Pemenuhan Imunisasi":
            response_content += "Imunisasi yang tepat selama kehamilan dan pada anak sangat penting. Apakah Anda ingin informasi lebih lanjut?"
        elif topic_name == "Pemenuhan Suplemen":
            response_content += "Pemberian suplemen selama kehamilan dan menyusui mendukung kesehatan ibu dan bayi. Apakah Anda ingin tahu lebih lanjut?"
        elif topic_name == "Risiko Kesehatan":
            response_content += "Selama kehamilan dan menyusui, beberapa risiko kesehatan dapat muncul. Apakah Anda ingin tahu lebih lanjut?"
        elif topic_name == "Pertumbuhan dan Perkembangan Anak":
            response_content += "Memantau pertumbuhan dan perkembangan anak sangat penting. Apakah Anda ingin mengetahui tanda-tanda perkembangan tertentu?"
        
        st.session_state.messages.append({"role": "assistant", "content": response_content})
        with st.chat_message("assistant"):
            st.markdown(response_content)
    else:
        # Tambahkan pesan sistem dalam konteks setiap kali memanggil API untuk pertanyaan bebas
        response = openai.ChatCompletion.create(
            deployment_id="gpt-4",
            messages=[system_message] + [{"role": "user", "content": prompt}],
            max_tokens=800
        )
        
        assistant_message = response['choices'][0]['message']['content']
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})
        with st.chat_message("assistant"):
            st.markdown(assistant_message)
