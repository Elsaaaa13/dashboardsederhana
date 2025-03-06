import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
import pandas as pd
import os
import io

# Atur gaya Seaborn
sns.set_theme(style="whitegrid", context="talk")

# Tentukan path absolut ke file CSV dan gambar
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, "data_terbaru.csv")

@st.cache_data
def load_data():
    """Load dataset dengan pengecekan error."""
    st.write("🔍 Mencari file data...")  # Debugging path file dihapus
    if not os.path.exists(data_path):
        st.error("⚠️ File data tidak ditemukan!")
        return None
    try:
        return pd.read_csv(data_path, encoding="utf-8", delimiter=",")
    except Exception as e:
        st.error(f"⚠️ Error loading data: {e}")
        return None
    
def main():
    st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")
    st.title("🏪 E-Commerce Dashboard")
    
    # Sidebar
    st.sidebar.header("🔧 Pengaturan")
    show_city_chart = st.sidebar.checkbox("Tampilkan Grafik Kota Pelanggan", True)
    
    # Load data
    merged_data_df = load_data()
    if merged_data_df is None or merged_data_df.empty:
        st.warning("🚫 Data tidak tersedia atau kosong.")
        return
    
    # Tampilkan preview dataset
    st.subheader("📊 Data Review")
    st.write(merged_data_df.head())
    
    # Visualisasi Dari Kota Mana Pelanggan Berasal
    if show_city_chart:
        st.subheader("🌍 Kota Asal Pelanggan")
        if 'customer_city' in merged_data_df.columns:
            city_counts = merged_data_df['customer_city'].value_counts().head(10)
            colors = sns.color_palette("pastel", len(city_counts))
            
            fig, ax = plt.subplots(figsize=(12, 6))
            city_counts.plot(kind='bar', color=colors, edgecolor='black', ax=ax)
            
            ax.set_title("10 Kota dengan Pelanggan Terbanyak", fontsize=14)
            ax.set_xlabel("Kota", fontsize=12)
            ax.set_ylabel("Jumlah Pelanggan", fontsize=12)
            ax.set_xticklabels(city_counts.index, rotation=45)
            ax.grid(axis='y', linestyle='--', alpha=0.7)
            
            st.pyplot(fig)
        else:
            st.warning("⚠️ Kolom 'customer_city' tidak ditemukan dalam dataset.")

if __name__ == "__main__":
    main()
