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

st.subheader("Data Cleaning")
st.write("Data day.csv yang sudah dibersihkan:")
st.write(day_df.head())

st.write("Data hour.csv yang sudah dibersihkan:")
st.write(hour_df.head())

st.subheader("Exploratory Data")
st.markdown("""
#### Perbandingan jumlah pengguna dan rentang suhu
""")
suhu_agg = round(day_df.groupby(
    by=pd.cut(day_df['suhu'], bins=[-10, 0, 10, 20, 30, 40, 50], include_lowest=True), 
    observed=False
).agg({
    'kasual': 'sum',
    'terdaftar': 'sum',
    'total': 'sum'
}), 2).reset_index().sort_values(by='total', ascending=False)

suhu_agg.columns = ['Rentang Suhu (°C)', 'Pengguna Kasual', 'Pengguna Terdaftar', 'Total Jumlah Pengguna']

# Menampilkan DataFrame di Streamlit
st.write("Data Pengguna berdasarkan Rentang Suhu:")
st.dataframe(suhu_agg)

st.subheader("Visualisasi korelasi suhu dan total penyewaan")
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