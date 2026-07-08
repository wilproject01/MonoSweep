#!/usr/bin/env python3
import os
import shutil
import sys
import hashlib
import textwrap
import time

# ==============================================================================
# [ KONFIGURASI KEAMANAN PRO ]
# ==============================================================================
# True  = File dianggap duplikat jika NAMANYA SAMA *DAN* ISINYA (MD5 HASH) SAMA PERSIS.
# False = File dianggap duplikat hanya berdasarkan PERSAMAAN NAMA FILE (Lebih cepat).
VERIFIKASI_ISI_FILE = False
# ==============================================================================

if sys.platform == "win32":
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except:
        pass

MENDUKUNG_RGB = True
if os.name == 'nt' and 'WT_SESSION' not in os.environ:
    MENDUKUNG_RGB = False
if os.environ.get('TERM') == 'dumb':
    MENDUKUNG_RGB = False

# --- KONSTANTA WARNA STANDAR ---
RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
MAGENTA = "\033[35m"
BLUE = "\033[34m"

def lebar_terminal():
    try:
        return shutil.get_terminal_size((100, 24)).columns
    except OSError:
        return 100


def potong_teks(teks, lebar=None):
    lebar = lebar or lebar_terminal()
    if lebar <= 0:
        return ""
    return teks[:max(1, lebar)]


def pembatas(karakter='=', lebar=None):
    lebar = lebar or lebar_terminal()
    lebar_aman = max(40, min(lebar, 120))
    return karakter * lebar_aman


def format_kolom(teks, lebar):
    teks = str(teks)
    if len(teks) > lebar:
        return textwrap.shorten(teks, width=lebar, placeholder='...')
    return teks.ljust(lebar)


def cetak_teks_responsif(teks, warna='', prefix='', lebar=None):
    lebar = max(30, min(100, (lebar or lebar_terminal()) - 2))
    isi = str(teks)
    for baris in textwrap.wrap(isi, width=lebar, break_long_words=False, break_on_hyphens=False):
        print(f"{warna}{prefix}{baris}{RESET}")


def cetak_gradasi(teks, rgb_awal, rgb_akhir, warna_fallback=CYAN):
    teks = potong_teks(teks, lebar_terminal())
    if not MENDUKUNG_RGB:
        sys.stdout.write(f"{BOLD}{warna_fallback}{teks}{RESET}\n")
        return
    r1, g1, b1 = rgb_awal
    r2, g2, b2 = rgb_akhir
    panjang = len(teks)
    if panjang <= 1:
        sys.stdout.write(teks + "\n")
        return
    for i, karakter in enumerate(teks):
        rasio = i / (panjang - 1)
        r = int(r1 + (r2 - r1) * rasio)
        g = int(g1 + (g2 - g1) * rasio)
        b = int(b1 + (b2 - b1) * rasio)
        sys.stdout.write(f"\033[38;2;{r};{g};{b}m{karakter}")
    sys.stdout.write(RESET + "\n")


