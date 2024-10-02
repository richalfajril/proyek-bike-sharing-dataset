import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

#Dataset
day_df = pd.read_csv('data/day.csv')
hour_df = pd.read_csv('data/hour.csv')


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