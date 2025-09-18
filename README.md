# 🖐💻 Shutdown Laptop with Hand Sensor

Proyek ini adalah aplikasi untuk **mematikan laptop menggunakan sensor tangan**.  
Dengan program ini, kamu bisa mematikan komputer tanpa menekan tombol atau klik menu, cukup dengan mendekatkan tangan pada sensor.

---

## 🚀 Fitur Utama
- ✅ **Deteksi Tangan Otomatis** – Menggunakan sensor (misalnya sensor ultrasonik atau kamera).
- ✅ **Shutdown Laptop Sekali Gerakan** – Tidak perlu klik tombol Start → Shutdown.
- ✅ **Mudah Dikustomisasi** – Bisa disesuaikan untuk Windows / Linux.
- ✅ **Kode Ringkas & Mudah Dipahami** – Cocok untuk pembelajaran.

---

## 🛠 Teknologi yang Digunakan
- **Python 3.9** – Bahasa pemrograman utama.
- **requirements.txt** – Berisi semua library yang dibutuhkan.
- **Virtual Environment (venv)** – Opsional, disarankan agar dependensi terisolasi.
- Sensor pendukung (misalnya **HC-SR04** jika menggunakan hardware).

## 📦 Instalasi & Menjalankan Program

Ikuti langkah-langkah berikut untuk menjalankan proyek ini:

```bash
# 1️⃣ Pastikan menggunakan Python 3.9
python --version
# Jika belum 3.9, install Python 3.9 dari https://www.python.org/downloads/release/python-390/

# 2️⃣ (Opsional) Buat Virtual Environment
python -m venv venv

# Aktivasi venv
# Windows:
venv\Scripts\activate
# Linux / Mac:
source venv/bin/activate

# 3️⃣ Install dependensi dari requirements.txt
pip install -r requirements.txt

# 4️⃣ Jalankan Program
python shutdown.py
