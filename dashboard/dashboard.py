import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
import pandas as pd
import os

# Atur gaya Seaborn
sns.set_theme(style="whitegrid", context="talk")

# Tentukan path absolut ke file CSV dan gambar
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, "data_baru.csv")

@st.cache_data
def load_data():
    """Load dataset dengan pengecekan error."""
    if not os.path.exists(data_path):
        st.error(f"File data tidak ditemukan: {data_path}")
        return None
    try:
        return pd.read_csv(data_path)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None
    
def main():
    st.title("🚴‍♂️ Bike Sharing Dashboard")

    # Load data
    merged_data_df = load_data()
    if merged_data_df is None or merged_data_df.empty:
        st.warning("Data tidak tersedia atau kosong.")
        return
    
    # Tampilkan preview dataset
    st.subheader("📊 Data Review")
    st.write(merged_data_df.head())
    
    # Menampilkan informasi dataset
    st.subheader("📈 Informasi Dataset")
    buffer = []
    merged_data_df.info(buf=buffer)
    st.text("\n".join(buffer))
    
    # Statistik deskriptif
    st.subheader("📉 Statistik Deskriptif")
    st.write(merged_data_df.describe())

if __name__ == "__main__":
    main()