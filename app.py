import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# --- Ambil data dari Google Spreadsheet dalam format CSV ---
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1f6m1Bjj3IxCMCbPEcgWt6bsZ7uEz1pK1baiK34XqzlM/export?format=csv"
df = pd.read_csv(spreadsheet_url)

df['PEMINAT 2024'] = df.apply(
    lambda row: row['DAYA TAMPUNG 2025'] if row['PEMINAT 2024'] == 0 else row['PEMINAT 2024'], axis=1
)

# --- Preprocessing ---
df.columns = df.columns.str.strip()
df['NAMA'] = df['NAMA'].astype(str)
df['ASAL UNIV'] = df['ASAL UNIV'].astype(str)
df['DAYA TAMPUNG 2025'] = pd.to_numeric(df['DAYA TAMPUNG 2025'], errors='coerce')
df['PEMINAT 2024'] = pd.to_numeric(df['PEMINAT 2024'], errors='coerce')


# --- Title ---
st.title("📊 Dashboard Analisis Jurusan IPS Berdasarkan Prospek Kerja")

# Insight dan Tim
st.markdown("""
<div style="background-color:#f0f2f6; padding:20px; border-radius:10px; margin-bottom:25px; border-left: 5px solid #0066cc;">
    <h3 style="color:#0066cc;">📌 Insight 4: Jurusan IPS PT Negeri yang Sepi Peminat, Tapi Punya Prospek Kerja Bagus</h3>
    <p style="font-size:16px;">Banyak jurusan di rumpun IPS yang kurang diminati oleh calon mahasiswa, namun justru memiliki prospek karier yang cerah karena rendahnya persaingan dan tingginya kebutuhan di dunia kerja.</p>
    <hr style="border:1px dashed #ccc;">
    <p style="font-size:14px;"><strong>Disusun oleh Tim:</strong><br>
    I Gede Surya Adi Pradana (525) - Universitas Udayana<br>
    I Gede Widnyana (526) - Universitas Udayana<br>
    I Gusti Agung Ayu Gita Pradnyaswari Mantara (527) - Universitas Udayana<br>
    I Gusti Agung Istri Agrivina Shyta Devi (528) - Universitas Udayana
    </p>
</div>
""", unsafe_allow_html=True)

# --- Statistik Umum ---
st.header("📌 Statistik Umum")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Jumlah Program Studi", df['NAMA'].nunique())
col2.metric("Jumlah PTN", df['ASAL UNIV'].nunique())
col3.metric("Total Daya Tampung 2025", int(df['DAYA TAMPUNG 2025'].sum()))
col4.metric("Jumlah Peminat 2024", int(df['PEMINAT 2024'].sum()))


# --- Filter Jalur ---
st.header("🎛️ Filter Jalur Masuk")
jalur_opsi = ["SNBP", "SNBT", "SNBP dan SNBT"]
pilihan_jalur = st.radio("Pilih Jalur:", jalur_opsi)

if pilihan_jalur == "SNBP dan SNBT":
    filtered_df = df[df["JALUR"].isin(["SNBP", "SNBT"])]
else:
    filtered_df = df[df["JALUR"] == pilihan_jalur]

# --- Layout 2 kolom visualisasi ---
def dua_kolom_chart(title1, chart1, insight1, title2, chart2, insight2):
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(title1)
        st.plotly_chart(chart1, use_container_width=True)
        st.markdown(insight1)
    with col2:
        st.subheader(title2)
        st.plotly_chart(chart2, use_container_width=True)
        st.markdown(insight2)

# --- Filter Jurusan dengan Peminat antara 0 - 50 ---
filtered_df_sepi_peminat = filtered_df[(filtered_df['PEMINAT 2024'] >= 0) & (filtered_df['PEMINAT 2024'] <= 50)]

# Ambil 10 jurusan teratas berdasarkan jumlah peminat (0 - 50)
filtered_df_sepi_peminat_top10 = filtered_df_sepi_peminat.nlargest(10, 'PEMINAT 2024')

# --- Filter Jurusan dengan Peminat lebih dari 50 ---
filtered_df_banyak_peminat = filtered_df[filtered_df['PEMINAT 2024'] > 50]

# Ambil 10 jurusan teratas berdasarkan jumlah peminat (> 50)
filtered_df_banyak_peminat_top10 = filtered_df_banyak_peminat.nlargest(10, 'PEMINAT 2024')

# --- Visualisasi Diagram Batang untuk Peminat 0 - 50 ---
fig1 = px.bar(
    filtered_df_sepi_peminat_top10,
    x='PEMINAT 2024',
    y='NAMA',
    orientation='h',
    title="10 Jurusan dengan Peminat 2024 antara 0 dan 50",
    labels={'PEMINAT 2024': 'Jumlah Peminat', 'NAMA': 'Nama Jurusan'},
    color='PEMINAT 2024',
    color_continuous_scale='Viridis'
)

