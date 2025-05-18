# Laporan Proyek Machine Learning - I Gede Widnyana

## Domain Proyek

Proyek ini berada dalam domain pendidikan tinggi, khususnya pada analisis data peminatan jurusan IPS di Indonesia. Setiap tahun, jutaan siswa bersaing untuk mendapatkan kursi di perguruan tinggi negeri melalui berbagai jalur seleksi. Salah satu permasalahan yang muncul adalah ketimpangan minat antara jurusan-jurusan tertentu. Beberapa jurusan menjadi sangat populer, sementara lainnya justru sepi peminat. Masalah ini penting untuk dianalisis agar dapat memberikan informasi kepada pihak universitas dan calon mahasiswa mengenai tren peminatan serta mendorong pemerataan minat.

Permasalahan sebaran peminat ini memiliki implikasi pada efisiensi pendidikan tinggi dan perencanaan daya tampung. Jurusan yang selalu kelebihan atau kekurangan peminat dapat berdampak pada ketidakseimbangan sumber daya dan kesempatan kerja lulusan. Oleh karena itu, penting untuk memprediksi apakah suatu jurusan akan ramai atau sepi peminat dengan menggunakan pendekatan machine learning.

Beberapa riset sebelumnya juga telah membahas pemodelan peminatan jurusan berdasarkan data historis. Misalnya, penelitian oleh Hematang dkk (2023) [1] yang mengungkap bahwa algoritma random forest lebih unggul dalam memprediksi calon mahasiswa baru sehingga metode ini menjadi salah satu hipotesa saya dalam menyelesaikan masalah.

**Referensi**:
- [1] Hematang, A. K., Utami, N. W., & Paramitha, A. I. I. (2023). PERBANDINGAN MODEL PREDIKSI CALON MAHASISWA BARU MENGGUNAKAN ALGORITMA ID3 DAN RANDOM FOREST. JATI (Jurnal Mahasiswa Teknik Informatika), 7(6), 3427-3434.

## Business Understanding

### Problem Statements

* Bagaimana memprediksi apakah suatu jurusan IPS tergolong sepi atau ramai peminat?
* Algoritma machine learning mana yang memiliki performa terbaik dalam klasifikasi peminatan jurusan?

### Goals

* Menghasilkan model klasifikasi untuk menentukan apakah suatu jurusan tergolong "Sepi Peminat" atau "Ramai Peminat".
* Membandingkan performa model Random Forest dan Gaussian Naive Bayes dalam klasifikasi peminatan jurusan.

### Solution statements

* Membangun model baseline menggunakan algoritma Gaussian Naive Bayes dan Random Forest.
* Melakukan oversampling data minoritas dengan SMOTE untuk menangani ketidakseimbangan kelas.
* Memilih model dengan akurasi terbaik berdasarkan metrik evaluasi.

## Data Understanding

