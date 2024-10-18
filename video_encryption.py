import customtkinter as ctk
from tkinter import filedialog, messagebox, scrolledtext
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
import time
import binascii

class VideoEncryptionApp:
    def __init__(self, root):
        self.root = root
        self.input_file_path = None
        self.decryption_file_path = None
        self.root.title("Video Encryption Decryption (AES)")
        self.root.geometry("660x600")
        self.setup_ui()

    def setup_ui(self):
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(pady=10, padx=5)

        self.browse_button = ctk.CTkButton(self.frame, text="( + ) Browse Video File to Encrypt", command=self.browse_file, width=626, height=70)
        self.browse_button.grid(row=1, column=0, columnspan=3, padx=6, pady=5, sticky='ew')

        self.input_file_label = ctk.CTkLabel(self.frame, text="Selected File to Encrypt: None")
        self.input_file_label.grid(row=2, column=0, columnspan=3, padx=6, pady=5)

        self.decryption_browse_button = ctk.CTkButton(self.frame, text="( + ) Browse Encrypted File to Decrypt", command=self.browse_encrypted_file, width=626, height=70)
        self.decryption_browse_button.grid(row=3, column=0, columnspan=3, padx=6, pady=5, sticky='ew')

        self.decryption_file_label = ctk.CTkLabel(self.frame, text="Selected Encrypted File: None")
        self.decryption_file_label.grid(row=4, column=0, columnspan=3, padx=6, pady=5)

        self.key_label = ctk.CTkLabel(self.frame, text="NIM (10 Digits):")
        self.key_label.grid(row=5, column=0, padx=5, pady=5)
        self.key_entry = ctk.CTkEntry(self.frame)
        self.key_entry.grid(row=5, column=1, padx=5, pady=5, sticky='ew')

        self.encryption_button = ctk.CTkButton(self.frame, text="Encrypt", command=self.encrypt_file, width=256)
        self.encryption_button.grid(row=6, column=0, padx=5, pady=5, sticky='ew')

        self.decryption_button = ctk.CTkButton(self.frame, text="Decrypt", command=self.decrypt_file, width=256)
        self.decryption_button.grid(row=6, column=1, padx=5, pady=5, sticky='ew')

        self.reset_button = ctk.CTkButton(self.frame, text="Reset", command=self.reset, fg_color="#D03F2C", hover_color="lightcoral", width=80)
        self.reset_button.grid(row=6, column=2, padx=5, pady=5)

        # Scrolled Text for displaying results
        self.result_text = scrolledtext.ScrolledText(self.root, width=80, height=10)
        self.result_text.pack(pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mkv;*.mov")])
        if file_path:
            self.input_file_path = file_path
            self.input_file_label.configure(text=f"Selected File to Encrypt: {os.path.basename(self.input_file_path)}")

    def browse_encrypted_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Encrypted files", "*.enc")])
        if file_path:
            self.decryption_file_path = file_path
            self.decryption_file_label.configure(text=f"Selected Encrypted File: {os.path.basename(self.decryption_file_path)}")

    def encrypt_file(self):
        nim_input = self.key_entry.get()
        if len(nim_input) != 10 or not nim_input.isdigit():
            messagebox.showerror("Error", "NIM must be a 10-digit number!")
            return
        if not self.input_file_path:
            messagebox.showerror("Error", "Please select a file to encrypt first!")
            return

        key = nim_input.encode('utf-8')  # Use the NIM directly as key (you might want to hash it to ensure it's 16 bytes)
        key = key.ljust(16)[:16]  # Ensure key is 16 bytes (padding/truncating)

        initial_size = os.path.getsize(self.input_file_path)

        try:
            with open(self.input_file_path, 'rb') as file:
                plaintext = file.read()

            start_time = time.time()
            aes = AES.new(key, AES.MODE_CBC)
            iv = aes.iv
            padded_text = pad(plaintext, AES.block_size)
            encrypted_text = aes.encrypt(padded_text)
            encoded_text = iv + encrypted_text
            hex_encoded_text = binascii.hexlify(encoded_text).decode()  # Convert to hex
            end_time = time.time()

            save_path = self.input_file_path + '.enc'
            with open(save_path, 'wb') as file:
                file.write(binascii.unhexlify(hex_encoded_text.encode()))  # Save as binary

            final_size = os.path.getsize(save_path)
            duration = end_time - start_time

            self.result_text.delete('1.0', 'end')
            self.result_text.insert('end', f"Encryption successful!\nFile saved to: {save_path}\nDuration: {duration:.4f} seconds\nInitial size: {initial_size} bytes\nEncrypted size: {final_size} bytes")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during encryption: {e}")

    def decrypt_file(self):
        nim_input = self.key_entry.get()
        if len(nim_input) != 10 or not nim_input.isdigit():
            messagebox.showerror("Error", "NIM must be a 10-digit number!")
            return
        if not self.decryption_file_path:
            messagebox.showerror("Error", "Please select an encrypted file to decrypt first!")
            return

        key = nim_input.encode('utf-8')  # Use the NIM directly as key
        key = key.ljust(16)[:16]  # Ensure key is 16 bytes

        initial_size = os.path.getsize(self.decryption_file_path)

        try:
            with open(self.decryption_file_path, 'rb') as file:
                encoded_content = file.read()

            start_time = time.time()
            iv = encoded_content[:AES.block_size]
            ciphertext = encoded_content[AES.block_size:]
            aes = AES.new(key, AES.MODE_CBC, iv)
            padded_text = aes.decrypt(ciphertext)
            plaintext = unpad(padded_text, AES.block_size)
            end_time = time.time()

            save_path = self.decryption_file_path.rsplit('.', 1)[0] + '_decrypted.mp4'
            with open(save_path, 'wb') as file:
                file.write(plaintext)

            final_size = os.path.getsize(save_path)
            duration = end_time - start_time

            self.result_text.delete('1.0', 'end')
            self.result_text.insert('end', f"Decryption successful!\nFile saved to: {save_path}\nDuration: {duration:.2f} seconds\nInitial size: {initial_size} bytes\nDecrypted size: {final_size} bytes")
        except ValueError as ve:
            messagebox.showerror("Error", f"Decryption error (possibly incorrect padding or key): {ve}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during decryption: {e}")

    def reset(self):
        self.input_file_label.configure(text='Selected File to Encrypt: None')
        self.decryption_file_label.configure(text='Selected Encrypted File: None')
        self.input_file_path = None
        self.decryption_file_path = None
        self.key_entry.delete(0, 'end')
        self.result_text.delete('1.0', 'end')

if __name__ == "__main__":
    root = ctk.CTk()
    app = VideoEncryptionApp(root)
    root.mainloop()
