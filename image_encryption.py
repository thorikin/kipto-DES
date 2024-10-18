import numpy as np
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox

# Constants (untuk lookup table permutasi)
INITIAL_PERMUTATION_TABLE = [58, 50, 42, 34, 26, 18, 10, 2,
                             60, 52, 44, 36, 28, 20, 12, 4,
                             62, 54, 46, 38, 30, 22, 14, 6,
                             64, 56, 48, 40, 32, 24, 16, 8,
                             57, 49, 41, 33, 25, 17, 9, 1,
                             59, 51, 43, 35, 27, 19, 11, 3,
                             61, 53, 45, 37, 29, 21, 13, 5,
                             63, 55, 47, 39, 31, 23, 15, 7]
FINAL_PERMUTATION_TABLE = [40, 8, 48, 16, 56, 24, 64, 32,
                           39, 7, 47, 15, 55, 23, 63, 31,
                           38, 6, 46, 14, 54, 22, 62, 30,
                           37, 5, 45, 13, 53, 21, 61, 29,
                           36, 4, 44, 12, 52, 20, 60, 28,
                           35, 3, 43, 11, 51, 19, 59, 27,
                           34, 2, 42, 10, 50, 18, 58, 26,
                           33, 1, 41, 9, 49, 17, 57, 25]
PC1 = [57, 49, 41, 33, 25, 17, 9,
       1, 58, 50, 42, 34, 26, 18,
       10, 2, 59, 51, 43, 35, 27,
       19, 11, 3, 60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15,
       7, 62, 54, 46, 38, 30, 22,
       14, 6, 61, 53, 45, 37, 29,
       21, 13, 5, 28, 20, 12, 4]
PC2 = [14, 17, 11, 24, 1, 5, 3, 28,
       15, 6, 21, 10, 23, 19, 12, 4,
       26, 8, 16, 7, 27, 20, 13, 2,
       41, 52, 31, 37, 47, 55, 30, 40,
       51, 45, 33, 48, 44, 49, 39, 56,
       34, 53, 46, 42, 50, 36, 29, 32]
SHIFT_SCHEDULE = [1, 1, 2, 2, 2, 2, 2, 2,
                  1, 2, 2, 2, 2, 2, 2, 1]
EXPANSION_TABLE = [32, 1, 2, 3, 4, 5,
                   4, 5, 6, 7, 8, 9,
                   8, 9, 10, 11, 12, 13,
                   12, 13, 14, 15, 16, 17,
                   16, 17, 18, 19, 20, 21,
                   20, 21, 22, 23, 24, 25,
                   24, 25, 26, 27, 28, 29,
                   28, 29, 30, 31, 32, 1]
P_BOX = [16, 7, 20, 21,
         29, 12, 28, 17,
         1, 15, 23, 26,
         5, 18, 31, 10,
         2, 8, 24, 14,
         32, 27, 3, 9,
         19, 13, 30, 6,
         22, 11, 4, 25]