# --- Visualisasi Diagram Batang untuk Peminat lebih dari 50 ---
fig2 = px.bar(
    filtered_df_banyak_peminat_top10,
    x='PEMINAT 2024',
    y='NAMA',
    orientation='h',
    title="10 Jurusan dengan Peminat 2024 lebih dari 50",
    labels={'PEMINAT 2024': 'Jumlah Peminat', 'NAMA': 'Nama Jurusan'},
    color='PEMINAT 2024',
    color_continuous_scale='Viridis'
)

st.header("📊 Top 10 Jurusan dengan Rasio Keketatan Tertinggi")

# --- Filter berdasarkan jalur & kategori jurusan ---
col_jalur, col_kategori = st.columns(2)
jalur_filter = col_jalur.selectbox("Pilih Jalur:", df['JALUR'].unique(), key="jalur_rasio")
kategori_filter = col_kategori.selectbox("Pilih Kategori Jurusan:", df['KATEGORI JURUSAN'].unique(), key="kategori_rasio")

# --- Filter dataframe sesuai pilihan ---
filtered_rasio = df[
    (df['JALUR'] == jalur_filter) &
    (df['KATEGORI JURUSAN'] == kategori_filter)
].copy()

# --- Tangani nilai RASIO KEKETATAN ---
import numpy as np

filtered_rasio['RASIO_ANGKA'] = filtered_rasio['RASIO KEKETATAN'].astype(str).str.replace(',', '.')
filtered_rasio['RASIO_ANGKA'] = filtered_rasio['RASIO_ANGKA'].replace('inf', np.inf)
filtered_rasio['RASIO_ANGKA'] = pd.to_numeric(filtered_rasio['RASIO_ANGKA'], errors='coerce')

# --- Ambil Top 10 ---
top10_rasio = filtered_rasio.sort_values(by='RASIO_ANGKA', ascending=False).head(10)

# --- Format tampilan rasio ---
def format_rasio(x):
    if np.isinf(x):
        return "∞"
    elif pd.isnull(x):
        return "-"
    else:
        return f"{x:.2f}%"

# --- Visualisasi ---
import plotly.express as px
fig_top10 = px.bar(
    top10_rasio,
    x='NAMA',
    y='RASIO_ANGKA',
    text=top10_rasio['RASIO_ANGKA'].apply(format_rasio),
    labels={'RASIO_ANGKA': 'Rasio Keketatan (%)'},
    title=f"Top 10 Jurusan {kategori_filter} - Jalur {jalur_filter} berdasarkan Rasio Keketatan"
)
fig_top10.update_traces(marker_color='darkblue', textposition='outside')
fig_top10.update_layout(xaxis_tickangle=-45, yaxis_title="Rasio Keketatan (%)")
st.plotly_chart(fig_top10, use_container_width=True)

# --- Tabel detail ---
st.subheader("📋 Detail Top 10 Jurusan Berdasarkan Rasio Keketatan")
top10_rasio_formatted = top10_rasio.copy()
top10_rasio_formatted['PEMINAT 2024'] = top10_rasio_formatted['PEMINAT 2024'].apply(lambda x: f"{x:,}")
top10_rasio_formatted['RASIO KEKETATAN'] = top10_rasio_formatted['RASIO KEKETATAN'].astype(str)

st.dataframe(top10_rasio_formatted[[
    'NAMA', 'ASAL UNIV', 'JENJANG', 'DAYA TAMPUNG 2025',
    'PEMINAT 2024', 'RASIO KEKETATAN', 'PROSPEK KERJA'
]])


# --- Total peminat per provinsi ---
df_provinsi = df.groupby('PROVINSI')['PEMINAT 2024'].sum().reset_index()
df_provinsi.columns = ['provinsi', 'total_peminat']

# Pastikan nama kolom sesuai format
# df['PROVINSI'] = df['PROVINSI'].str.upper().str.strip()

# # Group berdasarkan provinsi dan jumlahkan peminat
# df_provinsi = df.groupby('PROVINSI')['PEMINAT 2024'].sum().reset_index()

# df['PROVINSI'] = df['PROVINSI'].str.title().str.strip()

# df_provinsi = df.groupby('PROVINSI')['PEMINAT 2024'].sum().reset_index()

# --- Menghitung Jumlah Peminat per Provinsi ---
df_provinsi = df.groupby('PROVINSI').agg({'PEMINAT 2024': 'sum'}).reset_index()

# --- Mengurutkan data berdasarkan jumlah peminat dari tertinggi ke terendah ---
df_provinsi = df_provinsi.sort_values(by='PEMINAT 2024', ascending=False)

# --- Membuat Diagram Batang berdasarkan Provinsi dan Jumlah Peminat ---
fig = px.bar(
    df_provinsi,
    x='PROVINSI', 
    y='PEMINAT 2024', 
    title="Jumlah Peminat Berdasarkan Provinsi",
    labels={'PEMINAT 2024': 'Jumlah Peminat', 'PROVINSI': 'Provinsi'},
    hover_data={
        'PEMINAT 2024': False,  # Jangan tampilkan jumlah peminat di hover
        'PROVINSI': False,  # Jangan tampilkan provinsi di hover
    }
)

