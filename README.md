# Pembuatan Backup Otomatis Aman di Cloud Storage Gratis (Backblaze B2)

Proyek ini merupakan implementasi sistem backup otomatis yang mengamankan data dengan enkripsi AES sebelum mengunggahnya ke layanan cloud storage Backblaze B2. Proses backup dijalankan secara otomatis setiap hari pukul 13.00 menggunakan Windows Task Scheduler.

## Fitur Utama
- Pembuatan backup otomatis dalam format ZIP terenkripsi AES.
- Upload otomatis ke Backblaze B2.
- Pencatatan aktivitas backup ke file `backup.log`.
- Penjadwalan backup harian dengan Windows Task Scheduler.

## Kebutuhan Perangkat Lunak
- Python 3.11 atau yang lebih baru
- Windows Task Scheduler
- Akun Backblaze B2
- Paket Python sesuai `requirements.txt`

## Konfigurasi `.env`
Buat file `.env` pada direktori proyek dengan isi:

```env
B2_KEY_ID=your_key_id
B2_APPLICATION_KEY=your_application_key
B2_BUCKET_NAME=your_bucket_name
AES_PASSWORD=your_backup_password
```

## Menjalankan Backup Secara Manual

```bash
python backup.py
```

## Penjadwalan Otomatis
Buat tugas pada Windows Task Scheduler untuk menjalankan `backup.py` setiap hari pukul 13.00.

## Proses Restore
1. Unduh file backup dari Backblaze B2.
2. Buka file ZIP menggunakan aplikasi yang mendukung AES, seperti 7-Zip atau WinRAR.
3. Masukkan kata sandi backup.
4. Salin kembali file hasil ekstraksi ke lokasi yang diinginkan.

## Log
Riwayat proses backup tersimpan pada file `backup.log`.