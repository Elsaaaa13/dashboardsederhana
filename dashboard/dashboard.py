import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np

# Produk yang paling banyak terjual
st.subheader("Top 10 Best-Selling Product Categories")

# Mengambil 10 produk terlaris
top_products = main_df.groupby("product_category_name_x")["total_sold"].sum().reset_index()
top_products = top_products.sort_values(by="total_sold", ascending=False).head(10)

# Warna unik untuk setiap kategori
colors = plt.cm.get_cmap("tab10", len(top_products))

# Membuat pie chart
fig, ax = plt.subplots(figsize=(10, 6))
ax.pie(
    top_products["total_sold"],
    labels=top_products["product_category_name_x"],
    autopct='%1.1f%%',
    colors=[colors(i) for i in range(len(top_products))],
    startangle=140
)
ax.set_title("10 Kategori Produk Paling Banyak Terjual")
st.pyplot(fig)

# Rata-rata jumlah foto per kategori
st.subheader("Top 5 Categories with Most Photos")

# Menghitung rata-rata jumlah foto per kategori
foto_rata_rata = main_df.groupby("product_category_name_x")["product_photos_qty_x"].mean().reset_index()
foto_rata_rata = foto_rata_rata.sort_values(by="product_photos_qty_x", ascending=False).head(5)

# Membuat line plot
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(
    x="product_category_name_x",
    y="product_photos_qty_x",
    data=foto_rata_rata,
    marker="o",
    linewidth=2,
    color="b"
)
ax.set_xlabel("Kategori Produk")
ax.set_ylabel("Rata-rata Jumlah Foto")
ax.set_title("5 Kategori Produk dengan Rata-rata Foto Terbanyak")
plt.xticks(rotation=45)
st.pyplot(fig)
