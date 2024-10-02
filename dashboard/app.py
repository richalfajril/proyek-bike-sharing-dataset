import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

#Dataset
day_df = pd.read_csv('data/day.csv')
hour_df = pd.read_csv('data/hour.csv')

## Streamlit app title
st.title("Bike Sharing Data Analysis")
st.subheader("oleh : Richal Fajril")

st.markdown("""
## **KARAKTERISTIK DATA**
Baik hour.csv maupun day.csv memiliki kolom-kolom berikut, kecuali hr yang tidak tersedia di day.csv

- **instant:** indeks rekaman
- **dteday:** tanggal
- **season:** musim (1: semi, 2: panas, 3: gugur, 4: dingin)
- **yr:** tahun (0: 2011, 1: 2012)
- **mnth:** bulan (1 hingga 12)
- **hr:** jam (0 hingga 23)
- **holiday:** apakah hari tersebut adalah hari libur atau tidak
- **weekday:** hari dalam seminggu
- **workingday:** jika hari tersebut bukan akhir pekan maupun hari libur adalah 1, jika tidak 0.
- **weathersit:**
    - 1: Jelas, Beberapa awan, Sebagian berawan
    - 2: Kabut + Berawan, Kabut + Awan terputus, Kabut + Beberapa awan, Kabut
    - 3: Salju ringan, Hujan ringan + Badai petir + Awan tersebar, Hujan ringan + Awan tersebar
    - 4: Hujan deras + Peluru es + Badai petir + Kabut, Salju + Kabut
- **temp:** Suhu yang dinormalisasi dalam Celsius. Nilai dibagi 41 (maks)
- **atemp:** Suhu yang dirasakan yang dinormalisasi dalam Celsius. Nilai dibagi 50 (maks)
- **hum:** Kelembapan yang dinormalisasi. Nilai dibagi 100 (maks)
- **windspeed:** Kecepatan angin yang dinormalisasi. Nilai dibagi 67 (maks)
- **casual:** jumlah pengguna kasual
- **registered:** jumlah pengguna terdaftar
- **cnt:** jumlah total sepeda sewa termasuk kasual dan terdaftar

Sumber: readme.txt dalam zip dataset
""")

# Menampilkan 5 data teratas dari data day
st.subheader("Menampilkan 5 data teratas dari data day.csv")
st.write(day_df.head())

# Menampilkan 5 data teratas dari data hour
st.subheader("Menampilkan 5 data teratas dari data hour.csv")
st.write(hour_df.head())

