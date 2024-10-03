import streamlit as st
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

#Dataset
day_df = pd.read_csv('data/day.csv')
hour_df = pd.read_csv('data/hour.csv')
cday_df = pd.read_csv('cleaned_day_data.csv')
chour_df = pd.read_csv('cleaned_hour_data.csv')

st.title("Bike Sharing Data Analysis")
st.subheader("oleh Richal Fajril")

st.subheader("Gathering Data")

st.markdown("Membaca data day.csv dan menampilkan 5 data acak")
st.write(day_df.sample(5))

st.markdown("Membaca data hour.csv dan menampilkan 5 data acak")
st.write(hour_df.sample(5))


#Data Cleaning
day_df["dteday"] = pd.to_datetime(day_df["dteday"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

day_df.rename(columns={
    "instant": "no",
    "dteday": "tanggal",
    "season": "musim",
    "yr": "tahun",
    "mnth": "bulan",
    "holiday": "hari_libur",
    "weekday": "hari",
    "workingday": "hari_kerja",
    "weathersit": "cuaca",
    "temp": "suhu",
    "atemp": "suhu_subjek",
    "hum": "kelembapan",
    "windspeed": "kecepatan_angin",
    "casual": "kasual",
    "registered": "terdaftar",
    "cnt": "total"
}, inplace=True)

hour_df.rename(columns={
    "instant": "no",
    "dteday": "tanggal",
    "season": "musim",
    "yr": "tahun",
    "mnth": "bulan",
    "holiday": "hari_libur",
    "hr": "jam",
    "weekday": "hari",
    "workingday": "hari_kerja",
    "weathersit": "cuaca",
    "temp": "suhu",
    "atemp": "suhu_subjek",
    "hum": "kelembapan",
    "windspeed": "kecepatan_angin",
    "casual": "kasual",
    "registered": "terdaftar",
    "cnt": "total"
}, inplace=True)

categories = ['musim', 'bulan', 'hari', 'cuaca']

for category in categories:
    day_df[category] = day_df[category].astype('category')
    hour_df[category] = hour_df[category].astype('category')

def konversi (df, col_and_ctg):
    for col, ctg in col_and_ctg.items():
        df[col] = df[col].cat.rename_categories(ctg)
    return df

season_dict = {
    'musim':{
        1:'Semi',
        2:'Panas',
        3:'Gugur',
        4:'Dingin'
    }
}

day_df = konversi(day_df, season_dict)
hour_df = konversi(hour_df, season_dict)

month_dict = {
    'bulan':{
        1: 'Januari',
        2: 'Februari',
        3: 'Maret',
        4: 'April',
        5: 'Mei',
        6: 'Juni',
        7: 'Juli',
        8: 'Agustus',
        9: 'September',
        10: 'Oktober',
        11: 'November',
        12: 'Desember'
    }
}

day_df = konversi(day_df, month_dict)
hour_df = konversi(hour_df, month_dict)

day_dict = {
    'hari':{
        0: 'Minggu',
        1: 'Senin',
        2: 'Selasa',
        3: 'Rabu',
        4: 'Kamis',
        5: 'Jumat',
        6: 'Sabtu'
    }
}

day_df = konversi(day_df, day_dict)
hour_df = konversi(hour_df, day_dict)

#Konversi Cuaca
weather_dict = {
    'cuaca':{
        1: 'Cerah',
        2: 'Berkabut',
        3: 'Hujan/Salju Ringan',
        4: 'Hujan/Salju Lebat'
    }
}

day_df = konversi(day_df, weather_dict)
hour_df = konversi(hour_df, weather_dict)

year_mapping = {
    0: '2011',
    1: '2012'
}

day_df['tahun'] = day_df['tahun'].map(year_mapping)
hour_df['tahun'] = hour_df['tahun'].map(year_mapping)

def return_value(df):
    df['suhu'] = (df['suhu'] * 41).round().astype(int)
    df['suhu_subjek'] = (df['suhu_subjek'] * 50).round().astype(int)
    df['kelembapan'] = (df['kelembapan'] * 100).round().astype(int)
    df['kecepatan_angin'] = (df['kecepatan_angin'] * 67).round().astype(int)
    return df


hour_df = return_value(hour_df)
day_df = return_value(day_df)

hour_df['jam'] = hour_df['jam'].apply(lambda x: '{:02d}:00'.format(x))

#Data Cleaning
st.subheader("Data Cleaning")
st.write("Data day.csv yang sudah dibersihkan:")
st.write(day_df.head())

st.write("Data hour.csv yang sudah dibersihkan:")
st.write(hour_df.head())

st.subheader("Exploratory Data")
st.markdown("""
##### 1. Perbandingan jumlah pengguna dan rentang suhu
""")

#Perbandingan jumlah pengguna dan rentang suhu
suhu_bins = [-10, 0, 10, 20, 30, 40, 50]
suhu_labels = ['-10 - 0', '0 - 10', '10 - 20', '20 - 30', '30 - 40', '40 - 50']

suhu_agg = round(day_df.groupby(
    by=pd.cut(day_df['suhu'], bins=suhu_bins, labels=suhu_labels, include_lowest=True, right=False), 
    observed=False
).agg({
    'kasual': 'sum',
    'terdaftar': 'sum',
    'total': 'sum'
}), 2).reset_index().sort_values(by=[], ascending=False)

suhu_agg.columns = ['Rentang Suhu (°C)', 'Pengguna Kasual', 'Pengguna Terdaftar', 'Total Jumlah Pengguna']
st.write("Data Pengguna berdasarkan Rentang Suhu:")
st.dataframe(suhu_agg)

#Mengetahui korelasi suhu terhadap total pengguna
st.markdown("""
##### 2. Mengetahui korelasi suhu terhadap total pengguna
""")
correlation = day_df['suhu'].corr(day_df['total'])

if correlation > 0.7:
    result = f"Korelasi positif yang sangat kuat bernilai: {correlation:.2f}"
elif correlation > 0.5:
    result = f"Korelasi positif yang kuat bernilai: {correlation:.2f}"
elif correlation > 0:
    result = f"Korelasi positif yang lemah bernilai: {correlation:.2f}"
else:
    result = f"Tidak ada korelasi yang signifikan. Nilai korelasi: {correlation:.2f}"

st.write(result)

#Mengetahui suhu yang sering dipilih pengguna untuk meminjam sepeda
st.markdown("""
##### 3. Mengetahui suhu yang sering dipilih pengguna untuk meminjam sepeda
""")
choose_temp = day_df.groupby('suhu', observed=True)['total'].sum().reset_index()
most_temp = choose_temp.loc[choose_temp['total'].idxmax()]
least_temp = choose_temp.loc[choose_temp['total'].idxmin()]

st.write("Suhu dengan penyewaan sepeda tertinggi:")
st.write(f"Suhu: {most_temp['suhu']}°C - Total Penyewaan: {most_temp['total']}")

st.write("Suhu dengan penyewaan sepeda terendah:")
st.write(f"Suhu: {least_temp['suhu']}°C - Total Penyewaan: {least_temp['total']}")

#Perbandingan jumlah pengguna dan kecepatan angin
st.markdown("""
##### 4. Perbandingan jumlah pengguna dan kecepatan angin
""")
kecepatan_bins = [0, 10, 20, 30, 40]
kecepatan_labels = ['0 - 10 km/h', '10 - 20 km/h', '20 - 30 km/h', '30 - 40 km/h']

user_v_windspeed = round(day_df.groupby(
    by=pd.cut(day_df['kecepatan_angin'], bins=kecepatan_bins, labels=kecepatan_labels, include_lowest=True, right=False), 
    observed=False
).agg({
    'suhu': 'mean',
    'suhu_subjek': 'mean',
    'total': 'sum'
}), 2).reset_index().sort_values(by=[], ascending=False)

user_v_windspeed.columns = ['Rentang Kecepatan Angin (km/h)', 'Rata-rata Suhu (°C)', 'Rata-rata Suhu Subjektif (°C)', 'Total Jumlah Pengguna']

st.write("Data Pengguna berdasarkan Rentang Kecepatan Angin:")
st.dataframe(user_v_windspeed)

#Mengetahui korelasi kecepatan angin terhadap pengguna
st.markdown("""
##### 5. Mengetahui korelasi kecepatan angin terhadap pengguna
""")
corr_wind = day_df[['kecepatan_angin', 'total']].corr().iloc[0, 1]

if corr_wind > 0.7:
    correlation_message = f"Korelasi positif yang sangat kuat bernilai: {corr_wind:.2f}"
elif corr_wind > 0.5:
    correlation_message = f"Korelasi positif yang kuat bernilai: {corr_wind:.2f}"
elif corr_wind < 0:
    correlation_message = f"Korelasi negatif yang lemah bernilai: {corr_wind:.2f}"
else:
    correlation_message = f"Tidak ada korelasi yang signifikan: {corr_wind:.2f}"

st.write(correlation_message)

# Mengetahui variasi jumlah pengguna terhadap tinggi atau rendahnya angin
st.markdown("""
#####  6. Mengetahui variasi jumlah pengguna terhadap tinggi atau rendahnya angin
""")
windspeed = day_df.groupby('kecepatan_angin', observed=True)['total'].sum().reset_index()
most_wspeed = windspeed.loc[windspeed['total'].idxmax()]
least_wspeed = windspeed.loc[windspeed['total'].idxmin()]

st.write("Kecepatan angin dengan penyewaan sepeda tertinggi:")
st.write(f"Kecepatan Angin: {most_wspeed['kecepatan_angin']} km/h, Total Penyewaan: {most_wspeed['total']}")
st.write("Kecepatan angin penyewaan sepeda terendah:")
st.write(f"Kecepatan Angin: {least_wspeed['kecepatan_angin']} km/h, Total Penyewaan: {least_wspeed['total']}")

#Visualisasi Data
st.subheader("Visualisasi Data")
st.markdown("""
##### Pertanyaan 1: Bagaimana suhu mempengaruhi jumlah user? Apakah terdapat batas suhu tertentu yang menunjukkan perubahan signifikan dalam jumlah user?
""")
st.write("Visualisasi korelasi suhu dan total penyewaan ")
fig, ax = plt.subplots(figsize=(12, 6))
sns.scatterplot(x=day_df['suhu'], y=day_df['total'], 
                hue=day_df['total'],  # Menggunakan data hue yang sesuai
                size=day_df['total'], 
                palette='viridis',  
                alpha=0.6,
                ax=ax)

# Menambahkan title dan label
ax.set_title('Hubungan antara Suhu dan Total Penyewaan', fontsize=16)
ax.set_xlabel('Suhu (°C)', fontsize=12)
ax.set_ylabel('Total Penyewaan', fontsize=12)

# Menambahkan grid dan legenda
ax.legend(title='Total Penyewaan')
ax.grid(True, linestyle='--', alpha=0.5)

# Menampilkan plot di Streamlit
st.pyplot(fig)

st.markdown("""
**Insight Chart 1:**
- Terdapat kecenderungan positif antara suhu dan total penyewaan. Artinya, semakin tinggi suhu, cenderung semakin banyak jumlah sepeda yang disewa. Hal ini mengindikasikan bahwa cuaca yang hangat atau panas mendorong lebih banyak orang untuk menggunakan sepeda.
- Terlihat adanya pengelompokan data pada rentang suhu tertentu, terutama pada suhu yang lebih hangat. Hal ini menunjukkan bahwa pada rentang suhu tertentu, terdapat lonjakan permintaan terhadap penyewaan sepeda.
""")
#2
st.write("Visualisasi perbandingan jumlah pengguna berdasarkan rentang suhu ")

plt.figure(figsize=(12, 6))

sns.barplot(x='Rentang Suhu (°C)', y='value', hue='variable', data=pd.melt(suhu_agg, id_vars=['Rentang Suhu (°C)']))
plt.title('Perbandingan Jumlah Pengguna Berdasarkan Rentang Suhu')
plt.xlabel('Rentang Suhu (°C)')
plt.ylabel('Jumlah Pengguna')
plt.legend(title='Jenis Pengguna')

st.pyplot(plt)

st.markdown("""
**Insight Chart 2:**
- Secara umum, jumlah pengguna cenderung meningkat seiring dengan kenaikan suhu, terutama untuk pengguna terdaftar. Hal ini mengindikasikan bahwa suhu yang lebih tinggi mungkin lebih disukai oleh pengguna terdaftar.
- Jumlah pengguna kasual juga cenderung meningkat seiring dengan kenaikan suhu, namun tidak setajam peningkatan pengguna terdaftar. Ini menunjukkan bahwa suhu juga mempengaruhi perilaku pengguna kasual, meskipun tidak sebesar pengaruhnya pada pengguna terdaftar.
- Jumlah pengguna kasual juga cenderung meningkat seiring dengan kenaikan suhu, namun tidak setajam peningkatan pengguna terdaftar. Ini menunjukkan bahwa suhu juga mempengaruhi perilaku pengguna kasual, meskipun tidak sebesar pengaruhnya pada pengguna terdaftar.
- Grafik total pengguna mengikuti tren yang serupa dengan pengguna terdaftar, menunjukkan bahwa pengguna terdaftar memberikan kontribusi yang lebih besar terhadap peningkatan total pengguna.
- Rentang suhu (20, 30) tampaknya menjadi rentang suhu yang optimal untuk menarik dan mempertahankan pengguna, terutama pengguna terdaftar.            
""")
#3
st.write("Visualisasi korelasi suhu dan total penyewaan ")


st.markdown("""
            
""")


#pertanyaan 2
st.markdown("""
            
""")
st.write("Visualisasi korelasi suhu dan total penyewaan ")


st.markdown("""
            
""")


st.write("Visualisasi korelasi suhu dan total penyewaan ")


st.markdown("""
            
""")


st.write("Visualisasi korelasi suhu dan total penyewaan ")


st.markdown("""
            
""")
