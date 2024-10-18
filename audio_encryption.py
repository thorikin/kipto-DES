import customtkinter as ctk  # Mengimpor pustaka customtkinter sebagai ctk untuk membuat antarmuka grafis
from tkinter import filedialog, messagebox  # Mengimpor modul filedialog dan messagebox dari tkinter
from Crypto.Cipher import DES  # Mengimpor kelas DES dari pustaka Crypto untuk enkripsi dan dekripsi
from Crypto.Util.Padding import pad, unpad  # Mengimpor fungsi pad dan unpad dari Crypto untuk penanganan padding
import os  # Mengimpor pustaka os untuk operasi file dan sistem
import time  # Mengimpor pustaka time untuk mengukur waktu eksekusi

class EncryptionAudioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Encryption Decryption")  # Mengatur judul jendela utama
        self.root.geometry("660x525")  # Mengatur ukuran jendela utama
        self.input_file_path = None  # Variabel untuk menyimpan jalur file yang dipilih

        ctk.set_default_color_theme("green")  # Mengatur tema warna default menjadi hijau

        # Menyiapkan komponen antarmuka pengguna
        self.setup_ui()

    def setup_ui(self):
        frame = ctk.CTkFrame(self.root)  # Membuat frame untuk komponen UI
        frame.pack(pady=10, padx=5)  # Menempatkan frame dengan padding

        browse_button = ctk.CTkButton(frame, text="( + ) Browse File", command=self.browse_file, width=626, height=70)
        browse_button.grid(row=1, column=0, columnspan=3, padx=6, pady=5, sticky='ew')  # Menempatkan tombol browse dengan padding

        self.input_file_label = ctk.CTkLabel(frame, text="Selected File: None")
        self.input_file_label.grid(row=2, column=0, columnspan=3, padx=6, pady=5)  # Menempatkan label untuk menampilkan file yang dipilih

        button_frame = ctk.CTkFrame(self.root)
        button_frame.pack(pady=10, padx=10)  # Menempatkan frame untuk tombol dengan padding

        key_label = ctk.CTkLabel(button_frame, text="NIM (10 digits):")
        key_label.grid(row=0, column=0, columnspan=1, padx=5, pady=5)  # Menempatkan label untuk input kunci
        self.key_entry = ctk.CTkEntry(button_frame)
        self.key_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky='ew')  # Menempatkan input kunci dengan padding

        encryption_button = ctk.CTkButton(button_frame, text="Encryption", command=self.encrypt_file, width=256)
        encryption_button.grid(row=1, column=0, padx=5, pady=5, sticky='ew')  # Menempatkan tombol enkripsi dengan padding

        decryption_button = ctk.CTkButton(button_frame, text="Decryption", command=self.decrypt_file, width=256)
        decryption_button.grid(row=1, column=1, padx=5, pady=5, sticky='ew')  # Menempatkan tombol dekripsi dengan padding

        reset_button = ctk.CTkButton(button_frame, text="Reset", command=self.reset, fg_color="#D03F2C", hover_color="lightcoral", width=100)
        reset_button.grid(row=1, column=2, padx=5, pady=5)  # Menempatkan tombol reset dengan padding

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3 *.wav *.aac *.flac")])
        if file_path:
            self.input_file_path = file_path  # Menyimpan jalur file yang dipilih
            self.input_file_label.configure(text=f"Selected File: {os.path.basename(self.input_file_path)}")  # Menampilkan nama file yang dipilih

    def encrypt_file(self):
        key = self.key_entry.get()
        if len(key) != 10 or not key.isdigit():
            messagebox.showerror("Error", "NIM must be 10 digits long!")  # Menampilkan pesan error jika NIM tidak 10 angka
            return
        if not self.input_file_path:
            messagebox.showerror("Error", "Please select a file first!")  # Menampilkan pesan error jika tidak ada file yang dipilih
            return
        try:
            with open(self.input_file_path, 'rb') as file:
                plaintext = file.read()  # Membaca isi file sebagai byte

            # Mengukur waktu mulai enkripsi
            start_time = time.time()

            # Padding key menjadi 8 karakter dengan memotong atau menambahkan
            padded_key = key[:8].ljust(8)  # Menggunakan 8 karakter pertama dari NIM
            des = DES.new(padded_key.encode('utf-8'), DES.MODE_CBC)  # Membuat objek DES dengan mode CBC
            iv = des.iv  # Mengambil nilai inisialisasi (IV)
            padded_text = pad(plaintext, DES.block_size)  # Menambahkan padding pada plaintext
            encrypted_text = des.encrypt(padded_text)  # Mengenkripsi teks yang sudah dipadding
            encoded_text = iv + encrypted_text  # Menggabungkan IV dan teks yang dienkripsi

            output_path = self.input_file_path + '_encrypt.mp3'  # Menentukan jalur file output
            with open(output_path, 'wb') as file:
                file.write(encoded_text)  # Menyimpan teks yang dienkripsi ke file

            # Menghitung ukuran file yang dienkripsi
            encrypted_size = os.path.getsize(output_path)
            encrypted_size_kb = encrypted_size / 1024  # Ukuran dalam kilobyte

            # Mengukur waktu selesai enkripsi
            end_time = time.time()
            duration = end_time - start_time  # Menghitung durasi enkripsi

            messagebox.showinfo("Success", f"Encrypted file saved as {output_path}\n\nTime: {duration:.4f} seconds\nSize: {encrypted_size_kb:.2f} KB")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during encryption: {e}")  # Menampilkan pesan error jika terjadi kesalahan

    def decrypt_file(self):
        key = self.key_entry.get()
        if len(key) != 10 or not key.isdigit():
            messagebox.showerror("Error", "NIM must be 10 digits long!")  # Menampilkan pesan error jika NIM tidak 10 angka
            return
        if not self.input_file_path or not self.input_file_path.endswith('_encrypt.mp3'):
            messagebox.showerror("Error", "Please select an encrypted file (.mp3) first!")  # Menampilkan pesan error jika tidak ada file terenkripsi yang dipilih
            return
        try:
            with open(self.input_file_path, 'rb') as file:
                encrypted_text = file.read()  # Membaca isi file terenkripsi

            # Mengukur waktu mulai dekripsi
            start_time = time.time()

            iv = encrypted_text[:DES.block_size]  # Memisahkan IV dari teks terenkripsi
            ciphertext = encrypted_text[DES.block_size:]  # Memisahkan teks terenkripsi
            padded_key = key[:8].ljust(8)  # Menggunakan 8 karakter pertama dari NIM
            des = DES.new(padded_key.encode('utf-8'), DES.MODE_CBC, iv)  # Membuat objek DES dengan mode CBC dan IV
            padded_text = des.decrypt(ciphertext)  # Mendekripsi teks terenkripsi
            plaintext = unpad(padded_text, DES.block_size)  # Menghapus padding dari plaintext

            # Menentukan jalur file output
            output_path = self.input_file_path.replace('_encrypt.mp3', '.mp3')  # Mengganti ekstensi menjadi .mp3

            with open(output_path, 'wb') as file:
                file.write(plaintext)  # Menyimpan plaintext ke file

            # Menghitung ukuran file yang didekripsi
            decrypted_size = os.path.getsize(output_path)
            decrypted_size_kb = decrypted_size / 1024  # Ukuran dalam kilobyte

            # Mengukur waktu selesai dekripsi
            end_time = time.time()
            duration = end_time - start_time  # Menghitung durasi dekripsi

            messagebox.showinfo("Success", f"Decrypted file saved as {output_path}\n\nTime: {duration:.4f} seconds\nSize: {decrypted_size_kb:.2f} KB")
        except ValueError as ve:
            messagebox.showerror("Error", f"Decryption error (possibly incorrect padding or key): {ve}")  # Menampilkan pesan error jika terjadi kesalahan padding atau kunci
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during decryption: {e}")  # Menampilkan pesan error jika terjadi kesalahan

    def reset(self):
        self.input_file_label.configure(text='Selected File: None')  # Mengatur ulang label file yang dipilih
        self.input_file_path = None  # Mengatur ulang jalur file yang dipilih
        self.key_entry.delete(0, 'end')  # Menghapus input kunci

# Titik masuk utama program untuk menguji kelas ini
if __name__ == "__main__":
    root = ctk.CTk()  # Membuat instance dari aplikasi CTk
    app = EncryptionAudioApp(root)  # Membuat instance dari aplikasi enkripsi audio
    root.mainloop()  # Memulai loop utama aplikasi