# --- Menambahkan data hover untuk universitas, daya tampung, rasio keketatan, kategori jurusan
fig.update_traces(
    hovertemplate='<b>%{x}</b><br>' +
                  'Nama Universitas: %{customdata[0]}<br>' +
                  'Daya Tampung 2025: %{customdata[1]}<br>' +
                  'Kategori Jurusan: %{customdata[3]}<br>',  # Hapus %{customdata[2]} untuk Rasio Keketatan
    customdata=df[['NAMA', 'DAYA TAMPUNG 2025', 'RASIO KEKETATAN', 'KATEGORI JURUSAN']].values
)

# --- Tampilkan Diagram Batang di Streamlit ---
st.subheader("📊 Diagram Batang Jumlah Peminat Berdasarkan Provinsi")
st.plotly_chart(fig, use_container_width=True)

# --- Insight Otomatis Berdasarkan Provinsi ---
# Jurusan dengan peminat terbanyak dan tersedikit per provinsi
jurusan_terbanyak = df_provinsi.loc[df_provinsi['PEMINAT 2024'].idxmax()]
jurusan_terendah = df_provinsi.loc[df_provinsi['PEMINAT 2024'].idxmin()]

# Menampilkan insight
st.subheader("📊 Insight Otomatis")
st.write(f"🎯 Provinsi dengan jumlah peminat tertinggi adalah **{jurusan_terbanyak['PROVINSI']}** dengan **{jurusan_terbanyak['PEMINAT 2024']} peminat**.")
st.write(f"🎯 Provinsi dengan jumlah peminat paling sedikit adalah **{jurusan_terendah['PROVINSI']}** dengan **{jurusan_terendah['PEMINAT 2024']} peminat**.")

# Rekomendasi
if jurusan_terbanyak['PEMINAT 2024'] > jurusan_terendah['PEMINAT 2024']:
    st.write(f"📌 **Rekomendasi:** Provinsi dengan peminat tertinggi, **{jurusan_terbanyak['PROVINSI']}**, dapat mempertimbangkan **peningkatan kapasitas daya tampung** untuk menampung lebih banyak peminat. Sementara itu, provinsi dengan peminat paling sedikit, **{jurusan_terendah['PROVINSI']}**, perlu melihat strategi **peningkatan daya tarik** untuk jurusan-jurusan tersebut.")
else:
    st.write(f"📌 **Rekomendasi:** Provinsi dengan peminat sedikit mungkin perlu **meningkatkan promosi** atau memperbaiki kualitas pendidikan di wilayah tersebut.")

# --- Tabel Detail ---
st.subheader("📋 Tabel Detail Jumlah Peminat Berdasarkan Provinsi")
st.dataframe(df_provinsi, use_container_width=True)



# --- Fitur Pilih Provinsi ---
provinsi_terpilih = st.selectbox("Pilih Provinsi", df_provinsi['PROVINSI'].unique())

# --- Menampilkan Data untuk Provinsi Terpilih ---
df_provinsi_terpilih = df[df['PROVINSI'] == provinsi_terpilih]

# --- Menghitung Jumlah Peminat per Jurusan di Provinsi Terpilih ---
df_terpilih_jurusan = df_provinsi_terpilih.groupby('NAMA').agg({'PEMINAT 2024': 'sum'}).reset_index()

# --- Mengurutkan data untuk jurusan dengan peminat terbanyak dan tersedikit ---
df_terpilih_jurusan_terbanyak = df_terpilih_jurusan.sort_values(by='PEMINAT 2024', ascending=False)
df_terpilih_jurusan_tersedikit = df_terpilih_jurusan.sort_values(by='PEMINAT 2024', ascending=True)

# --- Menampilkan Diagram Batang Jurusan dengan Peminat Terbanyak ---
fig_terbanyak = px.bar(
    df_terpilih_jurusan_terbanyak,
    x='NAMA', 
    y='PEMINAT 2024', 
    title=f"Jurusan dengan Peminat Terbanyak di {provinsi_terpilih}",
    labels={'PEMINAT 2024': 'Jumlah Peminat', 'NAMA': 'Nama Jurusan'},
    hover_data={
        'PEMINAT 2024': True,
        'NAMA': False
    }
)

# --- Menampilkan Diagram Batang Jurusan dengan Peminat Tersedikit ---
fig_tersedikit = px.bar(
    df_terpilih_jurusan_tersedikit,
    x='NAMA', 
    y='PEMINAT 2024', 
    title=f"Jurusan dengan Peminat Paling Sedikit di {provinsi_terpilih}",
    labels={'PEMINAT 2024': 'Jumlah Peminat', 'NAMA': 'Nama Jurusan'},
    hover_data={
        'PEMINAT 2024': True,
        'NAMA': False
    }
)

# Menampilkan kedua diagram batang di Streamlit
st.subheader(f"📊 Jurusan dengan Peminat Terbanyak di {provinsi_terpilih}")
st.plotly_chart(fig_terbanyak, use_container_width=True)

st.subheader(f"📊 Jurusan dengan Peminat Paling Sedikit di {provinsi_terpilih}")
st.plotly_chart(fig_tersedikit, use_container_width=True)

# --- Insight Otomatis ---
# Jurusan dengan Peminat Terbanyak
jurusan_terbanyak = df_terpilih_jurusan_terbanyak.iloc[0]
jurusan_terendah = df_terpilih_jurusan_tersedikit.iloc[0]

