import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Dashboard Produksi",
    page_icon="📊",
    layout="wide"
)

# --- Header ---
st.title("🚲 Analisis Pengguna Sepeda")
st.markdown("Menganalisis pola penggunaan selama 2 tahun.")

# Gathering data

hour_df = pd.read_csv("../data/data_1.csv")
day_df = pd.read_csv("../data/data_2.csv")

# Clean data
datetime_column = ["dteday", "date_time"]

for column in datetime_column:
    if column in day_df.columns:
        day_df[column] = pd.to_datetime(day_df[column])
    if column in hour_df.columns:
        hour_df[column] = pd.to_datetime(hour_df[column])

# Explore data
hour_df1 = hour_df.sample(frac=0.75, random_state=42)

semi = hour_df1[hour_df1['weathersit'] == 1]
gugur = hour_df1[hour_df1['weathersit'] == 2]
panas = hour_df1[hour_df1['weathersit'] == 3]
dingin = hour_df1[hour_df1['weathersit'] == 4]

semi_casual = semi['casual'].mean()
semi_registered = semi['registered'].mean()
gugur_casual = gugur['casual'].mean()
gugur_registered = gugur['registered'].mean()
panas_casual = panas['casual'].mean()
panas_registered = panas['registered'].mean()
dingin_casual = dingin['casual'].mean()
dingin_registered = dingin['registered'].mean()

weekday_map = {0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'}
day_df['weekday'] = day_df['weekday'].map(weekday_map)

avg_count = day_df.groupby('weekday')['cnt'].mean().reindex(weekday_map.values())
avg_casual = day_df.groupby('weekday')['casual'].mean().reindex(weekday_map.values())
avg_registered = day_df.groupby('weekday')['registered'].mean().reindex(weekday_map.values())

# Layout dengan kolom
col1, col2 = st.columns(2)

# Visualisasi Perbandingan Penggunaan Sepeda pada Setiap Musim
with col1:
    st.subheader("📊 Perbandingan Penggunaan Sepeda")
    labels = ['Semi', 'Gugur', 'Panas', 'Dingin']
    math_scores = [semi_casual, gugur_casual, panas_casual, dingin_casual]
    science_scores = [semi_registered, gugur_registered, panas_registered, dingin_registered]

    x = np.arange(len(labels))
    width = 0.40

    fig, ax = plt.subplots(figsize=(6, 4))
    rects1 = ax.bar(x - width, math_scores, width, label='Casual', color='b')
    rects2 = ax.bar(x, science_scores, width, label='Registered', color='g')

    ax.set_xlabel('Musim')
    ax.set_ylabel('Total Pelanggan')
    ax.set_title('Penggunaan Sepeda per Musim')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    st.pyplot(fig)

# Visualisasi Tren Penggunaan Sepeda
with col2:
    st.subheader("📈 Tren Penggunaan Sepeda")
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.plot(avg_casual.index, avg_casual.values, marker='o', linestyle='-', color='b', label='Casual Users')
    ax2.plot(avg_registered.index, avg_registered.values, marker='s', linestyle='-', color='g', label='Registered Users')
    ax2.plot(avg_count.index, avg_count.values, marker='s', linestyle='-', color='r', label='Count Users')

    ax2.set_xlabel('Hari dalam Seminggu')
    ax2.set_ylabel('Rata-rata Pengguna')
    ax2.set_title('Tren Penggunaan Sepeda')
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.6)

    st.pyplot(fig2)
    st.write(f"Current Directory: {os.getcwd()}")