import customtkinter as ctk  # Mengimpor modul customtkinter untuk antarmuka pengguna kustom
from tkinter import filedialog, messagebox  # Mengimpor modul tkinter untuk dialog file dan messagebox
from Crypto.Cipher import DES  # Mengimpor modul DES dari pustaka Crypto untuk enkripsi dan dekripsi DES
from Crypto.Util.Padding import pad, unpad  # Mengimpor fungsi pad dan unpad untuk padding data
import os  # Mengimpor modul os untuk operasi sistem
import time  # Mengimpor modul time untuk pengukuran waktu
import cv2  # Mengimpor modul cv2 untuk pemutaran video
from threading import Thread  # Mengimpor kelas Thread untuk pemutaran video dalam thread terpisah

class VideoEncryptorApp:
    def __init__(self, master):
        """
        Inisialisasi aplikasi Video Encryptor Decryption menggunakan DES Algorithm.

        Parameters:
        master (Tk): Instance utama dari Tkinter sebagai master window.
        """
        self.master = master
        self.master.title("Video Encryption Decryption Using DES Algorithm")  # Mengatur judul jendela utama
        self.master.geometry("700x400")  # Mengatur ukuran jendela utama

        # Cobakan mengatur tema kustom, gunakan tema default jika tidak ditemukan
        try:
            ctk.set_default_color_theme(r"c:\pykripto\MoonLitSky.json")
        except FileNotFoundError:
            print("Peringatan: File tema tidak ditemukan. Menggunakan tema default.")
            ctk.set_default_color_theme("green")  # Contoh menggunakan tema default yang terdaftar

        # Inisialisasi path untuk video yang dipilih
        self.input_video_path = ""

        # Setup antarmuka pengguna
        self.setup_ui()

    def setup_ui(self):
        """
        Menyiapkan antarmuka pengguna (UI) aplikasi dengan menambahkan tombol-tombol,
        label, dan frame-frame yang diperlukan.
        """
        # Frame untuk tombol 'Browse'
        frame = ctk.CTkFrame(self.master)
        frame.pack(pady=10, padx=5)

        browse_button = ctk.CTkButton(frame, text="( + ) Pilih Video", command=self.browse_video, width=626, height=70)
        browse_button.grid(row=1, column=0, columnspan=3, padx=6, pady=5, sticky='ew')

        self.input_video_label = ctk.CTkLabel(frame, text="Video Terpilih: Tidak Ada")
        self.input_video_label.grid(row=2, column=0, columnspan=3, padx=6, pady=5)

        # Frame untuk tombol dan input kunci
        button_frame = ctk.CTkFrame(self.master)
        button_frame.pack(pady=10, padx=10)

        key_label = ctk.CTkLabel(button_frame, text="Kunci (8 karakter):")
        key_label.grid(row=0, column=0, columnspan=1, padx=5, pady=5)
        self.key_entry = ctk.CTkEntry(button_frame)
        self.key_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky='ew')

        encryption_button = ctk.CTkButton(button_frame, text="Enkripsi", command=self.encrypt_video, width=256)
        encryption_button.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

        decryption_button = ctk.CTkButton(button_frame, text="Dekripsi", command=self.decrypt_video, width=256)
        decryption_button.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        reset_button = ctk.CTkButton(button_frame, text="Reset", command=self.reset, fg_color="#D03F2C", hover_color="lightcoral", width=100)
        reset_button.grid(row=1, column=2, padx=5, pady=5)

        # Frame untuk pemutaran video
        video_frame = ctk.CTkFrame(self.master)
        video_frame.pack(pady=10, padx=10)

        self.play_button = ctk.CTkButton(video_frame, text="Putar Video", command=self.play_video, width=256)
        self.play_button.pack(pady=10)

    def play_video(self):
        """
        Memulai pemutaran video yang dipilih dalam jendela baru.
        """
        if not self.input_video_path:
            messagebox.showerror("Error", "Silakan pilih video terlebih dahulu!")
            return

        # Buat jendela baru untuk pemutaran video
        self.video_window = ctk.CTk()
        self.video_window.title("Pemutaran Video")
        self.video_window.geometry("800x600")

        # Muat dan putar video dalam thread terpisah
        video_thread = Thread(target=self.load_and_play_video)
        video_thread.start()

    def load_and_play_video(self):
        """
        Memuat dan memutar video yang dipilih menggunakan OpenCV.
        """
        try:
            cap = cv2.VideoCapture(self.input_video_path)
            if not cap.isOpened():
                messagebox.showerror("Error", "Gagal membuka file video.")
                return

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                cv2.imshow("Video", frame)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()

        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat memutar video: {e}")

    def encrypt_video(self):
        """
        Mengenkripsi video yang dipilih menggunakan algoritma DES dan menyimpan hasilnya.
        """
        key = self.key_entry.get()
        if len(key) != 8:
            messagebox.showerror("Error", "Kunci harus terdiri dari 8 karakter!")
            return
        if not self.input_video_path:
            messagebox.showerror("Error", "Silakan pilih video terlebih dahulu!")
            return
        try:
            with open(self.input_video_path, 'rb') as file:
                plaintext = file.read()

            # Mengukur waktu mulai enkripsi
            start_time = time.time()

            # Membuat objek DES dengan kunci yang dienkripsi dan mode CBC
            des = DES.new(key.encode('utf-8'), DES.MODE_CBC)
            iv = des.iv  # Mendapatkan IV (Initialization Vector) dari objek DES
            padded_text = pad(plaintext, DES.block_size)  # Padding teks plaintext agar sesuai dengan block size DES
            encrypted_text = des.encrypt(padded_text)  # Melakukan enkripsi menggunakan DES
            encoded_text = iv + encrypted_text  # Menggabungkan IV dengan teks terenkripsi

            # Menyimpan teks terenkripsi ke file dengan ekstensi yang sama dengan file asli
            output_path = os.path.splitext(self.input_video_path)[0] + '_terenkripsi' + os.path.splitext(self.input_video_path)[1]
            with open(output_path, 'wb') as file:
                file.write(encoded_text)

            # Menghitung ukuran file terenkripsi
            encrypted_size = os.path.getsize(output_path)
            encrypted_size_kb = encrypted_size / 1024  # Ukuran dalam kilobyte

            # Mengukur waktu selesai enkripsi
            end_time = time.time()
            duration = end_time - start_time

            # Menampilkan pesan sukses dengan informasi tambahan
            messagebox.showinfo("Sukses", f"Video terenkripsi disimpan sebagai {output_path}\n\nWaktu: {duration:.4f} detik\nUkuran: {encrypted_size_kb:.2f} KB")
        except Exception as e:
            # Menampilkan pesan error jika terjadi kesalahan
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

    def decrypt_video(self):
        """
        Mendekripsi video yang dipilih menggunakan algoritma DES dan menyimpan hasilnya.
        """
        key = self.key_entry.get()
        if len(key) != 8:
            messagebox.showerror("Error", "Kunci harus terdiri dari 8 karakter!")
            return
        if not self.input_video_path:
            messagebox.showerror("Error", "Silakan pilih video terlebih dahulu!")
            return
        try:
            with open(self.input_video_path, 'rb') as file:
                encrypted_text = file.read()

            # Mengukur waktu mulai dekripsi
            start_time = time.time()

            iv = encrypted_text[:DES.block_size]  # Mengambil IV dari teks terenkripsi
            ciphertext = encrypted_text[DES.block_size:]  # Mengambil teks terenkripsi setelah IV
            des = DES.new(key.encode('utf-8'), DES.MODE_CBC, iv)  # Membuat objek DES dengan kunci dan IV
            padded_text = des.decrypt(ciphertext)  # Mendekripsi teks terenkripsi
            plaintext = unpad(padded_text, DES.block_size)  # Menghapus padding dari teks terdekripsi

            # Menyimpan teks terdekripsi ke file dengan ekstensi yang sama dengan file asli
            output_path = os.path.splitext(self.input_video_path)[0] + '_terdekripsi' + os.path.splitext(self.input_video_path)[1]
            with open(output_path, 'wb') as file:
                file.write(plaintext)

            # Menghitung ukuran file terdekripsi
            decrypted_size = os.path.getsize(output_path)
            decrypted_size_kb = decrypted_size / 1024  # Ukuran dalam kilobyte

            # Mengukur waktu selesai dekripsi
            end_time = time.time()
            duration = end_time - start_time

            # Menampilkan pesan sukses dengan informasi tambahan
            messagebox.showinfo("Sukses", f"Video terdekripsi disimpan sebagai {output_path}\n\nWaktu: {duration:.4f} detik\nUkuran: {decrypted_size_kb:.2f} KB")
        except ValueError as ve:
            # Menampilkan pesan error jika terjadi kesalahan dekripsi
            messagebox.showerror("Error", f"Terjadi kesalahan dekripsi: {ve}")
        except Exception as e:
            # Menampilkan pesan error jika terjadi kesalahan lainnya
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

    def browse_video(self):
        """
        Membuka dialog untuk memilih video yang akan dienkripsi atau didekripsi.
        """
        file_path = filedialog.askopenfilename(filetypes=[("File video", "*.mp4 *.avi *.mov *.bin")])
        if file_path:
            self.input_video_path = file_path
            self.input_video_label.configure(text=f"Video Terpilih: {os.path.basename(self.input_video_path)}")

    def reset(self):
        """
        Mengembalikan antarmuka pengguna ke kondisi awal dengan menghapus pilihan video
        dan mengosongkan input kunci.
        """
        self.input_video_label.configure(text='Video Terpilih: Tidak Ada')
        self.input_video_path = ""
        self.key_entry.delete(0, 'end')

# Inisialisasi aplikasi jika dijalankan sebagai script utama
if __name__ == "__main__":
    root = ctk.CTk()
    app = VideoEncryptorApp(root)
    root.mainloop()