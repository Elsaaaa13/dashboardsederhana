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
    
    # Sidebar
    st.sidebar.header("🔧 Pengaturan")
    show_pie_chart = st.sidebar.checkbox("Tampilkan Diagram Lingkaran", True)
    show_line_chart = st.sidebar.checkbox("Tampilkan Grafik Garis", True)
    
    # Load data
    merged_data_df = load_data()
    if merged_data_df is None or merged_data_df.empty:
        st.warning("Data tidak tersedia atau kosong.")
        return
    
    # Tampilkan preview dataset
    st.subheader("📊 Data Review")
    st.write(merged_data_df.head())
    
    # Visualisasi 10 Produk Paling Banyak Terjual
    if show_pie_chart:
        st.subheader("🥇 10 Produk Paling Banyak Terjual")
        if 'product_category_name_x' in merged_data_df.columns:
            produk_terlaris = merged_data_df["product_category_name_x"].value_counts().reset_index()
            produk_terlaris.columns = ["product_category_name_x", "total_sold"]
            top_products = produk_terlaris.head(10)
            
            # Debugging: tampilkan data sebelum plotting
            st.write(top_products)
            
            # Gunakan palet warna yang sama seperti di Google Colab
            colors = sns.color_palette("tab10", len(top_products))
            
            # Plot pie chart
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.pie(
                top_products['total_sold'],
                labels=top_products['product_category_name_x'],
                autopct='%1.1f%%',
                colors=colors,
                startangle=140
            )
            ax.axis("equal")  # Menjaga aspek agar lingkaran sempurna
            plt.title("10 Kategori Produk Paling Banyak Terjual")
            
            st.pyplot(fig)
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
            
            # Plot line chart
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.lineplot(
                x="product_category_name_x",
                y="product_photos_qty_x",
                data=foto_rata_rata,
                marker="o",
                linewidth=2,
                color="b",
                ax=ax
            )
            
            ax.set_xlabel("Kategori Produk")
            ax.set_ylabel("Rata-rata Jumlah Foto")
            ax.set_title("5 Kategori Produk dengan Rata-rata Foto Terbanyak")
            ax.set_xticklabels(foto_rata_rata["product_category_name_x"], rotation=45)
            
            st.pyplot(fig)
        else:
            st.warning("Kolom 'product_category_name_x' atau 'product_photos_qty_x' tidak ditemukan dalam dataset.")

if __name__ == "__main__":
    main()