# Menampilkan insight
st.subheader("📊 Insight Otomatis")
st.write(f"🎯 Di provinsi {provinsi_terpilih}, jurusan dengan peminat terbanyak adalah **{jurusan_terbanyak['NAMA']}** dengan **{jurusan_terbanyak['PEMINAT 2024']} peminat**.")
st.write(f"🎯 Sedangkan jurusan dengan peminat paling sedikit adalah **{jurusan_terendah['NAMA']}** dengan **{jurusan_terendah['PEMINAT 2024']} peminat**.")

# Rekomendasi
if jurusan_terbanyak['PEMINAT 2024'] > jurusan_terendah['PEMINAT 2024']:
    st.write(f"📌 **Rekomendasi:** Berdasarkan data, jurusan **{jurusan_terbanyak['NAMA']}** memiliki peminat terbanyak, yang menunjukkan bahwa jurusan ini lebih diminati. **Pihak universitas perlu mempertimbangkan peningkatan kapasitas daya tampung dan rasio keketatan** untuk jurusan ini.")
else:
    st.write(f"📌 **Rekomendasi:** Jurusan dengan peminat paling sedikit perlu mendapat perhatian khusus. Mungkin perlu adanya **upaya untuk meningkatkan daya tarik jurusan tersebut**, seperti penambahan program studi baru atau perbaikan promosi jurusan.")

# --- Tabel Detail ---
st.subheader(f"📋 Detail Universitas per Provinsi {provinsi_terpilih}")
st.dataframe(df_provinsi_terpilih, use_container_width=True)


st.title("🎯 Eksplorasi Jurusan Berdasarkan Provinsi, Universitas, dan Kategori")

# --- Dropdown untuk memilih Provinsi ---
provinsi_terpilih = st.selectbox("📍 Pilih Provinsi", options=df['PROVINSI'].dropna().unique())

# Filter berdasarkan provinsi
df_filtered_prov = df[df['PROVINSI'] == provinsi_terpilih]

# --- Dropdown untuk memilih Universitas dari provinsi yang dipilih ---
univ_terpilih = st.selectbox("🏫 Pilih Universitas", options=df_filtered_prov['ASAL UNIV'].dropna().unique())

# Filter berdasarkan universitas
df_filtered_univ = df_filtered_prov[df_filtered_prov['ASAL UNIV'] == univ_terpilih]

# --- Dropdown untuk memilih Kategori Jurusan ---
kategori_terpilih = st.selectbox("📊 Pilih Kategori Jurusan", options=df_filtered_univ['KATEGORI JURUSAN'].dropna().unique())

# Filter final berdasarkan kategori jurusan
df_final = df_filtered_univ[df_filtered_univ['KATEGORI JURUSAN'] == kategori_terpilih]

# Membersihkan kolom 'RASIO KEKETATAN' dan mengonversinya ke tipe numerik
df_final['RASIO KEKETATAN'] = df_final['RASIO KEKETATAN'].replace({',': ''}, regex=True)  # Menghapus koma sebagai pemisah ribuan
df_final['RASIO KEKETATAN'] = pd.to_numeric(df_final['RASIO KEKETATAN'], errors='coerce')  # Mengonversi ke numerik

# Menggunakan metode groupby dan agregasi
df_jurusan = df_final.groupby('NAMA').agg({
    'RASIO KEKETATAN': 'mean',  # Mengambil nilai rata-rata dari Rasio Keketatan
    # kolom lain yang perlu dihitung agregatnya
})

# --- Pastikan kolom RASIO KEKETATAN bertipe float ---
df['RASIO KEKETATAN'] = (
    df['RASIO KEKETATAN']
    .astype(str)                     # ubah ke string
    .str.replace(',', '.', regex=False)  # ganti koma dengan titik
    .astype(float)                  # konversi ke float
)


# --- Hitung total peminat per jurusan (jika ada duplikat nama) ---
df_jurusan = df_final.groupby('NAMA').agg({
    'PEMINAT 2024': 'sum',
    'DAYA TAMPUNG 2025': 'sum',
    'RASIO KEKETATAN': 'mean',
    'PROSPEK KERJA': 'first'
}).reset_index()

# Urutkan dari jumlah peminat tertinggi
df_jurusan = df_jurusan.sort_values(by='PEMINAT 2024', ascending=False)

# --- Visualisasi diagram batang ---
fig = px.bar(
    df_jurusan,
    x='NAMA',
    y='PEMINAT 2024',
    title=f"Jumlah Peminat Jurusan di {univ_terpilih} ({kategori_terpilih})",
    labels={'NAMA': 'Nama Jurusan', 'PEMINAT 2024': 'Jumlah Peminat'},
    hover_data={
        'DAYA TAMPUNG 2025': True,
        'RASIO KEKETATAN': True,
        'PROSPEK KERJA': True,
    }
)
fig.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig, use_container_width=True)

# --- Insight Otomatis ---
st.subheader("📌 Insight Otomatis")

