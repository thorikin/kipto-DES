import customtkinter as ctk
from tkinter import filedialog, messagebox
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import os
import time

class EncryptionAudioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Encryption Decryption")
        self.root.geometry("660x600")
        self.input_file_path = None

        ctk.set_default_color_theme("green")

        self.setup_ui()

    def setup_ui(self):
        frame = ctk.CTkFrame(self.root)
        frame.pack(pady=10, padx=5)

        browse_button = ctk.CTkButton(frame, text="( + ) Browse Audio File", command=self.browse_file, width=626, height=70)
        browse_button.grid(row=1, column=0, columnspan=3, padx=6, pady=5, sticky='ew')

        self.input_file_label = ctk.CTkLabel(frame, text="Selected File: None")
        self.input_file_label.grid(row=2, column=0, columnspan=3, padx=6, pady=5)

        key_frame = ctk.CTkFrame(self.root)
        key_frame.pack(pady=10, padx=10)

        key_label = ctk.CTkLabel(key_frame, text="Key:")
        key_label.grid(row=0, column=0, padx=5, pady=5)

        self.key_entry = ctk.CTkEntry(key_frame, width=30)
        self.key_entry.grid(row=0, column=1, padx=5, pady=5)

        self.key_format_var = ctk.StringVar(value="hex")  # Default to hex
        hex_radio = ctk.CTkRadioButton(key_frame, text="Hexadecimal", variable=self.key_format_var, value="hex")
        hex_radio.grid(row=0, column=2, padx=5, pady=5)
        bit_radio = ctk.CTkRadioButton(key_frame, text="Binary", variable=self.key_format_var, value="bin")
        bit_radio.grid(row=0, column=3, padx=5, pady=5)

        button_frame = ctk.CTkFrame(self.root)
        button_frame.pack(pady=10, padx=10)

        encryption_button = ctk.CTkButton(button_frame, text="Encrypt", command=self.encrypt_file, width=256)
        encryption_button.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

        decryption_button = ctk.CTkButton(button_frame, text="Decrypt", command=self.decrypt_file, width=256)
        decryption_button.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        reset_button = ctk.CTkButton(button_frame, text="Reset", command=self.reset, fg_color="#D03F2C", hover_color="lightcoral", width=100)
        reset_button.grid(row=1, column=2, padx=5, pady=5)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.aac *.flac")])
        if file_path:
            self.input_file_path = file_path
            self.input_file_label.configure(text=f"Selected File: {os.path.basename(self.input_file_path)}")

    def convert_key(self, key):
        """Convert the key from hexadecimal or binary to bytes."""
        if self.key_format_var.get() == "hex":
            return bytes.fromhex(key)
        elif self.key_format_var.get() == "bin":
            return int(key, 2).to_bytes(8, byteorder='big')
        return None

    def encrypt_file(self):
        key = self.key_entry.get()
        if len(key) not in [8, 64]:  # 8 hex characters or 64 binary characters
            messagebox.showerror("Error", "Key must be 8 characters long (hex) or 64 bits long (binary)!")
            return
        if not self.input_file_path:
            messagebox.showerror("Error", "Please select a file first!")
            return

        try:
            key_bytes = self.convert_key(key)
            if key_bytes is None or len(key_bytes) != 8:
                raise ValueError("Invalid key format.")

            with open(self.input_file_path, 'rb') as file:
                plaintext = file.read()

            start_time = time.time()
            des = DES.new(key_bytes, DES.MODE_CBC)
            iv = des.iv
            padded_text = pad(plaintext, DES.block_size)
            encrypted_text = des.encrypt(padded_text)
            encoded_text = iv + encrypted_text

            output_path = self.input_file_path + '_encrypt.bin'
            with open(output_path, 'wb') as file:
                file.write(encoded_text)

            encrypted_size = os.path.getsize(output_path)
            encrypted_size_kb = encrypted_size / 1024

            end_time = time.time()
            duration = end_time - start_time

            messagebox.showinfo("Success", f"Encrypted file saved as {output_path}\n\nTime: {duration:.4f} seconds\nSize: {encrypted_size_kb:.2f} KB")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during encryption: {e}")

    def decrypt_file(self):
        key = self.key_entry.get()
        if len(key) not in [8, 64]:
            messagebox.showerror("Error", "Key must be 8 characters long (hex) or 64 bits long (binary)!")
            return
        if not self.input_file_path or not self.input_file_path.endswith('_encrypt.bin'):
            messagebox.showerror("Error", "Please select an encrypted file (.bin) first!")
            return

        try:
            key_bytes = self.convert_key(key)
            if key_bytes is None or len(key_bytes) != 8:
                raise ValueError("Invalid key format.")

            with open(self.input_file_path, 'rb') as file:
                encrypted_text = file.read()

            start_time = time.time()

            iv = encrypted_text[:DES.block_size]
            ciphertext = encrypted_text[DES.block_size:]
            des = DES.new(key_bytes, DES.MODE_CBC, iv)
            padded_text = des.decrypt(ciphertext)
            plaintext = unpad(padded_text, DES.block_size)

            original_extension = os.path.splitext(self.input_file_path)[0].split('_encrypt')[0]
            output_path = original_extension + '_decrypted' + os.path.splitext(self.input_file_path)[1]

            with open(output_path, 'wb') as file:
                file.write(plaintext)

            decrypted_size = os.path.getsize(output_path)
            decrypted_size_kb = decrypted_size / 1024

            end_time = time.time()
            duration = end_time - start_time

            messagebox.showinfo("Success", f"Decrypted file saved as {output_path}\n\nTime: {duration:.4f} seconds\nSize: {decrypted_size_kb:.2f} KB")
        except ValueError as ve:
            messagebox.showerror("Error", f"Decryption error (possibly incorrect padding or key): {ve}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during decryption: {e}")

    def reset(self):
        self.input_file_label.configure(text='Selected File: None')
        self.input_file_path = None
        self.key_entry.delete(0, 'end')

if __name__ == "__main__":
    root = ctk.CTk()
    app = EncryptionAudioApp(root)
    root.mainloop()
