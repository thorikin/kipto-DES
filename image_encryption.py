import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import os
import time

class ImageEncryptorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Encryption Decryption")
        self.master.geometry("660x525")

        
        ctk.set_default_color_theme("green") 

        # Initialize paths
        self.input_image_path = ""
        self.decrypted_image_path = ""

        # Setup UI
        self.setup_ui()

    def setup_ui(self):
        # Frame for browse button
        frame = ctk.CTkFrame(self.master)
        frame.pack(pady=10, padx=5)

        browse_button = ctk.CTkButton(frame, text="( + ) Browse Image", command=self.browse_image, width=626, height=70)
        browse_button.grid(row=1, column=0, columnspan=3, padx=6, pady=5, sticky='ew')

        # Frame for displaying images
        image_frame = ctk.CTkFrame(self.master)
        image_frame.pack(padx=5)

        self.input_image_label = ctk.CTkLabel(image_frame, text="Input Image")
        self.input_image_label.grid(row=0, column=0, padx=10)
        self.input_image_label_image = ctk.CTkLabel(image_frame, width=300, height=300, text='')
        self.input_image_label_image.grid(row=1, column=0, padx=10)

        self.decrypted_image_label = ctk.CTkLabel(image_frame, text="Decrypted Image")
        self.decrypted_image_label.grid(row=0, column=1, padx=10)
        self.decrypted_image_label_image = ctk.CTkLabel(image_frame, width=300, height=300, text='')
        self.decrypted_image_label_image.grid(row=1, column=1, padx=10)

        # Frame for buttons and key entry
        button_frame = ctk.CTkFrame(self.master)
        button_frame.pack(pady=10, padx=10)

        key_label = ctk.CTkLabel(button_frame, text="Key (8 characters):")
        key_label.grid(row=0, column=0, columnspan=1, padx=5, pady=5)
        self.key_entry = ctk.CTkEntry(button_frame)
        self.key_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky='ew')

        encryption_button = ctk.CTkButton(button_frame, text="Encryption", command=self.encrypt_image, width=256)
        encryption_button.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

        decryption_button = ctk.CTkButton(button_frame, text="Decryption", command=self.decrypt_image, width=256)
        decryption_button.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        reset_button = ctk.CTkButton(button_frame, text="Reset", command=self.reset, fg_color="#D03F2C", hover_color="lightcoral", width=100)
        reset_button.grid(row=1, column=2, padx=5, pady=5)

    def load_image(self, path, size):
        img = Image.open(path)
        img = img.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(img)

    def encrypt_image(self):
        key = self.key_entry.get()
        if len(key) != 8:
            messagebox.showerror("Error", "Key must be 8 characters long!")
            return
        if not self.input_image_path:
            messagebox.showerror("Error", "Please select an image first!")
            return
        try:
            with open(self.input_image_path, 'rb') as file:
                plaintext = file.read()

            # Measure start time
            start_time = time.time()

            des = DES.new(key.encode('utf-8'), DES.MODE_CBC)
            iv = des.iv
            padded_text = pad(plaintext, DES.block_size)
            encrypted_text = des.encrypt(padded_text)
            encoded_text = iv + encrypted_text

            output_path = os.path.splitext(self.input_image_path)[0] + '_encrypt.bin'
            with open(output_path, 'wb') as file:
                file.write(encoded_text)

            # Calculate encrypted file size
            encrypted_size = os.path.getsize(output_path)
            encrypted_size_kb = encrypted_size / 1024  # Size in kilobytes

            # Measure end time
            end_time = time.time()
            duration = end_time - start_time

            messagebox.showinfo("Success", f"Encrypted image saved as {output_path}\n\nTime: {duration:.4f} seconds\nSize: {encrypted_size_kb:.2f} KB")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def decrypt_image(self):
        key = self.key_entry.get()
        if len(key) != 8:
            messagebox.showerror("Error", "Key must be 8 characters long!")
            return
        if not self.input_image_path or not self.input_image_path.endswith('.bin'):
            messagebox.showerror("Error", "Please select an encrypted image (.bin) first!")
            return
        try:
            with open(self.input_image_path, 'rb') as file:
                encrypted_text = file.read()

            # Measure start time
            start_time = time.time()

            iv = encrypted_text[:DES.block_size]
            ciphertext = encrypted_text[DES.block_size:]
            des = DES.new(key.encode('utf-8'), DES.MODE_CBC, iv)
            padded_text = des.decrypt(ciphertext)
            plaintext = unpad(padded_text, DES.block_size)

            output_path = os.path.splitext(self.input_image_path)[0] + '_decrypt.jpg'
            with open(output_path, 'wb') as file:
                file.write(plaintext)

            # Calculate decrypted file size
            decrypted_size = os.path.getsize(output_path)
            decrypted_size_kb = decrypted_size / 1024  # Size in kilobytes

            # Measure end time
            end_time = time.time()
            duration = end_time - start_time

            messagebox.showinfo("Success", f"Decrypted image saved as {output_path}\n\nTime: {duration:.4f} seconds\nSize: {decrypted_size_kb:.2f} KB")

            # Load and display the decrypted image
            decrypted_img = self.load_image(output_path, (300, 300))
            self.decrypted_image_label_image.configure(image=decrypted_img)
            self.decrypted_image_label_image.image = decrypted_img

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def browse_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image and Encrypted files", "*.jpg *.jpeg *.png *.bin")])
        if file_path:
            self.input_image_path = file_path
            if file_path.endswith('.bin'):
                # Show a placeholder for encrypted files
                self.input_image_label_image.configure(text="Encrypted File Selected", image='')
                self.decrypted_image_label_image.configure(image='', text='')
            else:
                input_img = self.load_image(self.input_image_path, (300, 300))
                self.input_image_label_image.configure(image=input_img)
                self.input_image_label_image.image = input_img
                self.decrypted_image_label_image.configure(image='', text='')
                self.decrypted_image_path = ""

    def reset(self):
        self.input_image_label_image.configure(image='', text='')
        self.decrypted_image_label_image.configure(image='', text='')
        self.input_image_path = ""
        self.decrypted_image_path = ""
        self.key_entry.delete(0, 'end')

# Initialize the application
if __name__ == "__main__":
    root = ctk.CTk()
    app = ImageEncryptorApp(root)
    root.mainloop()