if not df_jurusan.empty:
    tertinggi = df_jurusan.iloc[0]
    terendah = df_jurusan.iloc[-1]

    st.markdown(f"✅ **Jurusan dengan peminat terbanyak** adalah **{tertinggi['NAMA']}** dengan **{tertinggi['PEMINAT 2024']} peminat**.")
    st.markdown(f"⚠️ **Jurusan dengan peminat paling sedikit** adalah **{terendah['NAMA']}** dengan **{terendah['PEMINAT 2024']} peminat**.")

    st.markdown("📢 **Rekomendasi:**")
    if kategori_terpilih == 'SEPI PEMINAT':
        st.write(f"- Jurusan-jurusan ini memiliki peminat rendah. Rekomendasi untuk universitas: perkuat promosi dan kolaborasi dengan industri terkait seperti bidang **{terendah['PROSPEK KERJA']}**.")
    else:
        st.write(f"- Jurusan dengan peminat tinggi seperti **{tertinggi['NAMA']}** mungkin perlu penambahan **daya tampung** untuk mengakomodasi permintaan yang tinggi.")
else:
    st.warning("Data tidak tersedia untuk pilihan ini.")



# --- Tampilkan Diagram Peminat 0 - 50 ---
st.subheader("📊 Diagram Jurusan IPS dengan Jumlah Peminat antara 0 dan 50")
st.plotly_chart(fig1, use_container_width=True)

# --- Tabel Insight untuk Peminat 0 - 50 ---
insight_table_1 = filtered_df_sepi_peminat_top10[['ASAL UNIV', 'NAMA', 'JENJANG', 'PEMINAT 2024', 'DAYA TAMPUNG 2025', 'PROSPEK KERJA']]
st.write("Pemetaan Jurusan dengan Peminat Rendah (0 - 50):")
st.write(insight_table_1)

# --- Tampilkan Diagram Peminat lebih dari 50 ---
st.subheader("📊 Diagram Jurusan IPS dengan Jumlah Peminat lebih dari 50")
st.plotly_chart(fig2, use_container_width=True)

# --- Tabel Insight untuk Peminat lebih dari 50 ---
insight_table_2 = filtered_df_banyak_peminat_top10[['ASAL UNIV', 'NAMA', 'JENJANG', 'PEMINAT 2024', 'DAYA TAMPUNG 2025', 'PROSPEK KERJA']]
st.write("Pemetaan Jurusan dengan Peminat Tinggi (> 50):")
st.write(insight_table_2)

# --- Diagram Peminat (Top 20 & Bottom 20) ---
peminat_df = filtered_df.groupby("NAMA")["PEMINAT 2024"].sum().reset_index().sort_values("PEMINAT 2024", ascending=False)

top20_peminat = peminat_df.head(20)
bottom20_peminat = peminat_df[peminat_df["PEMINAT 2024"] > 0].tail(20)

# Insight otomatis Peminat
top_peminat = top20_peminat.sort_values("PEMINAT 2024", ascending=False).iloc[0]
bottom_peminat = bottom20_peminat.sort_values("PEMINAT 2024").iloc[0]
insight_top_peminat = f"""
📌 Berdasarkan diagram di atas, Pada jalur **{pilihan_jalur}**, jurusan **{top_peminat['NAMA']}** memiliki jumlah peminat tertinggi sebanyak **{top_peminat['PEMINAT 2024']}** orang. Hal ini mengindikasikan bahwa jurusan ini memiliki daya tarik tinggi, baik dari segi prospek kerja maupun popularitas kampus. Rekomendasinya adalah memperluas kapasitas daya tampung atau membuka kelas tambahan jika memungkinkan.
"""
insight_bottom_peminat = f"""
📌 Berdasarkan diagram di atas, Pada jalur **{pilihan_jalur}**, jurusan **{bottom_peminat['NAMA']}** memiliki jumlah peminat terendah dari 20 terbawah sebanyak **{bottom_peminat['PEMINAT 2024']}** orang. Hal ini bisa jadi karena kurangnya informasi publik, prospek kerja yang belum populer, atau lokasi kampus yang kurang strategis. Rekomendasinya adalah melakukan promosi dan kolaborasi industri untuk menarik minat calon mahasiswa.
"""

fig_top_peminat = px.bar(top20_peminat, x="NAMA", y="PEMINAT 2024", title="Top 20 Jurusan dengan Peminat Terbanyak", labels={"NAMA": "Jurusan"})
fig_bottom_peminat = px.bar(bottom20_peminat, x="NAMA", y="PEMINAT 2024", title="Bottom 20 Jurusan dengan Peminat Terendah", labels={"NAMA": "Jurusan"})

dua_kolom_chart("🔝 Top 20 Peminat", fig_top_peminat, insight_top_peminat,
                "🔻 Bottom 20 Peminat", fig_bottom_peminat, insight_bottom_peminat)

# --- Diagram Daya Tampung (Top 20 & Bottom 20) ---
dt_df = filtered_df.groupby("NAMA")["DAYA TAMPUNG 2025"].sum().reset_index().sort_values("DAYA TAMPUNG 2025", ascending=False)
top20_dt = dt_df.head(20)
bottom20_dt = dt_df[dt_df["DAYA TAMPUNG 2025"] > 0].tail(20)