Dataset diperoleh dari hasil scraping situs [https://snpmb.bppp.kemdikbud.go.id/snbp/daftar-ptn-snbp](https://snpmb.bppp.kemdikbud.go.id/snbp/daftar-ptn-snbp) dan terdiri dari informasi jurusan IPS dengan total 2298 entri. 

### Variabel-variabel pada dataset jurusan IPS 
Variabel-variabel pada dataset adalah sebagai berikut:

* `KODE` : Kode jurusan
* `NAMA` : Nama jurusan
* `JENJANG` : Jenjang studi (Sarjana, Diploma)
* `DAYA TAMPUNG 2025` : Jumlah kuota jurusan untuk tahun 2025
* `PEMINAT 2024` : Jumlah peminat jurusan pada tahun 2024
* `JENIS PORTOFOLIO` : Kebutuhan portofolio atau tidak
* `JALUR` : Jalur masuk (SNBP, SNBT)
* `ASAL UNIV` : Nama universitas penyelenggara
* `PROSPEK KERJA` : Prospek pekerjaan lulusan
* `PROVINSI` : Lokasi universitas
* `RASIO KEKETATAN` : Persentase keketatan (peminat : daya tampung)
* `KATEGORI JURUSAN` : Target klasifikasi, yaitu "SEPI PEMINAT" atau "RAMAI PEMINAT"

## Visualisasi

### 1. Banyaknya Jurusan di Setiap Provinsi

**Provinsi dengan jumlah jurusan terbanyak**:

* Jawa Timur
* Jawa Tengah
* Jawa Barat
* DI Yogyakarta

**Provinsi dengan jumlah jurusan paling sedikit**:

* Kepulauan Bangka Belitung
* Bengkulu
* Kepulauan Riau

💡 *Insight*: Sebagian besar jurusan terkonsentrasi di Pulau Jawa, menandakan ketimpangan distribusi pendidikan tinggi secara geografis.

### 2. Distribusi Jumlah Daya Tampung Tahun 2025

* Jurusan dengan daya tampung kecil (≤100) mendominasi.
* Hanya sedikit jurusan yang memiliki daya tampung di atas 200.

💡 *Insight*: Kebanyakan jurusan membatasi kapasitas penerimaan mahasiswa, kemungkinan disebabkan keterbatasan fasilitas atau sumber daya pengajar.

### 3. Proporsi Jurusan Berdasarkan Jumlah Peminat

* 81% jurusan termasuk ramai peminat
* 19% jurusan tergolong sepi peminat

💡 *Insight*: Preferensi peserta didik sangat terpusat pada jurusan-jurusan tertentu, sehingga beberapa jurusan lain mengalami kekurangan peminat.

### Korelasi Fitur terhadap 'KATEGORI JURUSAN'

* PEMINAT 2024: 0.5015
* KODE: -0.4737
* ASAL UNIV: -0.3738
* PROVINSI: -0.3277
* RASIO KEKETATAN: -0.2756
* DAYA TAMPUNG 2025: 0.2361
* JENIS PORTOFOLIO: 0.1637
* JALUR: 0.1380
* NO: -0.1326
* PROSPEK KERJA: -0.1206
* NAMA: -0.0483
* JENJANG: 0.0137

## Data Preparation

Langkah-langkah data preparation yang dilakukan:

* **Penanganan kolom yang tidak dipakai**: Menghapus kolom aneh yang muncul tidak jelas seperti Unnamed: 13
* **Pengecekan data kosong dan Pembersihan data dari duplikasi**: Mengecek data yang bernilai null dan Menghapus data ganda agar model tidak bias terhadap entri yang berulang.
* **Encoding fitur kategorikal menggunakan LabelEncoder**: Mengubah data kategorikal menjadi numerik agar dapat diproses oleh algoritma machine learning.
* **Oversampling data minoritas dengan SMOTE**: Untuk mengatasi ketidakseimbangan kelas antara jurusan ramai dan sepi peminat, sehingga model tidak berat sebelah.
* **Pembagian data menjadi fitur (X) dan target (y)**: Memisahkan data input (fitur) dan output (label) untuk keperluan pelatihan model.
* **Normalisasi menggunakan MinMaxScaler**: Menyamakan skala antar fitur numerik agar model lebih stabil dan cepat belajar.
* **Pembagian data latih dan uji menggunakan stratified split (80:20)**: Menjamin distribusi kelas yang seimbang pada data latih dan uji, penting untuk menjaga akurasi dan generalisasi model.

SMOTE dilakukan karena distribusi label target tidak seimbang (jumlah data jurusan "Ramai Peminat" jauh lebih banyak).

## Modeling

Dua model yang digunakan:

* **Gaussian Naive Bayes**: model probabilistik sederhana dengan asumsi independensi antar fitur.
* **Random Forest Classifier**: algoritma ensemble berbasis decision tree yang mampu menangani data kategorikal dan numerik dengan baik.

Tuning dilakukan dengan default parameter terlebih dahulu untuk baseline. Kemudian dilakukan perbandingan dengan dan tanpa SMOTE.

Dua model yang digunakan:

### 1. Gaussian Naive Bayes

* **Kelebihan**: Cepat, efisien, bekerja baik pada dataset kecil, dan tidak terlalu sensitif terhadap overfitting.
* **Kekurangan**: Asumsi independensi antar fitur sering kali tidak terpenuhi, sehingga akurasi bisa lebih rendah pada data kompleks.

### 2. Random Forest Classifier

* **Kelebihan**: Mampu menangani data numerik dan kategorikal, kuat terhadap overfitting, dan memberikan performa yang stabil.
* **Kekurangan**: Lebih lambat dibandingkan model sederhana dan interpretabilitas lebih rendah dibanding pohon keputusan tunggal.

## Evaluation

### Model Random Forest tanpa SMOTE

```
Akurasi: 0.9652
              precision    recall  f1-score   support

           0       0.95      0.87      0.91        94
           1       0.97      0.99      0.98       366

    accuracy                           0.97       460
   macro avg       0.96      0.93      0.94       460
weighted avg       0.96      0.97      0.96       460
```

### Model Random Forest dengan SMOTE

```
Akurasi: 0.9879
              precision    recall  f1-score   support

           0       0.98      0.99      0.99       362
           1       0.99      0.98      0.99       383

    accuracy                           0.99       745
   macro avg       0.99      0.99      0.99       745
weighted avg       0.99      0.99      0.99       745
```

### Model Gaussian Naive Bayes dengan SMOTE

```
Akurasi: 0.8939
              precision    recall  f1-score   support

           0       0.86      0.93      0.89       362
           1       0.93      0.86      0.89       383

    accuracy                           0.89       745
   macro avg       0.90      0.89      0.89       745
weighted avg       0.90      0.89      0.89       745
```

### Metrik Evaluasi

#### Akurasi

Akurasi adalah proporsi prediksi yang benar terhadap seluruh data.

$\text{Akurasi} = \frac{TP + TN}{TP + TN + FP + FN}$

Cocok digunakan ketika distribusi kelas seimbang, namun dapat menyesatkan pada data tidak seimbang.

#### Precision

Precision mengukur seberapa banyak prediksi positif yang benar.

$\text{Precision} = \frac{TP}{TP + FP}$

Penting jika biaya kesalahan positif tinggi (false positive), misalnya memprediksi jurusan ramai padahal sepi.

#### Recall

Recall mengukur seberapa banyak kasus positif yang berhasil diprediksi dengan benar.

$\text{Recall} = \frac{TP}{TP + FN}$

Relevan ketika kita ingin menangkap semua jurusan sepi peminat agar tidak terabaikan.

#### F1 Score

F1 Score adalah rata-rata harmonis dari precision dan recall.

$\text{F1} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$

### Hasil Evaluasi Model

* **Random Forest + SMOTE**

  * Akurasi: **0.9879**
  * Precision, Recall, F1-Score: Hampir sempurna pada kedua kelas
  * ✅ Sangat baik dalam membedakan antara jurusan ramai dan sepi peminat.

* **Random Forest tanpa SMOTE**

  * Akurasi: **0.9652**
  * Recall kelas minoritas (jurusan sepi): hanya **0.87**
  * ⚠️ Belum optimal dalam menangkap jurusan sepi.

* **Gaussian Naive Bayes + SMOTE**

  * Akurasi: **0.8939**
  * F1-score seimbang di kedua kelas
  * ⚖️ Stabil tetapi kalah dalam performa dibanding Random Forest.
  
**Kesimpulan**:

* Penggunaan SMOTE terbukti meningkatkan performa model klasifikasi.
* Model Random Forest menunjukkan performa terbaik baik dari segi akurasi, precision, recall, dan f1-score.
* Gaussian Naive Bayes bekerja baik namun kalah unggul dari Random Forest dalam menangani kompleksitas fitur.
* Berdasarkan hasil evaluasi, model terbaik yang dipilih adalah **Random Forest dengan SMOTE dan tuning parameter**, karena memberikan generalisasi yang optimal dan skor evaluasi tertinggi.

---

*Catatan: Gambar, kode, atau visualisasi tambahan dapat ditambahkan sesuai kebutuhan.*