def cetak_banner_gradasi(banner_list, rgb_awal, rgb_akhir, warna_fallback=CYAN):
    lebar = lebar_terminal()
    for baris in banner_list:
        baris = baris.rstrip()
        if len(baris) > lebar:
            baris = baris[:lebar]
        elif len(baris) < lebar:
            sisa = lebar - len(baris)
            baris = " " * (sisa // 2) + baris
        cetak_gradasi(baris, rgb_awal, rgb_akhir, warna_fallback)

def bersihkan_layar():
    os.system('cls' if os.name == 'nt' else 'clear')

# --- ASCII ART ---
BANNER_MENU_UTAMA = [
    "  ███╗   ███╗ ██████╗ ███╗   ██╗ ██████╗ ███████╗██╗    ██╗███████╗███████╗██████╗     ██╗   ██╗     ██████╗   ██╗",
    "  ████╗ ████║██╔═══██╗████╗  ██║██╔═══██╗██╔════╝██║    ██║██╔════╝██╔════╝██╔══██╗    ██║   ██║    ██╔═ ██╗   ██║",
    "  ██╔████╔██║██║   ██║██╔██╗ ██║██║   ██║███████╗██║ █╗ ██║█████╗  █████╗  ██████╔╝    ██║   ██║    ██║  ██║  ╚██║",
    "  ██║╚██╔╝██║██║   ██║██║╚██╗██║██║   ██║╚════██║██║███╗██║██╔══╝  ██╔══╝  ██╔═══╝     ╚██╗ ██╔╝    ██   ██║   ██║",
    "  ██║ ╚═╝ ██║╚██████╔╝██║ ╚████║╚██████╔╝███████║╚███╔███╔╝███████╗███████╗██║          ╚████╔╝     ╚████╔╝██╗ ██║",
    "  ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚══════╝ ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝           ╚═══╝       ╚═══╝ ╚═╝╚═╝"
]

BANNER_MERAPIKAN = [
    "  ███████╗██╗██╗      ███████╗     ██████╗ ██████╗  ██████╗  █████╗ ███╗   ██╗██╗███████╗███████╗██████╗ ",
    "  ██╔════╝██║██║      ██╔════╝    ██╔═══██╗██╔══██╗██╔════╝ ██╔══██╗████╗  ██║██║╚══███╔╝██╔════╝██╔══██╗",
    "  █████╗  ██║██║      █████╗      ██║   ██║██████╔╝██║  ███╗███████║██╔██╗ ██║██║  ███╔╝ █████╗  ██████╔╝",
    "  ██╔══╝  ██║██║      ██╔══╝      ██║   ██║██╔══██╗██║   ██║██╔══██║██║╚██╗██║██║ ███╔╝  ██╔══╝  ██╔══██╗",
    "  ██║     ██║███████╗ ███████╗    ╚██████╔╝██║  ██║╚██████╔╝██║  ██║██║ ╚████║██║███████╗███████╗██║  ██║",
    "  ╚═╝     ╚═╝╚══════╝ ╚══════╝     ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚══════╝╚══════╝╚═╝  ╚═╝"
]

BANNER_DUPLIKAT = [
    "  ██████╗ ██╗   ██╗██████╗ ██╗     ██╗██╗  ██╗ █████╗ ████████╗    ██████╗██╗     ███████╗ █████╗ ███╗   ██╗███████╗██████╗ ",
    "  ██╔══██╗██║   ██║██╔══██╗██║     ██║██║  ██║██╔══██╗╚══██╔══╝   ██╔════╝██║     ██╔════╝██╔══██╗████╗  ██║██╔════╝██╔══██╗",
    "  ██║  ██║██║   ██║██████╔╝██║     ██║███████║███████║   ██║      ██║     ██║     █████╗  ███████║██╔██╗ ██║█████╗  ██████╔╝",
    "  ██║  ██║██║   ██║██╔═══╝ ██║     ██║██╔══██║██╔══██║   ██║      ██║     ██║     ██╔══╝  ██╔══██║██║╚██╗██║██╔══╝  ██╔══██╗",
    "  ██████╔╝╚██████╔╝██║     ███████╗██║██║  ██║██║  ██║   ██║      ╚██████╗███████╗███████╗██║  ██║██║ ╚████║███████╗██║  ██║",
    "  ╚═════╝  ╚═════╝ ╚═╝     ╚══════╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝       ╚═════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝"
]

BANNER_TERIMAKASIH = [
    "  ████████╗███████╗██████╗ ██╗███╗   ███╗ █████╗ ██╗  ██╗ █████╗ ███████╗██╗██╗  ██╗",
    "  ╚══██╔══╝██╔════╝██╔══██╗██║████╗ ████║██╔══██╗██║  ██║██╔══██╗██╔════╝██║██║  ██║",
    "     ██║   █████╗  ██████╔╝██║██╔████╔██║███████║███████║███████║███████╗██║███████║",
    "     ██║   ██╔══╝  ██╔══██╗██║██║╚██╔╝██║██╔══██║██╔══██║██╔══██║╚════██║██║██╔══██║",
    "     ██║   ███████╗██║  ██║██║██║ ╚═╝ ██║██║  ██║██║  ██║██║  ██║███████║██║██║  ██║",
    "     ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝╚═╝  ╚═╝"
]

KATEGORI = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'],
    'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv'],
    'Documents': ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt'],
    'Archives': ['.zip', '.rar', '.7z'],
    'Audio': ['.mp3', '.wav', '.aac', '.flac']
}

