import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

st.set_page_config(
    page_title="Dashboard Produksi",
    page_icon="📊",
    layout="wide"
)

st.title("🚲 Analisis Pengguna Sepeda")
st.markdown("Menganalisis pola penggunaan selama 2 tahun.")

hour_df = pd.read_csv("data/hour.csv")
day_df = pd.read_csv("data/day.csv")

datetime_column = ["dteday", "date_time"]
for column in datetime_column:
    if column in day_df.columns:
        day_df[column] = pd.to_datetime(day_df[column])
    if column in hour_df.columns:
        hour_df[column] = pd.to_datetime(hour_df[column])

day_order = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']
day_df['weekday'] = day_df['weekday'].map({0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'})
day_df['weekday'] = pd.Categorical(day_df['weekday'], categories=day_order, ordered=True)

st.sidebar.header("Filter Data")
selected_season = st.sidebar.selectbox("Pilih Musim", ['Semua Musim', 'Semi', 'Gugur', 'Panas', 'Dingin'])
show_total_users = st.sidebar.checkbox("Tampilkan Total Pengguna")

season_map = {'Semi': 1, 'Gugur': 2, 'Panas': 3, 'Dingin': 4}
if selected_season == 'Semua Musim':
    filtered_df = hour_df
else:
    filtered_df = hour_df[hour_df['weathersit'] == season_map[selected_season]]

casual_avg = filtered_df['casual'].mean()
registered_avg = filtered_df['registered'].mean()
total_avg = filtered_df['cnt'].mean() if show_total_users else None

st.metric("📌 Pengguna Casual", f"{casual_avg:.2f}")
st.metric("📌 Pengguna Registered", f"{registered_avg:.2f}")
if show_total_users:
    st.metric("📌 Total Pengguna", f"{total_avg:.2f}")

st.subheader("📊 Perbandingan Penggunaan Sepeda")
if selected_season == 'Semua Musim':
    labels = ['Semi', 'Gugur', 'Panas', 'Dingin']
    casual_values = [hour_df[hour_df['weathersit'] == season_map[season]]['casual'].mean() for season in labels]
    registered_values = [hour_df[hour_df['weathersit'] == season_map[season]]['registered'].mean() for season in labels]
    
    x = np.arange(len(labels))
    width = 0.40
    
    fig, ax = plt.subplots()
    ax.bar(x - width/2, casual_values, width, label='Casual', color='blue')
    ax.bar(x + width/2, registered_values, width, label='Registered', color='green')
    
    ax.set_xlabel('Musim')
    ax.set_ylabel('Rata-rata Pengguna')
    ax.set_title('Perbandingan Penggunaan Sepeda per Musim')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    
    st.pyplot(fig)
else:
    labels = ['Casual', 'Registered']
    values = [casual_avg, registered_avg]
    
    fig, ax = plt.subplots()
    ax.bar(labels, values, color=['blue', 'green'])
    ax.set_ylabel("Rata-rata Pengguna")
    ax.set_title(f"Penggunaan Sepeda di Musim {selected_season}")
    
    st.pyplot(fig)

day_avg = day_df.groupby('weekday').mean()

st.subheader("📈 Tren Penggunaan Sepeda per Hari")
fig2, ax2 = plt.subplots(figsize=(6, 4))
ax2.plot(day_avg.index, day_avg['casual'], marker='o', linestyle='-', color='b', label='Casual Users')
ax2.plot(day_avg.index, day_avg['registered'], marker='s', linestyle='-', color='g', label='Registered Users')
ax2.plot(day_avg.index, day_avg['cnt'], marker='^', linestyle='-', color='r', label='Total Users')
ax2.set_xlabel('Hari dalam Seminggu')
ax2.set_ylabel('Rata-rata Pengguna')
ax2.set_title('Tren Penggunaan Sepeda')
ax2.legend()
ax2.grid(True, linestyle='--', alpha=0.6)

st.pyplot(fig2)
st.write(f"Current Directory: {os.getcwd()}")
