import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import json
import folium
from streamlit_folium import folium_static

import plotly.io as pio
pio.renderers.default = 'firefox'

st.set_page_config(page_title="Dashboard Monitoring", page_icon=":material/team_dashboard:", layout="wide")
st.title("NutriCare 1000 Dashboard Monitoring")

df = pd.read_excel('data/dummy_data.xlsx')
idn_prov = json.load(open('data/idn_prov.geojson', 'r'))

jml_pengguna = df["id"].count()

# Data for Bar Chart Pengguna by Usia
kat_usia = []
for value in df["usia"]:
    if value < 19:
        kat_usia.append("<19")
    elif value >= 19 and value < 25:
        kat_usia.append("19-25")
    elif value >= 25 and value < 30:
        kat_usia.append("25-30")
    elif value >= 30 and value < 35:
        kat_usia.append("30-35")
    elif value >= 35 and value < 40:
        kat_usia.append("35-40")
    else:
        kat_usia.append(">40")
df["kategori usia"] = kat_usia

kat_usia_label = {"kategori usia":["<19","19-25","25-30","30-35","35-40",">40"]}
df_kat_usia = pd.DataFrame(kat_usia_label)
df_usia = df[["id","kategori usia"]].groupby(["kategori usia"]).count()
df_usia.rename(columns={'id':'jumlah'}, inplace=True)
df_usia = pd.merge(df_kat_usia,df_usia, how="left", on="kategori usia")
df_usia = df_usia.fillna(0)

# Data for Pie Chart status Ibu
df_stat_ibu = df[["id","status ibu"]].groupby(["status ibu"]).count()
df_stat_ibu.rename(columns={'id':'jumlah'}, inplace=True)

# Data for Pie Chart Status Kenaikan Berat Badan (BB) Ibu Hamil
df_bb_bumil = df[df["status ibu"] == "Hamil"]
df_bb_bumil = df[["id","status bb"]].groupby(["status bb"]).count()
df_bb_bumil.rename(columns={'id':'jumlah'}, inplace=True)

# Data for WordCloud
makanan = df["konsumsi makanan"].str.cat(sep=', ')

# Data for Map
df_by_wilayah = pd.read_excel('data/idn_prov_attr.xlsx')

c1, c2, c3 = st.columns(3)
with c1:
    with st.container(border=True, height=500):
        st.html("""<div style='background-color: #333b68; border-radius: 1rem; padding: 1rem 1rem; color:white;'>
                <h5 style='padding-bottom:0; color: white;'>Jumlah Pengguna</h5>
                <h3 style='color: white;'>"""+str(jml_pengguna)+"""</h3>
                </div>
                """)
        fig = px.bar(df_usia, x="kategori usia", y="jumlah", title="Usia Pengguna")
        fig.update_yaxes(type="category")
        fig.update_layout(
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
with c2:
    with st.container(border=True, height=500):
        fig = px.pie(df_stat_ibu, values="jumlah", names=df_stat_ibu.index, title="Status Ibu")
        st.plotly_chart(fig, use_container_width=True)
with c3:
    with st.container(border=True, height=500):
        fig = px.pie(df_bb_bumil, values="jumlah", names=df_bb_bumil.index, title="Status Kenaikan Berat Badan (BB) Ibu Hamil")
        st.plotly_chart(fig, use_container_width=True)

c4, c5 = st.columns((1,2))
with c4:
    st.html("<h4>Konsumsi Makanan Harian</h4>")
    # plt.rcParams['figure.figsize']=(20,20)
    wordcloud = WordCloud(max_font_size=70, max_words=20, background_color="white").generate(makanan)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(plt.gcf())
with c5:
    st.html("<h4>Sebaran Status Gizi Pengguna</h4>")
    fig = px.choropleth(df_by_wilayah, locations="id_wilayah", geojson=idn_prov, featureidkey="properties.id_wilayah", color="kode status gizi", scope="asia")
    fig.update_geos(fitbounds="locations")
    st.plotly_chart(fig)

    # Alternative Map
    # m = folium.Map(location=[-2.638450777665013, 116.03361226277096], tiles='CartoDB positron', zoom_start=5)
    # folium.Choropleth(
    #     geo_data=idn_prov,
    #     name="choropleth",
    #     data=df,
    #     columns=["id_wilayah"],
    #     key_on="feature.properties.id_wilayah"
    # ).add_to(m)
    # folium.GeoJson(idn_prov).add_to(m)
    # folium_static(m, width=800, height=400)


