import streamlit as st
import time
import pandas as pd
import plotly.graph_objects as go
import random

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="Analisis Algoritma Armstrong", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# SIDEBAR: TEORI & PENJELASAN
# ==========================================
with st.sidebar:
    st.header("📚 Teori Singkat")
    
    st.subheader("Apa itu Bilangan Armstrong?")
    st.markdown("""
    Bilangan Armstrong (atau Narcissistic Number) adalah bilangan yang jumlah pangkat dari digit-digitnya sama dengan bilangan itu sendiri.
    
    **Contoh: 153 (3 digit)**
    $$1^3 + 5^3 + 3^3 = 1 + 125 + 27 = 153$$
    
    **Contoh: 1634 (4 digit)**
    $$1^4 + 6^4 + 3^4 + 4^4 = 1634$$
    """)
    
    st.divider()
    
    st.subheader("Tentang Algoritma")
    st.markdown("""
    **1. Iteratif (Looping)**
    Menggunakan perulangan `for` biasa untuk memecah digit dan menghitung pangkat. Biasanya lebih hemat memori.
    
    **2. Rekursif**
    Fungsi memanggil dirinya sendiri (*self-calling*) untuk setiap digit. Metode ini elegan tapi memakan memori (*stack*) lebih banyak.
    """)
    
    st.info("Dibuat untuk Tugas Besar Analisis Kompleksitas Algoritma.")

# ==========================================
# HEADER & JUDUL UTAMA
# ==========================================
st.title("🧪 Analisis Kompleksitas Algoritma")
st.markdown("""
### Studi Kasus: Penentuan Bilangan Armstrong
Aplikasi ini dirancang untuk membandingkan performa dua pendekatan algoritma yaitu Algoritma Iteratif dan Rekursif
dalam menyelesaikan masalah matematika yang sama. 

Di sini kita akan membuktikan teori **Time Complexity** secara visual melalui pengujian nyata.
""")

# =========================
# FUNGSI ALGORITMA
# =========================
# --- ITERATIF ---
def hitung_iteratif(n):
    text_n = str(n)
    pangkat = len(text_n)
    hasil = 0
    for digit in text_n:
        hasil += int(digit) ** pangkat
    return hasil == n

# --- REKURSIF ---
def helper_rekursif(text_n, pangkat, index):
    if index == len(text_n):
        return 0
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
st.write("---")
tab1, tab2 = st.tabs(["📊 Grafik Benchmark (Analisis)", "🔢 Cek Angka (Demonstrasi)"])

# =========================
# TAB 1: VISUALISASI GRAFIK
# =========================
with tab1:
    st.header("⏱️ Pengujian Kecepatan (Benchmark)")
    
    # Penjelasan agar user paham tujuannya
    st.info("""
    **Apa tujuan fitur ini?**
    Fitur ini melakukan *Stress Test* (Uji Beban). Komputer akan diminta mengerjakan ribuan soal Armstrong secara acak.
    
    Kita akan melihat **siapa yang lebih cepat lelah (lambat)** saat jumlah data (N) semakin banyak. 
    Ini adalah representasi visual dari **Big-O Notation**.
    """)
    
    col_set, col_spacer = st.columns([1, 2])
    with col_set:
        max_data = st.number_input("Masukkan Jumlah Sampel Data (N)", value=500, step=100, help="Semakin besar angka, semakin lama prosesnya.")
    
    if st.button("🚀 Mulai Analisis Benchmark"):
        results = []
        step = max(10, int(max_data / 10)) 
        
        # UI Progress
        progress_text = "Operasi sedang berjalan. Mohon tunggu..."
        my_bar = st.progress(0, text=progress_text)
        
        # Loop Range
        ranges = range(step, max_data + 1, step)
        
        for i, n in enumerate(ranges):
            # Update bar
            my_bar.progress((i + 1) / len(ranges), text=f"Memproses {n} data acak...")
            
            # Generate Soal Ujian (Random Numbers)
            dataset = [random.randint(100, 9999) for _ in range(n)]
            
            # Ukur Iteratif
            start = time.perf_counter()
            for num in dataset:
                hitung_iteratif(num)
            waktu_iter = time.perf_counter() - start
            
            # Ukur Rekursif
            start = time.perf_counter()
            for num in dataset:
                hitung_rekursif(num)
            waktu_rec = time.perf_counter() - start
            
            results.append({"N": n, "Iteratif": waktu_iter, "Rekursif": waktu_rec})
            
        my_bar.empty()
        
        # Data & Grafik
        df = pd.DataFrame(results)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["N"], y=df["Iteratif"], mode='lines+markers', name='Iteratif', line=dict(color='#00CC96', width=3, shape='spline')))
        fig.add_trace(go.Scatter(x=df["N"], y=df["Rekursif"], mode='lines+markers', name='Rekursif', line=dict(color='#EF553B', width=3, shape='spline')))
        
        fig.update_layout(
            title="Grafik Perbandingan Running Time (Detik)",
            xaxis_title="Jumlah Data Input (N)",
            yaxis_title="Waktu Eksekusi (Detik)",
            template="plotly_dark",
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Kesimpulan
        w_iter = df["Iteratif"].iloc[-1]
        w_rec = df["Rekursif"].iloc[-1]
        winner = "Iteratif" if w_iter < w_rec else "Rekursif"
        
        st.success(f"""
        **Kesimpulan Akhir:** Pada pengujian dengan **N = {max_data}**, Algoritma **{winner}** terbukti lebih efisien.
        (Iteratif: {w_iter:.4f}s vs Rekursif: {w_rec:.4f}s)
        """)

# =========================
# TAB 2: CEK ANGKA TUNGGAL
# =========================
with tab2:
    st.header("🔍 Cek Kebenaran Algoritma")
    st.markdown("""
    Fitur ini digunakan untuk **memverifikasi logika** kode program. Sebelum melakukan benchmark besar-besaran, 
    kita harus memastikan bahwa algoritma Iteratif maupun Rekursif menghasilkan jawaban yang **BENAR**.
    """)
    
    col_input, col_btn = st.columns([3, 1])
    with col_input:
        angka = st.number_input("Masukkan satu bilangan bulat", min_value=0, value=153)
    with col_btn:
        st.write("")
        st.write("")
        tombol_cek = st.button("Cek Sekarang")
    
    if tombol_cek:
        # Proses
        t1 = time.perf_counter()
        valid_iter = hitung_iteratif(angka)
        d_iter = time.perf_counter() - t1
        
        t2 = time.perf_counter()
        valid_rec = hitung_rekursif(angka)
        d_rec = time.perf_counter() - t2
        
        # Tampilan Hasil
        if valid_iter:
            st.success(f"✅ **HASIL: BENAR!** Angka {angka} adalah Bilangan Armstrong.")
            st.write(f"Bukti: Penjumlahan pangkat digitnya menghasilkan {angka}.")
        else:
            st.error(f"❌ **HASIL: BUKAN.** Angka {angka} bukan Bilangan Armstrong.")
            st.write("Karena jumlah pangkat digitnya tidak sama dengan bilangan aslinya.")
            
        st.divider()
        st.caption("Detail Waktu Eksekusi (Sangat cepat karena hanya 1 data):")
        c1, c2 = st.columns(2)
        c1.metric("⏱️ Waktu Iteratif", f"{d_iter:.8f} s")
        c2.metric("⏱️ Waktu Rekursif", f"{d_rec:.8f} s")