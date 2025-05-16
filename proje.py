import streamlit as st
import json
import urllib.parse
from datetime import datetime
import pytz

# proje.json dosyasını yükle
with open("proje.json", "r", encoding="utf-8") as dosya:
    aktiviteler = json.load(dosya)

# Türkiye 81 ili listesi
iller = [
    "Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Amasya", "Ankara", "Antalya",
    "Artvin", "Aydın", "Balıkesir", "Bilecik", "Bingöl", "Bitlis", "Bolu",
    "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır",
    "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun",
    "Gümüşhane", "Hakkari", "Hatay", "Isparta", "Mersin", "İstanbul", "İzmir",
    "Kars", "Kastamonu", "Kayseri", "Kırklareli", "Kırşehir", "Kocaeli", "Konya",
    "Kütahya", "Malatya", "Manisa", "Kahramanmaraş", "Mardin", "Muğla", "Muş",
    "Nevşehir", "Niğde", "Ordu", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop",
    "Sivas", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Şanlıurfa", "Uşak",
    "Van", "Yozgat", "Zonguldak", "Aksaray", "Bayburt", "Karaman", "Kırıkkale",
    "Batman", "Şırnak", "Bartın", "Ardahan", "Iğdır", "Yalova", "Karabük",
    "Kilis", "Osmaniye", "Düzce"
]

ruh_halleri = {
    "Farketmez": "Farketmez",
    "Mutlu": "😊 Mutlu",
    "Üzgün": "😢 Üzgün",
    "Enerjik": "⚡ Enerjik",
    "Yorgun": "😴 Yorgun",
    "Sakin": "🧘 Sakin",
    "Meraklı": "🤔 Meraklı"
}

def turkiye_saati_al():
    return datetime.now(pytz.timezone("Europe/Istanbul"))

turkiye_saati = turkiye_saati_al()

st.set_page_config(page_title="MoodMatrix", layout="wide")

# Sidebar filtreleri
with st.sidebar:
    st.header("🔎 Filtreler")
    secilen_il = st.selectbox("Konum/Şehir", options=iller, index=iller.index("İstanbul"))
    secilen_ruh_hali_etiket = st.selectbox("Ruh Haliniz", options=list(ruh_halleri.values()))
    secilen_ruh_hali = [k for k,v in ruh_halleri.items() if v == secilen_ruh_hali_etiket][0]
    secilen_butce = st.selectbox("Bütçe", ["Farketmez", "Ücretsiz", "Ücretli"])
    secilen_kimle = st.selectbox("Kiminle?", ["Farketmez", "Yalnız", "Arkadaşlarla", "Aileyle"])
    secilen_aktivite_turu = st.selectbox("Aktivite Türü", ["Farketmez", "Kültürel Keşif", "Etkinlik", "Açık Hava Aktivitesi"])

# Başlık ve bilgi alanı
st.markdown(
    f"""
    <div style='background-color:#D6EAF8; padding:20px; border-radius:10px;'>
        <h1 style='text-align:center; color:black; font-size:3rem; margin-bottom:0;'>🌍 MoodMatrix</h1>
        <div style='display:flex; justify-content:center; gap:3rem; margin-top:10px; color:black;'>
            <p style='margin:0; font-weight:bold;'>📍 Konum: {secilen_il}</p>
            <p style='margin:0; font-weight:bold;'>🌡️ Hava: 23°C</p>
            <p style='margin:0; font-weight:bold;'>🕒 Saat: {turkiye_saati.strftime("%H:%M")}</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Filtreleme fonksiyonu
def aktiviteleri_filtrele():
    filtrelenmis = []
    for aktivite in aktiviteler:
        if secilen_il.lower() not in aktivite["location"].lower():
            continue
        if secilen_ruh_hali != "Farketmez" and aktivite["mood"] != secilen_ruh_hali:
            continue
        if secilen_butce != "Farketmez" and aktivite["budget"] != secilen_butce:
            continue
        if secilen_kimle != "Farketmez" and aktivite["with"] != secilen_kimle:
            continue
        if secilen_aktivite_turu != "Farketmez" and aktivite["type"] != secilen_aktivite_turu:
            continue
        filtrelenmis.append(aktivite)
    return filtrelenmis

filtrelenmis_aktiviteler = aktiviteleri_filtrele()

st.markdown("---")
st.header("🎯 Önerilen Aktiviteler")

if not filtrelenmis_aktiviteler:
    st.info("Seçimlerinize uygun aktivite bulunamadı.")
else:
    for aktivite in filtrelenmis_aktiviteler:
        query = urllib.parse.quote(aktivite["location"])
        maps_url = f"https://www.google.com/maps/search/?api=1&query={query}"
        emoji_ruh_hali = ruh_halleri.get(aktivite["mood"], aktivite["mood"])

        st.markdown(
            f"""
            <div style='background-color:#D6EAF8; padding:15px; border-left:5px solid #1E88E5; border-radius:8px; margin-bottom:15px; color:black;'>
                <h4 style='margin-bottom:5px; color:black;'>{aktivite['name']}</h4>
                <p style='margin:0; color:black;'>📍 <b>{aktivite['location']}</b></p>
                <p style='margin:0; color:black;'>🧠 Ruh Hali: {emoji_ruh_hali} | 💰 Bütçe: {aktivite['budget']}</p>
                <p style='margin:0; color:black;'>👥 Kiminle: {aktivite['with']} | Tür: {aktivite['type']}</p>
                <p style='margin-top:5px;'><a href="{maps_url}" target="_blank" style='color:#1E88E5;'>📍 Haritada Göster</a></p>
            </div>
            """,
            unsafe_allow_html=True
        )
