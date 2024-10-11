import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import numpy as np
import os
import time

class ImageEncryptorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Encryption Decryption")
        self.master.geometry("800x600")

        ctk.set_default_color_theme("green")

        self.input_image_path = ""
        self.encrypted_image_path = ""

        self.setup_ui()

    def setup_ui(self):
        frame = ctk.CTkFrame(self.master)
        frame.pack(pady=10, padx=5)

        browse_button = ctk.CTkButton(frame, text="( + ) Browse Image", command=self.browse_image, width=626, height=70)
        browse_button.grid(row=1, column=0, columnspan=3, padx=6, pady=5, sticky='ew')

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

        self.encrypted_image_label = ctk.CTkLabel(image_frame, text="Encrypted Image")
        self.encrypted_image_label.grid(row=0, column=2, padx=10)
        self.encrypted_image_label_image = ctk.CTkLabel(image_frame, width=300, height=300, text='')
        self.encrypted_image_label_image.grid(row=1, column=2, padx=10)

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

            start_time = time.time()

            des = DES.new(key.encode('utf-8'), DES.MODE_CBC)
            iv = des.iv
            padded_text = pad(plaintext, DES.block_size)
            encrypted_text = des.encrypt(padded_text)
            encoded_text = iv + encrypted_text

            # Save the encrypted image
            self.encrypted_image_path = os.path.splitext(self.input_image_path)[0] + '_encrypt.bmp'
            self.save_encrypted_as_image(encoded_text)

            # Load and display the encrypted image
            encrypted_img = self.load_image(self.encrypted_image_path, (300, 300))
            self.encrypted_image_label_image.configure(image=encrypted_img)
            self.encrypted_image_label_image.image = encrypted_img

            # Display processing time
            end_time = time.time()
            duration = end_time - start_time
            messagebox.showinfo("Success", f"Encryption completed in {duration:.4f} seconds.\n\nEncrypted image saved as {self.encrypted_image_path}.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def save_encrypted_as_image(self, encrypted_data):
        width = 300
        height = (len(encrypted_data) // width) + 1
        image_data = np.zeros((height, width, 3), dtype=np.uint8)

        for i in range(len(encrypted_data)):
            row = i // width
            col = i % width
            if i % 3 == 0:
                image_data[row, col, 0] = encrypted_data[i]  # Red channel
            elif i % 3 == 1:
                image_data[row, col, 1] = encrypted_data[i]  # Green channel
            else:
                image_data[row, col, 2] = encrypted_data[i]  # Blue channel

        encrypted_image = Image.fromarray(image_data)
        encrypted_image.save(self.encrypted_image_path)

    def decrypt_image(self):
        key = self.key_entry.get()
        if len(key) != 8:
            messagebox.showerror("Error", "Key must be 8 characters long!")
            return

        # Ask user to select the encrypted .bmp file
        encrypted_file_path = filedialog.askopenfilename(title="Select Encrypted BMP Image", filetypes=[("BMP files", "*.bmp")])
        if not encrypted_file_path:
            return  # User canceled the operation

        try:
            # Load the encrypted image
            encrypted_image = Image.open(encrypted_file_path)
            encrypted_image_data = np.array(encrypted_image)
            encrypted_text = encrypted_image_data.flatten()

            start_time = time.time()

            iv = encrypted_text[:DES.block_size]
            ciphertext = encrypted_text[DES.block_size:]
            des = DES.new(key.encode('utf-8'), DES.MODE_CBC, iv)
            padded_text = des.decrypt(ciphertext)
            plaintext = unpad(padded_text, DES.block_size)

            output_path = os.path.splitext(encrypted_file_path)[0] + '_decrypt.jpg'
            with open(output_path, 'wb') as file:
                file.write(plaintext)

            decrypted_img = self.load_image(output_path, (300, 300))
            self.decrypted_image_label_image.configure(image=decrypted_img)
            self.decrypted_image_label_image.image = decrypted_img

            end_time = time.time()
            duration = end_time - start_time
            messagebox.showinfo("Success", f"Decryption completed in {duration:.4f} seconds.\n\nDecrypted image saved as {output_path}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def browse_image(self):
        # Updated to accept .bmp files as well
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if file_path:
            self.input_image_path = file_path
            input_img = self.load_image(self.input_image_path, (300, 300))
            self.input_image_label_image.configure(image=input_img)
            self.input_image_label_image.image = input_img
            self.decrypted_image_label_image.configure(image='', text='')
            self.encrypted_image_label_image.configure(image='', text='')

    def reset(self):
        self.input_image_label_image.configure(image='', text='')
        self.decrypted_image_label_image.configure(image='', text='')
        self.encrypted_image_label_image.configure(image='', text='')
        self.input_image_path = ""
        self.encrypted_image_path = ""
        self.key_entry.delete(0, 'end')


# Run the application
if __name__ == "__main__":
    root = ctk.CTk()
    app = ImageEncryptorApp(root)
    root.mainloop()
