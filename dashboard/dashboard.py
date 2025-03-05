import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
import pandas as pd
import os
import io
import plotly.express as px

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
    st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
    st.title("🚴‍♂️ Bike Sharing Dashboard")
    
    # Sidebar
    st.sidebar.header("🔧 Pengaturan")
    show_pie_chart = st.sidebar.checkbox("Tampilkan Diagram Lingkaran", True)
    show_line_chart = st.sidebar.checkbox("Tampilkan Grafik Garis", True)
    
    # Load data
    merged_data_df = load_data()
    if merged_data_df is None or merged_data_df.empty:
        st.warning("Data tidak tersedia atau kosong.")
        return
    
    # Sidebar untuk memilih kategori produk
    st.sidebar.subheader("📌 Pilih Kategori Produk")
    kategori_produk = merged_data_df["product_category_name_x"].unique()
    selected_category = st.sidebar.selectbox("Pilih kategori untuk ditampilkan", kategori_produk)
    
    # Filter data berdasarkan kategori yang dipilih
    filtered_data = merged_data_df[merged_data_df["product_category_name_x"] == selected_category]
    
    # Tampilkan preview dataset
    st.subheader("📊 Data Review")
    st.write(filtered_data.head())
    
    # Visualisasi 10 Produk Paling Banyak Terjual
    if show_pie_chart:
        st.subheader("🥇 10 Produk Paling Banyak Terjual")
        if 'product_category_name_x' in merged_data_df.columns:
            produk_terlaris = merged_data_df["product_category_name_x"].value_counts().reset_index()
            produk_terlaris.columns = ["product_category_name_x", "total_sold"]
            top_products = produk_terlaris.head(10)
            
            # Debugging: tampilkan data sebelum plotting
            st.write(top_products)
            
            # Plot pie chart dengan Plotly untuk tampilan lebih menarik
            fig = px.pie(
                top_products,
                values='total_sold',
                names='product_category_name_x',
                title="10 Kategori Produk Paling Banyak Terjual",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig)
        else:
            st.warning("Kolom 'product_category_name_x' tidak ditemukan dalam dataset.")
    
    # Visualisasi 5 Kategori Produk dengan Rata-rata Foto Terbanyak
    if show_line_chart:
        st.subheader("📷 5 Kategori Produk dengan Rata-rata Foto Terbanyak")
        if 'product_category_name_x' in merged_data_df.columns and 'product_photos_qty_x' in merged_data_df.columns:
            foto_rata_rata = merged_data_df.groupby("product_category_name_x")["product_photos_qty_x"].mean().reset_index()
            foto_rata_rata = foto_rata_rata.sort_values(by="product_photos_qty_x", ascending=False).head(5)
            
            # Debugging: tampilkan data sebelum plotting
            st.write(foto_rata_rata)
            
            # Plot line chart dengan Plotly
            fig = px.line(
                foto_rata_rata,
                x="product_category_name_x",
                y="product_photos_qty_x",
                markers=True,
                title="5 Kategori Produk dengan Rata-rata Foto Terbanyak",
                color_discrete_sequence=["blue"]
            )
            fig.update_layout(xaxis_title="Kategori Produk", yaxis_title="Rata-rata Jumlah Foto", xaxis_tickangle=-45)
            st.plotly_chart(fig)
        else:
            st.warning("Kolom 'product_category_name_x' atau 'product_photos_qty_x' tidak ditemukan dalam dataset.")

if __name__ == "__main__":
    main()
