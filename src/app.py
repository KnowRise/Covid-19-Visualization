import os
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load data
BASE_DIR = os.path.dirname(__file__)
csv_path = os.path.join(BASE_DIR, '../data/covid_19_indonesia_time_series_all_clean.csv')
df = pd.read_csv(csv_path)
df['Date'] = pd.to_datetime(df['Date'])

# Membuat pivot untuk heatmap
df_pivot = df.pivot_table(values='New Cases', index='Location', columns='Date', aggfunc='sum')

# Streamlit App
st.title("Analisis Data COVID-19 di Indonesia")
st.write("Visualisasi dan Analisis Interaktif untuk Data COVID-19.")

# Section 1: Grafik Kasus Baru, Kematian Baru, Kesembuhan Baru
st.header("Kasus Harian COVID-19 di Indonesia")
df_grouped = df.groupby('Date').sum()
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df_grouped.index, df_grouped['New Cases'], label='New Cases', color='red')
ax.plot(df_grouped.index, df_grouped['New Deaths'], label='New Deaths', color='blue')
ax.plot(df_grouped.index, df_grouped['New Recovered'], label='New Recovered', color='green')
ax.set_title("Kasus Baru COVID-19 per Hari di Indonesia")
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Kasus Baru")
ax.legend()
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))  # Setiap 3 bulan
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # Format label jadi "YYYY-MM"
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

# Section 2: Fatality & Recovery Rate
st.header("Persentase Fatality dan Recovery")
df_grouped['Fatality Rate (%)'] = (df_grouped['Total Deaths'] / df_grouped['Total Cases']) * 100
df_grouped['Recovery Rate (%)'] = (df_grouped['Total Recovered'] / df_grouped['Total Cases']) * 100
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df_grouped.index, df_grouped['Fatality Rate (%)'], label='Fatality Rate (%)', color='red')
ax.plot(df_grouped.index, df_grouped['Recovery Rate (%)'], label='Recovery Rate (%)', color='green')
ax.set_title("Persentase Fatality dan Recovery COVID-19 di Indonesia")
ax.set_xlabel("Tanggal")
ax.set_ylabel("Persentase (%)")
ax.legend()
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))  # Setiap 3 bulan
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # Format label jadi "YYYY-MM"
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

# Section 3: Kasus Tertinggi di 3 Lokasi
st.header("Kasus Tertinggi di 3 Lokasi")
top_locations = df.groupby('Location')['Total Cases'].max().nlargest(3).index
fig, ax = plt.subplots(figsize=(12, 8))
for loc in top_locations:
    df_location = df[df['Location'] == loc]
    df_location_grouped = df_location.groupby('Date').sum()
    ax.plot(df_location_grouped.index, df_location_grouped['Total Cases'], label=f'{loc} Total Cases')
ax.set_title("Perbandingan Kasus COVID-19 di 3 Lokasi dengan Kasus Tertinggi")
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Kasus")
ax.legend()
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))  # Setiap 3 bulan
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # Format label jadi "YYYY-MM"
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

# Section 4: Kasus Aktif Harian
st.header("Perubahan Harian Kasus Aktif")
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df_grouped.index, df_grouped['New Active Cases'], label='New Active Cases', color='orange')
ax.set_title("Perubahan Harian Kasus Aktif COVID-19 di Indonesia")
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Kasus Aktif Baru")
ax.legend()
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))  # Setiap 3 bulan
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # Format label jadi "YYYY-MM"
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

# Section 5: Grafik per Lokasi (Interactive Slider)
st.header("Grafik per Lokasi")
selected_location = st.selectbox("Pilih Lokasi", options=df['Location'].drop_duplicates().sort_values())
df_location = df[df['Location'] == selected_location]
df_location_grouped = df_location.groupby('Date').sum()

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df_location_grouped.index, df_location_grouped['Total Cases'], label='Total Cases', color='blue')
ax.plot(df_location_grouped.index, df_location_grouped['Total Deaths'], label='Total Deaths', color='red')
ax.plot(df_location_grouped.index, df_location_grouped['Total Recovered'], label='Total Recovered', color='green')
ax.set_title(f"Total Kasus, Kematian, dan Kesembuhan COVID-19 di {selected_location}")
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Kasus")
ax.legend()
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))  # Setiap 3 bulan
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # Format label jadi "YYYY-MM"
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)
