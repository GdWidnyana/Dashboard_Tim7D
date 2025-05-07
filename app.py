import streamlit as st
import pandas as pd
import plotly.express as px

# --- Ambil data dari Google Spreadsheet dalam format CSV ---
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1f6m1Bjj3IxCMCbPEcgWt6bsZ7uEz1pK1baiK34XqzlM/export?format=csv"
df = pd.read_csv(spreadsheet_url)

# --- Preprocessing ---
df.columns = df.columns.str.strip()
df['NAMA'] = df['NAMA'].astype(str)
df['ASAL UNIV'] = df['ASAL UNIV'].astype(str)
df['DAYA TAMPUNG 2025'] = pd.to_numeric(df['DAYA TAMPUNG 2025'], errors='coerce')
df['PEMINAT 2024'] = pd.to_numeric(df['PEMINAT 2024'], errors='coerce')

# --- Title ---
st.title("📊 Dashboard Analisis Jurusan IPS Berdasarkan Prospek Kerja")

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