top_dt = top20_dt.iloc[0]
bottom_dt = bottom20_dt.iloc[0]
insight_top_dt = f"""
📌 Berdasarkan diagram di atas, Pada jalur **{pilihan_jalur}**, jurusan **{top_dt['NAMA']}** memiliki daya tampung tertinggi sebanyak **{top_dt['DAYA TAMPUNG 2025']}** kursi. Ini menunjukkan kesiapan fasilitas dan kemungkinan kebutuhan tinggi akan lulusan bidang tersebut. Rekomendasinya adalah mempertahankan kualitas pengajaran meski dengan jumlah mahasiswa besar.
"""
insight_bottom_dt = f"""
📌 Berdasarkan diagram di atas, Pada jalur **{pilihan_jalur}**, jurusan **{bottom_dt['NAMA']}** memiliki daya tampung terendah dari 20 terbawah sebanyak **{bottom_dt['DAYA TAMPUNG 2025']}** kursi. Jurusan ini mungkin bersifat spesialis atau baru dibuka. Rekomendasi: evaluasi keterisian daya tampung dan dorong kerja sama dengan industri untuk meningkatkan daya tarik.
"""

fig_top_dt = px.bar(top20_dt, x="NAMA", y="DAYA TAMPUNG 2025", title="Top 20 Jurusan dengan Daya Tampung Terbanyak")
fig_bottom_dt = px.bar(bottom20_dt, x="NAMA", y="DAYA TAMPUNG 2025", title="Bottom 20 Jurusan dengan Daya Tampung Terendah")

dua_kolom_chart("🔝 Top 20 Daya Tampung", fig_top_dt, insight_top_dt,
                "🔻 Bottom 20 Daya Tampung", fig_bottom_dt, insight_bottom_dt)


# --- Diagram Peminat Keseluruhan (Terurut) ---
st.header("📈 Visualisasi Keseluruhan Jumlah Peminat per Jurusan")

# Mengelompokkan dan menjumlahkan data peminat
total_peminat_df = filtered_df.groupby("NAMA")["PEMINAT 2024"].sum().reset_index()

# Mengurutkan data berdasarkan peminat 2024 dari yang terbesar ke yang terkecil
total_peminat_df = total_peminat_df.sort_values(by="PEMINAT 2024", ascending=False)

# Membuat diagram batang untuk peminat
fig_all_peminat = px.bar(
    total_peminat_df,
    x="NAMA",
    y="PEMINAT 2024",
    labels={"NAMA": "Jurusan", "PEMINAT 2024": "Jumlah Peminat"},
    title=f"Jumlah Peminat Keseluruhan per Jurusan ({pilihan_jalur})"
)

fig_all_peminat.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_all_peminat, use_container_width=True)

# Insight otomatis peminat keseluruhan
total_jurusan = total_peminat_df['NAMA'].nunique()
avg_peminat = int(total_peminat_df["PEMINAT 2024"].mean())
insight_all_peminat = f"""
📌 Pada jalur **{pilihan_jalur}**, terdapat total **{total_jurusan}** jurusan IPS yang tersedia.  
🔢 Rata-rata jumlah peminat per jurusan adalah sekitar **{avg_peminat}** orang.  
📈 Grafik di atas menunjukkan distribusi jumlah peminat yang bervariasi, dengan beberapa jurusan jauh lebih populer dari yang lain.  
🔍 Rekomendasi: jurusan dengan peminat tinggi bisa menyesuaikan kapasitas, sementara jurusan dengan peminat rendah perlu meningkatkan promosi dan kerja sama eksternal.
"""
st.markdown(insight_all_peminat)


# --- Diagram Daya Tampung Keseluruhan (Terurut) ---
st.header("📥 Visualisasi Keseluruhan Daya Tampung per Jurusan")

# Mengelompokkan dan menjumlahkan data daya tampung
total_daya_df = filtered_df.groupby("NAMA")["DAYA TAMPUNG 2025"].sum().reset_index()

# Mengurutkan data berdasarkan daya tampung 2025 dari yang terbesar ke yang terkecil
total_daya_df = total_daya_df.sort_values(by="DAYA TAMPUNG 2025", ascending=False)

# Membuat diagram batang untuk daya tampung
fig_all_daya = px.bar(
    total_daya_df,
    x="NAMA",
    y="DAYA TAMPUNG 2025",
    labels={"NAMA": "Jurusan", "DAYA TAMPUNG 2025": "Daya Tampung"},
    title=f"Daya Tampung Keseluruhan per Jurusan ({pilihan_jalur})"
)

fig_all_daya.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_all_daya, use_container_width=True)

# Insight otomatis daya tampung keseluruhan
avg_daya = int(total_daya_df["DAYA TAMPUNG 2025"].mean())
insight_all_daya = f"""
📌 Pada jalur **{pilihan_jalur}**, total daya tampung dari semua jurusan adalah **{int(total_daya_df['DAYA TAMPUNG 2025'].sum())}** kursi.  
🔢 Rata-rata daya tampung per jurusan adalah sekitar **{avg_daya}** kursi.  
📥 Grafik memperlihatkan variasi besar dalam daya tampung antar jurusan, yang dapat dipengaruhi oleh kapasitas fakultas, kebijakan kampus, dan kebutuhan industri.  
🔍 Rekomendasi: evaluasi kembali alokasi daya tampung agar lebih proporsional terhadap peminat dan kebutuhan pasar kerja.
"""
st.markdown(insight_all_daya)




