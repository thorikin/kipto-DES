import customtkinter as ctk  # Mengimpor pustaka customtkinter sebagai ctk untuk membuat antarmuka grafis
from audio_encryption import EncryptionAudioApp  # Mengimpor kelas EncryptionAudioApp dari modul audio_encryption
from files_encryption import EncryptionFilesApp  # Mengimpor kelas EncryptionFilesApp dari modul files_encryption
from image_encryption import ImageEncryptorApp  # Mengimpor kelas ImageEncryptorApp dari modul image_encryption
from text_encryption import TextEncryptionApp  # Mengimpor kelas TextEncryptionApp dari modul text_encryption
from video_encryption import VideoEncryptorApp  # Mengimpor kelas VideoEncryptorApp dari modul video_encryption

class HomePage:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Encryption Standard App")  # Mengatur judul jendela utama
        self.root.geometry("660x525")  # Mengatur ukuran jendela utama

        # Header
        self.header_label = ctk.CTkLabel(self.root, text="DATA ENCRYPTION STANDARD APP", font=("Helvetica", 30, "bold"))  # Membuat label header
        self.header_label.pack(pady=(10, 20))  # Menempatkan label header dengan padding

        # Tombol untuk membuka halaman enkripsi teks
        self.text_button = ctk.CTkButton(self.root, text="Text", command=self.open_text_page, width=300, height=70)
        self.text_button.pack(pady=10)  # Menempatkan tombol dengan padding

        # Tombol untuk membuka halaman enkripsi file
        self.file_button = ctk.CTkButton(self.root, text="Files", command=self.open_file_page, width=300, height=70)
        self.file_button.pack(pady=10)  # Menempatkan tombol dengan padding

        # Tombol untuk membuka halaman enkripsi gambar
        self.image_button = ctk.CTkButton(self.root, text="Image", command=self.open_image_page, width=300, height=70)
        self.image_button.pack(pady=10)  # Menempatkan tombol dengan padding

        # Tombol untuk membuka halaman enkripsi video
        self.video_button = ctk.CTkButton(self.root, text="Video", command=self.open_video_page, width=300, height=70)
        self.video_button.pack(pady=10)  # Menempatkan tombol dengan padding

        # Tombol untuk membuka halaman enkripsi audio
        self.audio_button = ctk.CTkButton(self.root, text="Audio", command=self.open_audio_page, width=300, height=70)
        self.audio_button.pack(pady=10)  # Menempatkan tombol dengan padding

    # Metode untuk membuka halaman enkripsi gambar
    def open_image_page(self):
        self.new_window = ctk.CTkToplevel(self.root)  # Membuat jendela baru
        self.app = ImageEncryptorApp(self.new_window)  # Membuka aplikasi enkripsi gambar

    # Metode untuk membuka halaman enkripsi video
    def open_video_page(self):
        self.new_window = ctk.CTkToplevel(self.root)  # Membuat jendela baru
        self.app = VideoEncryptorApp(self.new_window)  # Membuka aplikasi enkripsi video

    # Metode untuk membuka halaman enkripsi teks
    def open_text_page(self):
        self.new_window = ctk.CTkToplevel(self.root)  # Membuat jendela baru
        self.app = TextEncryptionApp(self.new_window)  # Membuka aplikasi enkripsi teks

    # Metode untuk membuka halaman enkripsi file
    def open_file_page(self):
        self.new_window = ctk.CTkToplevel(self.root)  # Membuat jendela baru
        self.app = EncryptionFilesApp(self.new_window)  # Membuka aplikasi enkripsi file

    # Metode untuk membuka halaman enkripsi audio
    def open_audio_page(self):
        self.new_window = ctk.CTkToplevel(self.root)  # Membuat jendela baru
        self.app = EncryptionAudioApp(self.new_window)  # Membuka aplikasi enkripsi audio

# Titik masuk utama program
if __name__ == "__main__":
    app = ctk.CTk()  # Membuat instance dari aplikasi CTk
    ctk.set_default_color_theme("green")  # Mengatur tema warna default menjadi hijau
    homepage = HomePage(app)  # Membuat instance dari halaman utama
    app.mainloop()  # Memulai loop utama aplikasi