def animasi_loading(pesan="Loading", durasi=4.5):
    sys.stdout.write("\033[?25l") 
    sys.stdout.flush()
    spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    akhir = time.time() + durasi
    i = 0
    while time.time() < akhir:
        sisa = akhir - time.time()
        persen = int(((durasi - sisa) / durasi) * 100)
        persen = min(persen, 100)
        lebar_bar = 20
        balok = int(persen / 100 * lebar_bar)
        bar = "█" * balok + "░" * (lebar_bar - balok)
        sys.stdout.write(f"\r{BOLD}{CYAN}[{spinner[i % len(spinner)]}] {pesan} {bar} {persen}%{RESET}")
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1
    sys.stdout.write("\r\033[K") 
    sys.stdout.write(f"{BOLD}{GREEN}[✓] {pesan} Selesai!{RESET}\n")
    sys.stdout.write("\033[?25h") 
    sys.stdout.flush()
    time.sleep(0.3)

def hitung_hash_file(jalur_file, ukuran_blok=65536):
    hasher = hashlib.md5()
    try:
        with open(jalur_file, 'rb') as f:
            blok = f.read(ukuran_blok)
            while len(blok) > 0:
                hasher.update(blok)
                blok = f.read(ukuran_blok)
        return hasher.hexdigest()
    except:
        return None

def tampilkan_menu_utama():
    bersihkan_layar()
    cetak_banner_gradasi(BANNER_MENU_UTAMA, (0, 255, 255), (255, 0, 255), MAGENTA)
    lebar = lebar_terminal()
    garis = pembatas('=', lebar)
    print(f"{BOLD}{CYAN}{garis}{RESET}")
    header = f"Github : wilproject01 | System Name : MonoSweep V.0.1 | Instagram : wilden_ofcl"
    print(f"{BOLD}{GREEN}{textwrap.shorten(header, width=max(30, lebar - 4), placeholder='...')}{RESET}")
    print(f"{BOLD}{CYAN}{garis}{RESET}")
    print(f"{BOLD}{YELLOW}  [ DAFTAR ISI PROGRAM ]{RESET}\n")
    print(f"  {BOLD}{CYAN}1.{RESET} Merapihkan File Otomatis")
    print(f"  {BOLD}{CYAN}2.{RESET} Menghapus File Duplicate Otomatis")
    print(f"  {BOLD}3.{RESET} Exit (Keluar dari program)")
    print(f"{BOLD}{CYAN}{garis}{RESET}")

