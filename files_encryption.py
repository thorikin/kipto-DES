import customtkinter as ctk
from tkinter import filedialog, messagebox, scrolledtext
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import os
import time
import binascii

class EncryptionFilesApp:
    def __init__(self, root):
        self.root = root
        self.input_file_path = None
        self.root.title("Files Encryption Decryption")
        self.root.geometry("660x525")
        self.setup_ui()

    def setup_ui(self):
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(pady=10, padx=5)

        self.browse_button = ctk.CTkButton(self.frame, text="( + ) Browse File", command=self.browse_file, width=626, height=70)
        self.browse_button.grid(row=1, column=0, columnspan=3, padx=6, pady=5, sticky='ew')

        self.input_file_label = ctk.CTkLabel(self.frame, text="Selected File: None")
        self.input_file_label.grid(row=2, column=0, columnspan=3, padx=6, pady=5)

        self.button_frame = ctk.CTkFrame(self.root)
        self.button_frame.pack(pady=10, padx=5)

        self.key_type_var = ctk.CTkComboBox(self.button_frame, values=["Hexa (16 Digit)", "String (8 Char)"])
        self.key_type_var.grid(row=0, column=1, padx=2, pady=5, sticky='ew')
        self.key_type_var.set("None")

        self.key_label = ctk.CTkLabel(self.button_frame, text="Key :")
        self.key_label.grid(row=0, column=0, padx=5, pady=5)
        self.key_entry = ctk.CTkEntry(self.button_frame)
        self.key_entry.grid(row=1, column=0,columnspan=3, padx=5, pady=5, sticky='ew')

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
        file_path = filedialog.askopenfilename(filetypes=[("All files", "*.*")])
        if file_path:
            self.input_file_path = file_path
            self.input_file_label.configure(text=f"Selected File: {os.path.basename(self.input_file_path)}")

    def encrypt_file(self):
        key_input = self.key_entry.get()
        key_type = self.key_type_var.get()
        if (key_type == "String (8 Char)" and len(key_input) != 8) or (key_type == "Hexa (16 Digit)" and len(key_input) != 16):
            messagebox.showerror("Error", "Key length is incorrect based on the selected type!")
            return
        if not self.input_file_path:
            messagebox.showerror("Error", "Please select a file first!")
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
            end_time = time.time()

            save_path = self.input_file_path + '.enc'
            with open(save_path, 'wb') as file:
                file.write(encoded_text)

            final_size = os.path.getsize(save_path)
            duration = end_time - start_time

            self.result_text.delete('1.0', 'end')
            self.result_text.insert('end', f"Encrypted content (in hex):\n{binascii.hexlify(encoded_text).decode()}\n")
            messagebox.showinfo("Encryption Completed", f"Encryption successful!\nFile saved to: {save_path}\nDuration: {duration:.4f} seconds\nInitial size: {initial_size} bytes\nEncrypted size: {final_size} bytes")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during encryption: {e}")

    def decrypt_file(self):
        key_input = self.key_entry.get()
        key_type = self.key_type_var.get()
        if (key_type == "String (8 Char)" and len(key_input) != 8) or (key_type == "Hexa (16 Digit)" and len(key_input) != 16):
            messagebox.showerror("Error", "Key length is incorrect based on the selected type!")
            return
        if not self.input_file_path:
            messagebox.showerror("Error", "Please select a file first!")
            return

        key = key_input.encode('utf-8') if key_type == "String (8 Char)" else binascii.unhexlify(key_input)
        initial_size = os.path.getsize(self.input_file_path)

        try:
            with open(self.input_file_path, 'rb') as file:
                encrypted_content = file.read()

            start_time = time.time()
            iv = encrypted_content[:DES.block_size]
            ciphertext = encrypted_content[DES.block_size:]
            des = DES.new(key, DES.MODE_CBC, iv)
            padded_text = des.decrypt(ciphertext)
            plaintext = unpad(padded_text, DES.block_size)
            end_time = time.time()

            save_path = self.input_file_path.rsplit('.', 1)[0] + '_decrypted'
            with open(save_path, 'wb') as file:
                file.write(plaintext)

            final_size = os.path.getsize(save_path)
            duration = end_time - start_time

            self.result_text.delete('1.0', 'end')
            self.result_text.insert('end', f"Decrypted content:\n{plaintext.decode('utf-8', errors='ignore')}\n")
            messagebox.showinfo("Decryption Completed", f"Decryption successful!\nFile saved to: {save_path}\n\nTime: {duration:.2f} detik\nInitial size: {initial_size} bytes\nDecrypted size: {final_size} bytes")
        except ValueError as ve:
            messagebox.showerror("Error", f"Decryption error (possibly incorrect padding or key): {ve}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during decryption: {e}")


    def reset(self):
        self.input_file_label.configure(text='Selected File: None')
        self.input_file_path = None
        self.key_entry.delete(0, 'end')
        self.result_text.delete('1.0', 'end')

if __name__ == "__main__":
    app = ctk.CTk()

    ctk.set_default_color_theme("green")
    

    EncryptionFilesApp(app)
    app.mainloop()
