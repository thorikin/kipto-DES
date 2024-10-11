import customtkinter as ctk
from tkinter import filedialog, messagebox, scrolledtext
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import os
import time
import binascii

class VideoEncryptionApp:
    def __init__(self, root):
        self.root = root
        self.input_file_path = None
        self.decryption_file_path = None
        self.root.title("Video Encryption Decryption (DES)")
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

        self.button_frame = ctk.CTkFrame(self.root)
        self.button_frame.pack(pady=10, padx=5)

        self.key_type_var = ctk.CTkComboBox(self.button_frame, values=["Hexa (16 Digit)", "String (8 Char)"])
        self.key_type_var.grid(row=0, column=1, padx=2, pady=5, sticky='ew')
        self.key_type_var.set("None")

        self.key_label = ctk.CTkLabel(self.button_frame, text="Key :")
        self.key_label.grid(row=0, column=0, padx=5, pady=5)
        self.key_entry = ctk.CTkEntry(self.button_frame)
        self.key_entry.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky='ew')

        self.encryption_button = ctk.CTkButton(self.button_frame, text="Encrypt", command=self.encrypt_file, width=256)
        self.encryption_button.grid(row=2, column=0, padx=5, pady=5, sticky='ew')

        self.decryption_button = ctk.CTkButton(self.button_frame, text="Decrypt", command=self.decrypt_file, width=256)
        self.decryption_button.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

        self.reset_button = ctk.CTkButton(self.button_frame, text="Reset", command=self.reset, fg_color="#D03F2C", hover_color="lightcoral", width=80)
        self.reset_button.grid(row=2, column=2, padx=5, pady=5)

        # Scrolled Text for displaying results
        self.result_text = scrolledtext.ScrolledText(self.root, width=80, height=10)
        self.result_text.pack(pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mkv;*.mov")])
        if file_path:
            self.input_file_path = file_path
            self.input_file_label.configure(text=f"Selected File to Encrypt: {os.path.basename(self.input_file_path)}")

    def browse_encrypted_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Encrypted files", "*.txt")])
        if file_path:
            self.decryption_file_path = file_path
            self.decryption_file_label.configure(text=f"Selected Encrypted File: {os.path.basename(self.decryption_file_path)}")

    def encrypt_file(self):
        key_input = self.key_entry.get()
        key_type = self.key_type_var.get()
        if (key_type == "String (8 Char)" and len(key_input) != 8) or (key_type == "Hexa (16 Digit)" and len(key_input) != 16):
            messagebox.showerror("Error", "Key length is incorrect based on the selected type!")
            return
        if not self.input_file_path:
            messagebox.showerror("Error", "Please select a file to encrypt first!")
            return

        key = key_input.encode('utf-8') if key_type == "String (8 Char)" else binascii.unhexlify(key_input)
        initial_size = os.path.getsize(self.input_file_path)

        try:
            with open(self.input_file_path, 'rb') as file:
                plaintext = file.read()

            start_time = time.time()
            des = DES.new(key, DES.MODE_CBC)
            iv = des.iv
            padded_text = pad(plaintext, DES.block_size)
            encrypted_text = des.encrypt(padded_text)
            encoded_text = iv + encrypted_text
            hex_encoded_text = binascii.hexlify(encoded_text).decode()  # Convert to hex
            end_time = time.time()

            save_path = self.input_file_path + '.enc.txt'
            with open(save_path, 'w') as file:
                file.write(hex_encoded_text)  # Save the hex encoded text

            final_size = os.path.getsize(save_path)
            duration = end_time - start_time

            self.result_text.delete('1.0', 'end')
            self.result_text.insert('end', f"Encrypted content (in hex):\n{hex_encoded_text}\n")
            messagebox.showinfo("Encryption Completed", f"Encryption successful!\nFile saved to: {save_path}\nDuration: {duration:.4f} seconds\nInitial size: {initial_size} bytes\nEncrypted size: {final_size} bytes")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during encryption: {e}")

    def decrypt_file(self):
        key_input = self.key_entry.get()
        key_type = self.key_type_var.get()
        if (key_type == "String (8 Char)" and len(key_input) != 8) or (key_type == "Hexa (16 Digit)" and len(key_input) != 16):
            messagebox.showerror("Error", "Key length is incorrect based on the selected type!")
            return
        if not self.decryption_file_path:
            messagebox.showerror("Error", "Please select an encrypted file to decrypt first!")
            return

        key = key_input.encode('utf-8') if key_type == "String (8 Char)" else binascii.unhexlify(key_input)
        initial_size = os.path.getsize(self.decryption_file_path)

        try:
            with open(self.decryption_file_path, 'r') as file:
                hex_encoded_content = file.read()

            start_time = time.time()
            encoded_content = binascii.unhexlify(hex_encoded_content)  # Convert hex to bytes
            iv = encoded_content[:DES.block_size]
            ciphertext = encoded_content[DES.block_size:]
            des = DES.new(key, DES.MODE_CBC, iv)
            padded_text = des.decrypt(ciphertext)
            plaintext = unpad(padded_text, DES.block_size)
            end_time = time.time()

            save_path = self.decryption_file_path.rsplit('.', 2)[0] + '_decrypted.mp4'
            with open(save_path, 'wb') as file:
                file.write(plaintext)

            final_size = os.path.getsize(save_path)
            duration = end_time - start_time

            self.result_text.delete('1.0', 'end')
            self.result_text.insert('end', f"Decrypted content:\n{plaintext.decode('utf-8', errors='ignore')}\n")
            messagebox.showinfo("Decryption Completed", f"Decryption successful!\nFile saved to: {save_path}\n\nTime: {duration:.2f} seconds\nInitial size: {initial_size} bytes\nDecrypted size: {final_size} bytes")
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
