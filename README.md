# MonoSweep

MonoSweep adalah program berbasis terminal (CLI) yang dirancang untuk membantu Anda mengatur file-file di dalam suatu folder secara otomatis. Program ini cocok digunakan untuk membersihkan folder kerja, folder unduhan, atau direktori yang berisi banyak file dengan berbagai ekstensi.

<img width="922" height="494" alt="tampilan1" src="https://github.com/user-attachments/assets/b42e8c4d-841d-47fc-b877-1d2a807d729f" />


<img width="920" height="491" alt="tampilan2" src="https://github.com/user-attachments/assets/f4d80b56-5bf3-45e4-b038-efd6c494bc2e" />


<img width="926" height="488" alt="tampilan3" src="https://github.com/user-attachments/assets/84b1352f-2b85-4fb3-a79d-7a0f8a389385" />


## Apa yang dapat dilakukan program ini?

MonoSweep memiliki dua fitur utama:

1. Merapikan File Otomatis
   - Mengelompokkan file berdasarkan kategori ekstensi.
   - File akan dipindahkan ke folder seperti:
     - Images
     - Videos
     - Documents
     - Archives
     - Audio
     - Others

2. Menghapus File Duplikat Otomatis
   - Mencari file yang memiliki nama yang sama.
   - Jika mode verifikasi isi aktif, program juga memeriksa konten file menggunakan hash MD5.
   - File duplikat akan dihapus secara permanen setelah konfirmasi pengguna.

## Fitur Tambahan

- Antarmuka menu yang sederhana dan mudah dipahami.
- Terdapat animasi loading dan banner visual saat program berjalan.
- Program berjalan lintas platform (Windows, Linux, macOS).

## Persyaratan

- Python 3.x

## Cara Menjalankan

Buka terminal, lalu masuk ke folder project, kemudian jalankan perintah berikut:

```bash
python3 MonoSweep.py
```

Setelah itu pilih menu yang tersedia:
- 1: Merapihkan file otomatis
- 2: Menghapus file duplikat otomatis
- 3: Keluar dari program

## Catatan Penting

- Program akan memproses file di direktori tempat file skrip ini berada.
- Fitur penghapusan duplikat bersifat permanen, jadi pastikan Anda telah memeriksa file sebelum melanjutkan.
- Program ini dibuat untuk membantu manajemen file secara cepat dan praktis.


## Lisensi Hak Cipta

Hak cipta © 2026 Wilden Widya Is Nanda. Seluruh hak cipta dilindungi undang-undang.
Program ini hanya boleh digunakan, disalin, dimodifikasi, dan didistribusikan dengan izin dari pembuat.
