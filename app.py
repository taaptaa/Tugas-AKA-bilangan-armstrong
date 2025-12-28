import streamlit as st
import time
import pandas as pd
import plotly.graph_objects as go
import random

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(page_title="Analisis Algoritma", layout="wide")
st.title("Analisis Bilangan Armstrong")
st.subheader("Perbandingan Iteratif vs Rekursif")

# =========================
# FUNGSI ITERATIF
# =========================
def hitung_iteratif(n):
    text_n = str(n)
    pangkat = len(text_n)
    hasil = 0
    
    for digit in text_n:
        hasil += int(digit) ** pangkat
        
    return hasil == n

# =========================
# FUNGSI REKURSIF
# =========================
def helper_rekursif(text_n, pangkat, index):
    # Base case: jika index sudah habis
    if index == len(text_n):
        return 0
    
    # Hitung digit saat ini + panggil fungsi untuk sisa digit
    nilai_sekarang = int(text_n[index]) ** pangkat
    return nilai_sekarang + helper_rekursif(text_n, pangkat, index + 1)

def hitung_rekursif(n):
    text_n = str(n)
    pangkat = len(text_n)
    total = helper_rekursif(text_n, pangkat, 0)
    return total == n

# =========================
# TAB NAVIGASI
# =========================
tab1, tab2 = st.tabs(["📊 Grafik Benchmark", "🔢 Cek Satu Angka"])

# =========================
# TAB 1: VISUALISASI GRAFIK
# =========================
with tab1:
    st.write("### Pengujian Kecepatan (Benchmark)")
    
    # Input User untuk Jumlah Data (N)
    # Default 500 agar tidak terlalu lama, tapi cukup untuk melihat bedanya
    max_data = st.number_input("Masukkan Jumlah Data Maksimal (N)", value=500, step=50)
    
    if st.button("🚀 Mulai Benchmark"):
        results = []
        # Tentukan langkah (step) agar titik di grafik tidak terlalu padat
        step = max(10, int(max_data / 10)) 
        
        # Progress Bar Sederhana
        bar = st.progress(0)
        status_text = st.empty()
        
        # Loop Pengujian dari data kecil ke besar
        # Range dibuat agar start dari 'step' sampai 'max_data'
        ranges = range(step, max_data + 1, step)
        
        for i, n in enumerate(ranges):
            # Update status dan progress bar
            status_text.text(f"Sedang memproses {n} data...")
            bar.progress((i + 1) / len(ranges))
            
            # Buat N bilangan acak (Dataset Ujian)
            # Menggunakan range 100-9999 agar beban hitungan cukup berat (3-4 digit)
            dataset = [random.randint(100, 9999) for _ in range(n)]
            
            # 1. Cek Waktu Iteratif
            start = time.perf_counter()
            for num in dataset:
                hitung_iteratif(num)
            waktu_iter = time.perf_counter() - start
            
            # 2. Cek Waktu Rekursif
            start = time.perf_counter()
            for num in dataset:
                hitung_rekursif(num)
            waktu_rec = time.perf_counter() - start
            
            # Simpan data
            results.append({
                "N": n,
                "Iteratif": waktu_iter,
                "Rekursif": waktu_rec
            })
            
        # Bersihkan tampilan progress
        bar.empty()
        status_text.text("Selesai! Menampilkan grafik...")
        time.sleep(0.5)
        status_text.empty()
        
        # Buat DataFrame
        df = pd.DataFrame(results)
        
        # --- MEMBUAT GRAFIK (PLOTLY) ---
        fig = go.Figure()
        
        # Garis Biru (Iteratif)
        fig.add_trace(go.Scatter(
            x=df["N"], y=df["Iteratif"],
            mode='lines+markers', name='Iteratif',
            # shape='spline' membuat garis melengkung halus
            line=dict(color='cyan', width=3, shape='spline') 
        ))
        
        # Garis Merah (Rekursif)
        fig.add_trace(go.Scatter(
            x=df["N"], y=df["Rekursif"],
            mode='lines+markers', name='Rekursif',
            # shape='spline' membuat garis melengkung halus
            line=dict(color='salmon', width=3, shape='spline')
        ))
        
        # Konfigurasi Layout Grafik
        fig.update_layout(
            title="Grafik Perbandingan Waktu Eksekusi",
            xaxis_title="Jumlah Data (N)",
            yaxis_title="Waktu (Detik)",
            template="plotly_dark", # Tema Gelap
            hovermode="x unified"   # Agar tooltip muncul rapi saat mouse lewat
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Kesimpulan Otomatis
        waktu_akhir_iter = df["Iteratif"].iloc[-1]
        waktu_akhir_rec = df["Rekursif"].iloc[-1]
        
        if waktu_akhir_iter < waktu_akhir_rec:
            st.success(f"✅ Kesimpulan: Pada N={max_data}, Algoritma Iteratif lebih cepat daripada Algoritma Rekursif.")
        else:
            st.warning(f"⚠️ Kesimpulan: Pada N={max_data}, Algoritma Rekursif lebih cepat daripada Algoritma Iteratif.")

# =========================
# TAB 2: CEK ANGKA TUNGGAL
# =========================
with tab2:
    st.write("### Cek Kebenaran Algoritma")
    st.info("Fitur ini untuk memastikan apakah bilangan tersebut merupakan bilangan armstrong atau tidak).")
    
    col_input, col_btn = st.columns([3, 1])
    with col_input:
        angka = st.number_input("Masukkan satu bilangan", min_value=0, value=153)
    with col_btn:
        st.write("") # Spacer
        st.write("") # Spacer
        tombol_cek = st.button("Cek Sekarang")
    
    if tombol_cek:
        # Hitung Iteratif
        t1 = time.perf_counter()
        hasil_iter = hitung_iteratif(angka)
        durasi_iter = time.perf_counter() - t1
        
        # Hitung Rekursif
        t2 = time.perf_counter()
        hasil_rec = hitung_rekursif(angka)
        durasi_rec = time.perf_counter() - t2
        
        # Tampilkan Hasil
        if hasil_iter:
            st.success(f"✅ Benar! {angka} adalah Bilangan Armstrong.")
        else:
            st.error(f"❌ Salah. {angka} Bukan Bilangan Armstrong.")
            
        st.write("---")
        # Menampilkan waktu eksekusi satuan (sangat kecil)
        col1, col2 = st.columns(2)
        col1.metric("Waktu Iteratif", f"{durasi_iter:.8f} s")
        col2.metric("Waktu Rekursif", f"{durasi_rec:.8f} s")