S_BOXES = [# S1
[
[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
[0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
[4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
[15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
],
# S2
[
[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
[3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
[0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
[13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
],
# S3
[
[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
[13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
[13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
[1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
],
# S4
[
[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
[13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
[10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
[3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
],
# S5
[
[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
[14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
[4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
[11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
],
# S6
[
[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
[10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
[9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
[4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
],
# S7
[
[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
[13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
[1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
[6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
],
# S8
  [
  [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
  [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
  [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
  [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
  ]]

# Define your DES functions here (same as your original code)

def generate_des_key(key_number):
    binary_str = format(key_number, '064b')
    return np.array([int(bit) for bit in binary_str], dtype=np.uint8)

def pad_data(data):
    pad_length = 8 - (len(data) % 8)
    return np.pad(data, (0, pad_length), 'constant', constant_values=(pad_length,))

def unpad_data(data):
    pad_length = data[-1]
    return data[:-pad_length]

def permute(block, table):
    return np.array([block[i - 1] for i in table])

def initial_permutation(block):
    return permute(block, INITIAL_PERMUTATION_TABLE)

def final_permutation(block):
    return permute(block, FINAL_PERMUTATION_TABLE)

def key_schedule(key):
    # Implementasi key schedule yang sebenarnya
    subkeys = []
    for i in range(16):
        subkey = np.roll(key, -i)[:48]  # Ini hanya contoh, bukan implementasi DES yang benar
        subkeys.append(subkey)
    return subkeys

def substitute(expanded_block):
    substituted = np.zeros(32, dtype=np.uint8)
    for i in range(8):
        block = expanded_block[i*6:(i+1)*6]
        row = int(block[0]) << 1 | int(block[5])
        col = (int(block[1]) << 3) | (int(block[2]) << 2) | (int(block[3]) << 1) | int(block[4])
        val = S_BOXES[i][row][col]
        substituted[i*4:(i+1)*4] = [(val >> j) & 1 for j in range(3, -1, -1)]
    return substituted

def f_function(half_block, round_key):
    expanded = permute(half_block, EXPANSION_TABLE)
    xored = np.bitwise_xor(expanded, round_key)
    substituted = substitute(xored)
    return permute(substituted, P_BOX)

def des_encrypt_block(block, subkeys):
    block = initial_permutation(block)
    left, right = block[:32], block[32:]
    for i in range(16):
        left, right = right, np.bitwise_xor(left, f_function(right, subkeys[i]))
    block = np.concatenate((right, left))
    return final_permutation(block)

def des_decrypt_block(block, subkeys):
    block = initial_permutation(block)
    left, right = block[:32], block[32:]
    for i in range(15, -1, -1):
        left, right = right, np.bitwise_xor(left, f_function(right, subkeys[i]))
    block = np.concatenate((right, left))
    return final_permutation(block)

def process_image(file_path, key, output_path, mode='encrypt'):
    try:
        image = Image.open(file_path).convert('RGB')  # Ubah ke RGB untuk memudahkan proses
        image_data = np.array(image)

        # Generate subkeys
        subkeys = key_schedule(key)

        processed_channels = []
        
        # Periksa jumlah saluran
        if len(image_data.shape) == 2:  # Gambar hitam putih
            # Jika hanya ada satu saluran, jadikan saluran grayscale sebagai data yang sama
            channel_data = image_data.flatten()
            bits = np.unpackbits(channel_data)

            if len(bits) % 64 != 0:
                pad_length = 64 - (len(bits) % 64)
                bits = np.pad(bits, (0, pad_length), 'constant', constant_values=0)

            processed_bits = []
            for i in range(0, len(bits), 64):
                block = bits[i:i+64]
                if mode == 'encrypt':
                    processed_block = des_encrypt_block(block, subkeys)
                else:
                    processed_block = des_decrypt_block(block, subkeys)
                processed_bits.extend(processed_block)

            processed_channel = np.packbits(np.array(processed_bits))
            processed_image = processed_channel.reshape(image_data.shape)  # Bentuk kembali ke dimensi asli

        else:  # Gambar berwarna (RGB)
            for channel in range(image_data.shape[2]):
                channel_data = image_data[:,:,channel].flatten()
                bits = np.unpackbits(channel_data)

                if len(bits) % 64 != 0:
                    pad_length = 64 - (len(bits) % 64)
                    bits = np.pad(bits, (0, pad_length), 'constant', constant_values=0)

                processed_bits = []
                for i in range(0, len(bits), 64):
                    block = bits[i:i+64]
                    if mode == 'encrypt':
                        processed_block = des_encrypt_block(block, subkeys)
                    else:
                        processed_block = des_decrypt_block(block, subkeys)
                    processed_bits.extend(processed_block)

                processed_channel = np.packbits(np.array(processed_bits))
                processed_channels.append(processed_channel[:image_data.shape[0]*image_data.shape[1]].reshape(image_data.shape[:2]))

            processed_image = np.stack(processed_channels, axis=-1)

        # Simpan gambar hasil pemrosesan
        Image.fromarray(processed_image.astype(np.uint8)).save(output_path)
        return output_path
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        return None

def encrypt_image():
    file_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not file_path:
        return
    key_number = int(key_entry.get())
    key = generate_des_key(key_number)
    output_path = filedialog.asksaveasfilename(defaultextension=".png", title="Save Encrypted Image")
    if output_path:
        process_image(file_path, key, output_path, mode='encrypt')
        messagebox.showinfo("Success", "Image encrypted successfully.")

def decrypt_image():
    file_path = filedialog.askopenfilename(title="Select Encrypted Image File", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not file_path:
        return
    key_number = int(key_entry.get())
    key = generate_des_key(key_number)
    output_path = filedialog.asksaveasfilename(defaultextension=".png", title="Save Decrypted Image")
    if output_path:
        process_image(file_path, key, output_path, mode='decrypt')
        messagebox.showinfo("Success", "Image decrypted successfully.")

# GUI Setup
root = tk.Tk()
root.title("DES Image Encryption/Decryption")

key_label = tk.Label(root, text="Enter Key Number:")
key_label.pack(pady=5)

key_entry = tk.Entry(root)
key_entry.pack(pady=5)

encrypt_button = tk.Button(root, text="Encrypt Image", command=encrypt_image)
encrypt_button.pack(pady=10)

decrypt_button = tk.Button(root, text="Decrypt Image", command=decrypt_image)
decrypt_button.pack(pady=10)

root.mainloop()
