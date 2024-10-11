import customtkinter as ctk
from tkinter import filedialog, messagebox, scrolledtext
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import os
import time
import binascii

class TextEncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Encryption Decryption (DES)")
        self.root.geometry("660x600")
        self.setup_ui()

    def setup_ui(self):
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(pady=10, padx=5)

        # Text Entry for Input
        self.text_entry_label = ctk.CTkLabel(self.frame, text="Text to Encrypt:")
        self.text_entry_label.grid(row=0, column=0, padx=5, pady=5)
        self.text_entry = ctk.CTkEntry(self.frame, width=50)
        self.text_entry.grid(row=1, column=0, padx=5, pady=5)

        # Browse File Button
        self.browse_button = ctk.CTkButton(self.frame, text="( + ) Browse Text File to Encrypt", command=self.browse_file, width=250)
        self.browse_button.grid(row=2, column=0, padx=5, pady=5)

        # Key Input Section
        self.key_label = ctk.CTkLabel(self.frame, text="Key:")
        self.key_label.grid(row=3, column=0, padx=5, pady=5)
        self.key_entry = ctk.CTkEntry(self.frame, width=50)
        self.key_entry.grid(row=4, column=0, padx=5, pady=5)

        # Key Type Selection
        self.key_type_var = ctk.CTkComboBox(self.frame, values=["String (8 chars)", "Hexadecimal (16 chars)"])
        self.key_type_var.grid(row=5, column=0, padx=5, pady=5)
        self.key_type_var.set("String (8 chars)")  # Default selection

        # Action Buttons
        self.encryption_button = ctk.CTkButton(self.frame, text="Encrypt", command=self.encrypt_text, width=120)
        self.encryption_button.grid(row=6, column=0, padx=5, pady=5)

        self.decryption_button = ctk.CTkButton(self.frame, text="Decrypt", command=self.decrypt_text, width=120)
        self.decryption_button.grid(row=7, column=0, padx=5, pady=5)

        # Scrolled Text for displaying results
        self.result_text = scrolledtext.ScrolledText(self.root, width=80, height=15)
        self.result_text.pack(pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                self.text_entry.delete(0, 'end')
                self.text_entry.insert(0, file.read())

    def encrypt_text(self):
        key = self.key_entry.get()
        key_type = self.key_type_var.get()

        if key_type == "String (8 chars)":
            if len(key) != 8:
                messagebox.showerror("Error", "Key must be 8 characters long!")
                return
            key = key.encode('utf-8')
        elif key_type == "Hexadecimal (16 chars)":
            if len(key) != 16:
                messagebox.showerror("Error", "Key must be 16 hexadecimal digits!")
                return
            key = binascii.unhexlify(key)

        text_to_encrypt = self.text_entry.get()
        if not text_to_encrypt:
            messagebox.showerror("Error", "Please enter text to encrypt!")
            return

        try:
            des = DES.new(key, DES.MODE_CBC)
            padded_text = pad(text_to_encrypt.encode('utf-8'), DES.block_size)
            iv = des.iv
            encrypted_text = des.encrypt(padded_text)
            encoded_text = iv + encrypted_text
            hex_encoded_text = binascii.hexlify(encoded_text).decode()  # Convert to hex

            self.result_text.delete('1.0', 'end')
            self.result_text.insert('end', f"Encrypted content (in hex):\n{hex_encoded_text}\n")
            self.save_encrypted_file(hex_encoded_text)
            messagebox.showinfo("Encryption Completed", "Encryption successful!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during encryption: {e}")

    def decrypt_text(self):
        key = self.key_entry.get()
        key_type = self.key_type_var.get()

        if key_type == "String (8 chars)":
            if len(key) != 8:
                messagebox.showerror("Error", "Key must be 8 characters long!")
                return
            key = key.encode('utf-8')
        elif key_type == "Hexadecimal (16 chars)":
            if len(key) != 16:
                messagebox.showerror("Error", "Key must be 16 hexadecimal digits!")
                return
            key = binascii.unhexlify(key)

        hex_encoded_content = self.result_text.get('1.0', 'end').strip().split('\n')[-1]
        if not hex_encoded_content.startswith("Encrypted content (in hex):"):
            messagebox.showerror("Error", "No encrypted content found for decryption!")
            return

        hex_encoded_content = hex_encoded_content.split(': ')[1]
        encoded_content = binascii.unhexlify(hex_encoded_content)  # Convert hex to bytes

        try:
            iv = encoded_content[:DES.block_size]
            ciphertext = encoded_content[DES.block_size:]
            des = DES.new(key, DES.MODE_CBC, iv)
            padded_text = des.decrypt(ciphertext)
            plaintext = unpad(padded_text, DES.block_size)

            self.result_text.delete('1.0', 'end')
            self.result_text.insert('end', f"Decrypted content:\n{plaintext.decode('utf-8')}\n")
            messagebox.showinfo("Decryption Completed", "Decryption successful!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during decryption: {e}")

    def save_encrypted_file(self, hex_encoded_text):
        with open('encrypted_text.txt', 'w') as file:
            file.write(hex_encoded_text)

if __name__ == "__main__":
    root = ctk.CTk()
    app = TextEncryptionApp(root)
    root.mainloop()