# --- Pie Chart Jenjang ---
st.header("🎓 Distribusi Jenjang Pendidikan")
jenjang_df = df['JENJANG'].value_counts().reset_index()
jenjang_df.columns = ['Jenjang', 'Jumlah']
fig_jenjang = px.pie(jenjang_df, names='Jenjang', values='Jumlah', title="Distribusi Jenjang", hover_data=['Jumlah'], labels={'Jumlah': 'Jumlah'})
fig_jenjang.update_traces(textinfo='percent+label')
st.plotly_chart(fig_jenjang, use_container_width=True)

# Insight jenjang
insight_jenjang = f"""
📌 Pada jalur **{pilihan_jalur}**, Sebagian besar program studi berada pada jenjang **{jenjang_df.iloc[0]['Jenjang']}** dengan jumlah **{jenjang_df.iloc[0]['Jumlah']}** program studi. Ini menandakan dominasi program sarjana dalam ranah IPS di PTN Indonesia. Rekomendasi: dorong peningkatan jenjang pendidikan lanjutan untuk memperluas akses ke pendidikan pascasarjana.
"""
st.markdown(insight_jenjang)

# --- Perbandingan Peminat vs Daya Tampung (Top & Bottom 10) ---
st.header("📊 Perbandingan Peminat vs Daya Tampung")

compare_df = filtered_df.groupby("NAMA")[["PEMINAT 2024", "DAYA TAMPUNG 2025"]].sum().reset_index()
top10_compare = compare_df.sort_values("PEMINAT 2024", ascending=False).head(10)
bottom10_compare = compare_df.sort_values("PEMINAT 2024", ascending=True).head(10)

fig_top10_compare = px.bar(top10_compare.melt(id_vars="NAMA"), x="NAMA", y="value", color="variable",
                           barmode="group", title="Top 10 Peminat vs Daya Tampung")
fig_bottom10_compare = px.bar(bottom10_compare.melt(id_vars="NAMA"), x="NAMA", y="value", color="variable",
                              barmode="group", title="Bottom 10 Peminat vs Daya Tampung")

insight_top10_compare = f"""
📌 Pada jalur **{pilihan_jalur}**, 10 jurusan teratas memiliki jumlah peminat yang jauh melampaui daya tampung. Hal ini menunjukkan persaingan yang sangat ketat dan popularitas tinggi jurusan tersebut.  
🔍 Rekomendasi: pertimbangkan peningkatan daya tampung atau pembukaan kelas paralel, serta lakukan seleksi masuk yang lebih kompetitif.
"""

insight_bottom10_compare = f"""
📌 Pada jalur **{pilihan_jalur}**, 10 jurusan terbawah memiliki jumlah peminat yang relatif rendah dibandingkan daya tampung yang tersedia.  
🔍 Rekomendasi: lakukan promosi jurusan melalui media digital dan kolaborasi industri agar lebih dikenal, serta evaluasi kurikulum agar sesuai dengan kebutuhan pasar kerja.
"""

dua_kolom_chart("Top 10 Peminat vs Daya Tampung", fig_top10_compare, insight_top10_compare,
                "Bottom 10 Peminat vs Daya Tampung", fig_bottom10_compare, insight_bottom10_compare)

# --- Diagram Prospek Kerja ---
st.header("💼 Persebaran Prospek Kerja")
prospek_df = df['PROSPEK KERJA'].value_counts().reset_index()
prospek_df.columns = ['Prospek Kerja', 'Jumlah']
fig_prospek = px.bar(prospek_df, x='Prospek Kerja', y='Jumlah', title="Distribusi Prospek Kerja", labels={"Jumlah": "Jumlah Lulusan"})
st.plotly_chart(fig_prospek, use_container_width=True)

# Insight prospek kerja
top_prospek = prospek_df.iloc[0]
insight_prospek = f"""
📌 Berdasarkan diagram di atas, prospek kerja sebagai **{top_prospek['Prospek Kerja']}** mendominasi dengan **{top_prospek['Jumlah']}** jurusan yang mengarah ke bidang ini. Ini menunjukkan permintaan tinggi dan kesesuaian kurikulum pendidikan dengan kebutuhan industri. Rekomendasi: dorong kolaborasi lebih lanjut antara kampus dan sektor industri ini.
"""

st.markdown(insight_prospek)

# --- Diagram Jumlah Jurusan per Universitas (Top 20 & Bottom 20) ---
st.header("🏫 Jumlah Jurusan per Universitas")

# Hitung jumlah jurusan unik per universitas
jurusan_per_univ = df.groupby("ASAL UNIV")["NAMA"].nunique().reset_index()
jurusan_per_univ.columns = ["Universitas", "Jumlah Jurusan"]
jurusan_per_univ = jurusan_per_univ.sort_values("Jumlah Jurusan", ascending=False)