def menu_merapikan_file():
    bersihkan_layar()
    cetak_banner_gradasi(BANNER_MERAPIKAN, (0, 255, 255), (0, 255, 128), CYAN)
    print(f"{BOLD}{CYAN}{pembatas('=', lebar_terminal())}{RESET}")
    
    direktori_target = os.path.dirname(os.path.abspath(__file__))
    nama_skrip_ini = os.path.basename(os.path.abspath(__file__))
    
    print(f"{BOLD}Target Direktori (Dinamis):{RESET}")
    cetak_teks_responsif(direktori_target, warna=YELLOW)
    
    pilihan = input(f"\n{BOLD}{YELLOW}[?] Jalankan proses merapikan file? (y/n): {RESET}").strip().lower()
    if pilihan not in ['y', 'yes']:
        print(f"\n{RED}[!] Fitur dibatalkan. Kembali ke menu utama...{RESET}")
        time.sleep(1.2)
        return

    print()
    animasi_loading("Menganalisis Ekstensi File", 1.2)

    lebar = max(50, lebar_terminal())
    lebar_nama = max(18, min(36, lebar // 2))
    lebar_kategori = max(10, min(14, lebar // 5))
    lebar_status = max(16, lebar - lebar_nama - lebar_kategori - 8)
    header = f"{format_kolom('Nama File', lebar_nama)} | {format_kolom('Kategori', lebar_kategori)} | {format_kolom('Log Status', lebar_status)}"
    print(f"{BOLD}{header}{RESET}")
    print("-" * min(lebar, 120))

    terpindah, dilewati = 0, 0

    for item in os.listdir(direktori_target):
        jalur_item = os.path.join(direktori_target, item)
        if os.path.isfile(jalur_item):
            if item == nama_skrip_ini:
                continue
            _, ekstensi = os.path.splitext(item)
            ekstensi = ekstensi.lower()
            folder_tujuan = 'Others'
            for kat, list_ekstensi in KATEGORI.items():
                if ekstensi in list_ekstensi:
                    folder_tujuan = kat
                    break
            jalur_folder_tujuan = os.path.join(direktori_target, folder_tujuan)
            if not os.path.exists(jalur_folder_tujuan):
                os.makedirs(jalur_folder_tujuan)
                print(f"{format_kolom(f'Folder [{folder_tujuan}]', lebar_nama)} | {format_kolom('Sistem', lebar_kategori)} | {CYAN}[+] Folder Baru{RESET}")
            tujuan_akhir_file = os.path.join(jalur_folder_tujuan, item)
            if os.path.exists(tujuan_akhir_file):
                print(f"{format_kolom(item, lebar_nama)} | {format_kolom(folder_tujuan, lebar_kategori)} | {YELLOW}[!] Dilewati (Eksis){RESET}")
                dilewati += 1
            else:
                try:
                    shutil.move(jalur_item, tujuan_akhir_file)
                    print(f"{format_kolom(item, lebar_nama)} | {format_kolom(folder_tujuan, lebar_kategori)} | {GREEN}[✓] Sukses Pindah{RESET}")
                    terpindah += 1
                except Exception as e:
                    print(f"{format_kolom(item, lebar_nama)} | {format_kolom(folder_tujuan, lebar_kategori)} | {RED}[❌] Gagal: {str(e)[:10]}{RESET}")
                    dilewati += 1

    print(f"\n{BOLD}Total Berhasil Dipindahkan: {GREEN}{terpindah}{RESET} | Dilewati: {YELLOW}{dilewati}{RESET}")
    input(f"{BOLD}\nTekan Enter untuk kembali ke menu utama...{RESET}")

def menu_hapus_duplikat():
    bersihkan_layar()
    cetak_banner_gradasi(BANNER_DUPLIKAT, (255, 255, 0), (255, 0, 0), YELLOW)
    print(f"{BOLD}{YELLOW}{pembatas('=', lebar_terminal())}{RESET}")
    
    direktori_aktif = os.path.dirname(os.path.abspath(__file__))
    nama_skrip_ini = os.path.basename(os.path.abspath(__file__))
    
    print(f"{BOLD}Target Direktori:{RESET}")
    cetak_teks_responsif(direktori_aktif, warna=YELLOW)
    
    if VERIFIKASI_ISI_FILE:
        print(f"{BOLD}{CYAN}[Mode Keamanan] Verifikasi Konten Aktif (Nama Sama & MD5 Checksum Harus Sama Persis).{RESET}")
    else:
        print(f"{BOLD}{BLUE}[Mode Keamanan] Verifikasi Cepat Aktif (Deteksi Duplikasi Berdasarkan Persamaan Nama File).{RESET}")
        
    pilihan = input(f"\n{BOLD}{RED}[!] PERINGATAN: File duplikat akan langsung dieliminasi. Lanjutkan? (y/n): {RESET}").strip().lower()
    if pilihan not in ['y', 'yes']:
        print(f"\n{RED}[!] Fitur dibatalkan demi keamanan. Kembali ke menu utama...{RESET}")
        time.sleep(1.2)
        return

    print()
    animasi_loading("Memindai Map Struktur File", 1.5)

    lebar = max(50, lebar_terminal())
    lebar_nama = max(18, min(36, lebar // 2))
    lebar_ukuran = max(8, min(12, lebar // 8))
    lebar_status = max(16, lebar - lebar_nama - lebar_ukuran - 8)
    header = f"{format_kolom('Nama File Duplikat', lebar_nama)} | {format_kolom('Ukuran', lebar_ukuran)} | {format_kolom('Log Status', lebar_status)}"
    print(f"{BOLD}{header}{RESET}")
    print("-" * min(lebar, 120))

    catatan_file_unik = set() if not VERIFIKASI_ISI_FILE else {}
    terhapus = 0
    total_file_diperiksa = 0

    for root, _, files in os.walk(direktori_aktif):
        for item in files:
            if item == nama_skrip_ini:
                continue
                
            jalur_lengkap = os.path.join(root, item)
            total_file_diperiksa += 1
            
            if VERIFIKASI_ISI_FILE:
                hash_file = hitung_hash_file(jalur_lengkap)
                if hash_file:
                    kunci_file = (item, hash_file)
                    if kunci_file in catatan_file_unik:
                        try:
                            ukuran_kb = os.path.getsize(jalur_lengkap) / 1024
                            os.remove(jalur_lengkap)
                            print(f"{format_kolom(item, lebar_nama)} | {format_kolom(f'{ukuran_kb:.1f} KB', lebar_ukuran)} | {RED}[🗑️] Terhapus (Isi Identik){RESET}")
                            terhapus += 1
                        except:
                            print(f"{format_kolom(item, lebar_nama)} | {format_kolom('-- KB', lebar_ukuran)} | {YELLOW}[!] Gagal Hapus{RESET}")
                    else:
                        catatan_file_unik[kunci_file] = jalur_lengkap
            else:
                if item in catatan_file_unik:
                    try:
                        ukuran_kb = os.path.getsize(jalur_lengkap) / 1024
                        os.remove(jalur_lengkap)
                        print(f"{format_kolom(item, lebar_nama)} | {format_kolom(f'{ukuran_kb:.1f} KB', lebar_ukuran)} | {RED}[🗑️] Terhapus (Nama Sama){RESET}")
                        terhapus += 1
                    except:
                        print(f"{format_kolom(item, lebar_nama)} | {format_kolom('-- KB', lebar_ukuran)} | {YELLOW}[!] Gagal Hapus{RESET}")
                else:
                    catatan_file_unik.add(item)

    print(f"\n{BOLD}Total File Diperiksa        : {CYAN}{total_file_diperiksa}{RESET}")
    print(f"{BOLD}Total File Duplikat Dihapus : {GREEN}{terhapus}{RESET}")
    input(f"{BOLD}\nTekan Enter untuk kembali ke menu utama...{RESET}")

def proses_exit():
    print()
    animasi_loading("Menutup Semua Sesi & Engine", 1.0)
    sys.stdout.write("\033[H\033[2J")
    sys.stdout.flush()
    bersihkan_layar()
    
    cetak_banner_gradasi(BANNER_TERIMAKASIH, (0, 255, 0), (0, 255, 255), GREEN)
    garis = pembatas('=', lebar_terminal())
    print(f"{BOLD}{CYAN}{garis}{RESET}")
    print(f"{BOLD}{YELLOW}  SCRIPT BY WILDEN.{RESET}")
    print(f"  SALAM HANGAT DARI KU UNTUK MU....")
    print(f"{BOLD}{CYAN}{garis}{RESET}\n")
    sys.exit(0)

def main():
    bersihkan_layar()
    print(f"{BOLD}{CYAN}Membuka Sistem MonoSweep V.0.1...{RESET}")
    animasi_loading("Menginisialisasi Program..", 1.0)
    
    while True:
        tampilkan_menu_utama()
        pilihan = input(f"{BOLD}{YELLOW}[?] Pilih nomor menu (1-3): {RESET}").strip()
        
        if pilihan == '1':
            print()
            animasi_loading("Membuka Modul File Organizer", 0.8)
            menu_merapikan_file()
        elif pilihan == '2':
            print()
            animasi_loading("Membuka Modul Duplicate Cleaner", 0.8)
            menu_hapus_duplikat()
        elif pilihan == '3':
            proses_exit()
        else:
            print(f"\n{RED}[!] Pilihan tidak valid! Silakan masukkan angka 1, 2, atau 3.{RESET}")
            time.sleep(1.2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
        bersihkan_layar()
        print(f"\n{BOLD}{RED}[!] Program dihentikan paksa.{RESET}\n")
        sys.exit(0)