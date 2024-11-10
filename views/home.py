import streamlit as st
import requests
from streamlit_lottie import st_lottie
# from PIL import Image


# --- ASSETS ---
def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
lottie_animation_cover = "https://lottie.host/8ce8c83b-97d6-462a-8018-1d62ada90eae/Gs3hychMqc.json"
lottie_animation_chatbot = "https://lottie.host/5fa0be2f-a498-4170-80ba-59780869d63e/zzEbfiQMU7.json"
lottie_animation_dashboard = "https://lottie.host/fb4754d6-54bf-409c-9260-210edb861d79/4PNhXFJ1wE.json"
# img_fitur1 = Image.open("images/fitur1_img.png")
# img_fitur2 = Image.open("images/fitur2_img.png")
# img_fitur3 = Image.open("images/fitur3_img.png")
img_fitur1 = "images/fitur1_img.png"
img_fitur2 = "images/fitur2_img.png"
img_fitur3 = "images/fitur3_img.png"


# --- PAGE CONFIG ---
logo = "images/logo_nutricare.png"
st.set_page_config(page_title="NutriCare 1000 Mockup", page_icon=logo, layout="wide")
# st.set_page_config(page_title="NutriCare 1000 Mockup", page_icon=":woman_feeding_baby:", layout="wide")


# --- HEADER SECTION ---
with st.container():
    left_column, right_column = st.columns(2)
    with left_column:
        st.title("NutriCare 1000")
        # st.subheader("Asisten kesehatan cerdas untuk tumbuh kembang optimum buah hatimu tercinta")
        st.subheader("Yuk, cegah stunting dengan NutriCare 1000! Dampingi ibu dalam 1000 Hari Pertama Kehidupan (HPK) dengan dukungan AI.")
    with right_column:
        st_lottie(lottie_animation_cover, height=300, key="cover-animation")


# --- OVERVIEW SECTION ---
with st.container():
    st.write("---")
    st.header("Kenapa NutriCare 1000?")
    c1, c2, c3 = st.columns(3)
    with c1:
        img_col, text_col = st.columns((1,2), vertical_alignment="center")
        with img_col:
            st.image(img_fitur1)
        with text_col:
            st.html("<h5>Pemantauan Status Gizi Ibu</h5>")
    with c2:
        img_col, text_col = st.columns((1,2), vertical_alignment="center")
        with img_col:
            st.image(img_fitur2)
        with text_col:
            st.html("<h5>Informasi Gizi Harian, Tips untuk Ibu, dan Konsultasi</h5>")
    with c3:
        img_col, text_col = st.columns((1,2), vertical_alignment="center")
        with img_col:
            st.image(img_fitur3)
        with text_col:
            st.html("<h5>Dashboard Monitoring Pemerintah</h5>") 


# --- CHATBOT DESCRIPTION ---
with st.container():
    st.write("---")
    left_column, right_column = st.columns((1,2), vertical_alignment="center")
    with left_column:
        st_lottie(lottie_animation_chatbot, height=300, key="chatbot-animation")
    with right_column:
        st.header("NutriCare 1000 Chatbot Assistat")
        st.html("<p>Mari memelihara 1000 Hari Pertama Kehidupan (HPK) bersama! NutriCare 1000 Chatbot siap memantau kondisi gizi ibu dan bayi, memberikan saran dan informasi, serta kemudahan konsultasi. Bersama NutriCare 1000, kita wujudkan generasi bebas stunting sejak awal kehidupan!</p>")
        st.button("Buka Chatbot")


# --- DASHBOARD DESCRIPTION ---
with st.container():
    st.write("---")
    left_column, right_column = st.columns((2,1), vertical_alignment="center")
    with left_column:
        st.header("NutriCare 1000 Dashboard Monitoring")
        st.html("<p>Dashboard ini menyajikan visualisasi data agregat pengguna untuk memantau demografi ibu dan anak, kondisi kesehatan ibu hamil, dan tumbuh kembang anak di masa1000 Hari Pertama Kehidupan (HPK). Informasi dari dashboard ini dapat dijadikan dasar dalam perumusan kebijakan pencegahan stunting berbasis data. Yuk pantau kondisinya!</p>")
        st.button("Buka Dashboard")
    with right_column:
        st_lottie(lottie_animation_dashboard, height=300, key="dashboard-animation")