# Ambil Top 20 dan Bottom 20
top20_univ = jurusan_per_univ.head(20)
bottom20_univ = jurusan_per_univ.tail(20)

# Insight otomatis
top_univ = top20_univ.iloc[0]
bottom_univ = bottom20_univ.iloc[-1]
insight_top_univ = f"""
📌 Pada jalur **{pilihan_jalur}**, universitas **{top_univ['Universitas']}** memiliki jumlah jurusan terbanyak yaitu **{top_univ['Jumlah Jurusan']}**. Ini mencerminkan kapasitas akademik yang luas dan ragam pilihan bagi calon mahasiswa di jalur tersebut.  
🔍 Rekomendasi: pastikan kualitas tiap jurusan tetap terjaga melalui evaluasi berkala dan penguatan kolaborasi akademik.
"""

insight_bottom_univ = f"""
📌 Pada jalur **{pilihan_jalur}**, universitas **{bottom_univ['Universitas']}** hanya memiliki **{bottom_univ['Jumlah Jurusan']}** jurusan. Hal ini bisa menunjukkan fokus pada bidang tertentu atau kapasitas institusi yang terbatas.  
🔍 Rekomendasi: evaluasi potensi pengembangan jurusan baru untuk memperluas akses pendidikan di jalur {pilihan_jalur.lower()}.
"""


# Visualisasi dengan Plotly
fig_top20_univ = px.bar(
    top20_univ,
    x="Universitas",
    y="Jumlah Jurusan",
    title="Top 20 Universitas dengan Jumlah Jurusan Terbanyak",
    labels={"Universitas": "Universitas", "Jumlah Jurusan": "Jumlah Jurusan"},
    hover_data=["Universitas"]
)
fig_bottom20_univ = px.bar(
    bottom20_univ,
    x="Universitas",
    y="Jumlah Jurusan",
    title="Bottom 20 Universitas dengan Jumlah Jurusan Tersedikit",
    labels={"Universitas": "Universitas", "Jumlah Jurusan": "Jumlah Jurusan"},
    hover_data=["Universitas"]
)

# Tampilkan visual dan insight secara berdampingan
dua_kolom_chart("🏆 Top 20 Universitas", fig_top20_univ, insight_top_univ,
                "📉 Bottom 20 Universitas", fig_bottom20_univ, insight_bottom_univ)


st.header("🔮 Prediksi Kategori Jurusan (Machine Learning)")

# --- Preprocessing untuk model ---
df_model = df.copy()

# Encode target
df_model['KATEGORI JURUSAN'] = df_model['KATEGORI JURUSAN'].map({'SEPI PEMINAT': 0, 'RAMAI PEMINAT': 1})

# Encode label kategori
label_cols = ['ASAL UNIV', 'PROVINSI', 'PROSPEK KERJA', 'JALUR', 'NAMA', 'JENJANG']
label_encoders = {}
for col in label_cols:
    le = LabelEncoder()
    df_model[col] = le.fit_transform(df_model[col].astype(str))
    label_encoders[col] = le

# Fitur yang digunakan (tanpa RASIO KEKETATAN)
fitur = ['PEMINAT 2024', 'ASAL UNIV', 'PROVINSI',
         'DAYA TAMPUNG 2025', 'PROSPEK KERJA', 'JALUR', 'NAMA', 'JENJANG']

# Data training
X = df_model[fitur]
y = df_model['KATEGORI JURUSAN']

# Latih model
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# --- Form input pengguna ---
st.subheader("📝 Masukkan Data Jurusan")

with st.form("form_prediksi"):
    peminat = st.number_input("Peminat 2024", min_value=0)
    daya_tampung = st.number_input("Daya Tampung 2025", min_value=0)

    asal_univ = st.selectbox("Asal Universitas", label_encoders['ASAL UNIV'].classes_)
    provinsi = st.selectbox("Provinsi", label_encoders['PROVINSI'].classes_)
    prospek = st.selectbox("Prospek Kerja", label_encoders['PROSPEK KERJA'].classes_)
    jalur = st.selectbox("Jalur", label_encoders['JALUR'].classes_)
    nama = st.selectbox("Nama Jurusan", label_encoders['NAMA'].classes_)
    jenjang = st.selectbox("Jenjang", label_encoders['JENJANG'].classes_)

    pred_button = st.form_submit_button("Prediksi Kategori")

# --- Prediksi ---
if pred_button:
    input_data = [[
        peminat,
        label_encoders['ASAL UNIV'].transform([asal_univ])[0],
        label_encoders['PROVINSI'].transform([provinsi])[0],
        daya_tampung,
        label_encoders['PROSPEK KERJA'].transform([prospek])[0],
        label_encoders['JALUR'].transform([jalur])[0],
        label_encoders['NAMA'].transform([nama])[0],
        label_encoders['JENJANG'].transform([jenjang])[0],
    ]]
    hasil = model.predict(input_data)[0]
    kategori = "RAMAI PEMINAT" if hasil == 1 else "SEPI PEMINAT"
    st.success(f"✅ Prediksi: Jurusan ini termasuk **{kategori}**.")
