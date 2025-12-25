import tkinter as tk
from tkinter import messagebox
import string
import random
import numpy as np

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def generate_random_key():
    letters = list(string.ascii_uppercase)
    random.shuffle(letters)
    return "".join(letters)

# =====================================================
# LEVEL 1 – CAESAR CIPHER
# =====================================================

def level1():
    win = tk.Toplevel()
    win.title("Level 1: Caesar Cipher")
    win.geometry("400x350")

    tk.Label(win, text="Enter Text").pack(pady=5)
    text_entry = tk.Entry(win, width=40)
    text_entry.pack(pady=5)

    tk.Label(win, text="Enter Key (Number)").pack(pady=5)
    key_entry = tk.Entry(win, width=10)
    key_entry.pack(pady=5)

    output = tk.Label(win, text="", wraplength=350)
    output.pack(pady=20)

    def caesar_encrypt(text, key):
        result = ""
        for ch in text:
            if ch.isalpha():
                base = ord('A') if ch.isupper() else ord('a')
                result += chr((ord(ch) - base + key) % 26 + base)
            else:
                result += ch
        return result

    def encrypt():
        try:
            key = int(key_entry.get())
            output.config(text="Encrypted: " + caesar_encrypt(text_entry.get(), key))
        except:
            output.config(text="Invalid key")

    def decrypt():
        try:
            key = int(key_entry.get())
            output.config(text="Decrypted: " + caesar_encrypt(text_entry.get(), -key))
        except:
            output.config(text="Invalid key")

    tk.Button(win, text="Encrypt", command=encrypt).pack(pady=5)
    tk.Button(win, text="Decrypt", command=decrypt).pack(pady=5)

# =====================================================
# LEVEL 2 – MONOALPHABETIC CIPHER
# =====================================================

def level2():
    win = tk.Toplevel()
    win.title("Level 2: Monoalphabetic Cipher")
    win.geometry("450x400")

    tk.Label(win, text="Enter Text").pack(pady=5)
    text_entry = tk.Entry(win, width=40)
    text_entry.pack(pady=5)

    tk.Label(win, text="Enter 26-letter Key").pack(pady=5)
    key_entry = tk.Entry(win, width=30)
    key_entry.pack(pady=5)

    output = tk.Label(win, text="", wraplength=400)
    output.pack(pady=20)

    def encrypt():
        key = key_entry.get().upper()
        if len(key) != 26:
            output.config(text="Key must be 26 letters")
            return
        table = str.maketrans(string.ascii_uppercase, key)
        output.config(text="Encrypted: " + text_entry.get().upper().translate(table))

    def decrypt():
        key = key_entry.get().upper()
        if len(key) != 26:
            output.config(text="Key must be 26 letters")
            return
        table = str.maketrans(key, string.ascii_uppercase)
        output.config(text="Decrypted: " + text_entry.get().upper().translate(table))

    def random_key():
        key_entry.delete(0, tk.END)
        key_entry.insert(0, generate_random_key())

    tk.Button(win, text="Generate Random Key", command=random_key).pack(pady=5)
    tk.Button(win, text="Encrypt", command=encrypt).pack(pady=5)
    tk.Button(win, text="Decrypt", command=decrypt).pack(pady=5)

# =====================================================
# LEVEL 3 – PLAYFAIR CIPHER
# =====================================================

def level3():
    win = tk.Toplevel()
    win.title("Level 3: Playfair Cipher")
    win.geometry("500x420")

    tk.Label(win, text="Enter Text").pack(pady=5)
    text_entry = tk.Entry(win, width=40)
    text_entry.pack(pady=5)

    tk.Label(win, text="Enter Key").pack(pady=5)
    key_entry = tk.Entry(win, width=30)
    key_entry.pack(pady=5)

    output = tk.Label(win, text="", wraplength=450)
    output.pack(pady=20)

    def generate_matrix(key):
        key = "".join(dict.fromkeys(key.upper().replace('J','I')))
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        matrix = key + "".join(c for c in alphabet if c not in key)
        return [matrix[i*5:(i+1)*5] for i in range(5)]

    def find(matrix, ch):
        for r in range(5):
            for c in range(5):
                if matrix[r][c] == ch:
                    return r, c

    def encrypt():
        text = "".join(c for c in text_entry.get().upper() if c.isalpha()).replace('J','I')
        if len(text) % 2 != 0:
            text += 'X'
        matrix = generate_matrix(key_entry.get())
        result = ""

        for i in range(0, len(text), 2):
            a, b = text[i], text[i+1]
            ra, ca = find(matrix, a)
            rb, cb = find(matrix, b)

            if ra == rb:
                result += matrix[ra][(ca+1)%5] + matrix[rb][(cb+1)%5]
            elif ca == cb:
                result += matrix[(ra+1)%5][ca] + matrix[(rb+1)%5][cb]
            else:
                result += matrix[ra][cb] + matrix[rb][ca]

        output.config(text="Encrypted: " + result)

    def decrypt():
        text = "".join(c for c in text_entry.get().upper() if c.isalpha())
        if len(text) % 2 != 0:
            output.config(text="Invalid ciphertext")
            return
        matrix = generate_matrix(key_entry.get())
        result = ""

        for i in range(0, len(text), 2):
            a, b = text[i], text[i+1]
            ra, ca = find(matrix, a)
            rb, cb = find(matrix, b)

            if ra == rb:
                result += matrix[ra][(ca-1)%5] + matrix[rb][(cb-1)%5]
            elif ca == cb:
                result += matrix[(ra-1)%5][ca] + matrix[(rb-1)%5][cb]
            else:
                result += matrix[ra][cb] + matrix[rb][ca]

        output.config(text="Decrypted: " + result)

    tk.Button(win, text="Encrypt", command=encrypt).pack(pady=5)
    tk.Button(win, text="Decrypt", command=decrypt).pack(pady=5)

# =====================================================
# PLACEHOLDER LEVELS
# =====================================================

def level4():
    messagebox.showinfo("Level 4", "Hill Cipher")
    win = tk.Toplevel()
    win.title("Level 4: Hill Cipher (2x2 Matrix)")
    win.geometry("500x400")

    tk.Label(win, text="Enter Text (letters only)").pack(pady=5)
    text_entry = tk.Entry(win, width=40)
    text_entry.pack(pady=5)

    tk.Label(win, text="Enter 2x2 Key Matrix (comma-separated, e.g., 3,3,2,5)").pack(pady=5)
    key_entry = tk.Entry(win, width=30)
    key_entry.pack(pady=5)

    output = tk.Label(win, text="", wraplength=450)
    output.pack(pady=20)

    def parse_key(key_str):
        try:
            nums = [int(x) for x in key_str.split(',')]
            if len(nums) != 4:
                return None
            return np.array(nums).reshape(2,2)
        except:
            return None

    def hill_encrypt(text, key_matrix):
        text = "".join([c.upper() for c in text if c.isalpha()])
        while len(text) % 2 != 0:
            text += "X"
        nums = [ord(c)-ord('A') for c in text]
        ciphertext = ""
        for i in range(0, len(nums), 2):
            pair = np.array([[nums[i]], [nums[i+1]]])
            c_pair = np.dot(key_matrix, pair) % 26
            ciphertext += chr(int(c_pair[0][0])+ord('A')) + chr(int(c_pair[1][0])+ord('A'))
        return ciphertext

    def hill_decrypt(text, key_matrix):
        det = int(np.round(np.linalg.det(key_matrix))) % 26
        try:
            det_inv = pow(det, -1, 26)
        except:
            return "Key matrix not invertible modulo 26"
        adj = np.round(det * np.linalg.inv(key_matrix)).astype(int) % 26
        key_inv = (det_inv * adj) % 26
        nums = [ord(c)-ord('A') for c in text]
        plaintext = ""
        for i in range(0, len(nums), 2):
            pair = np.array([[nums[i]], [nums[i+1]]])
            p_pair = np.dot(key_inv, pair) % 26
            plaintext += chr(int(p_pair[0][0])+ord('A')) + chr(int(p_pair[1][0])+ord('A'))
        return plaintext

    def encrypt():
        key_matrix = parse_key(key_entry.get())
        if key_matrix is None:
            output.config(text="Invalid key! Enter 4 numbers separated by commas.")
            return
        result = hill_encrypt(text_entry.get(), key_matrix)
        output.config(text="Encrypted: " + result)

    def decrypt():
        key_matrix = parse_key(key_entry.get())
        if key_matrix is None:
            output.config(text="Invalid key! Enter 4 numbers separated by commas.")
            return
        result = hill_decrypt(text_entry.get(), key_matrix)
        output.config(text="Decrypted: " + result)

    tk.Button(win, text="Encrypt", command=encrypt).pack(pady=5)
    tk.Button(win, text="Decrypt", command=decrypt).pack(pady=5)


def level5():
    messagebox.showinfo("Level 5", "Vernam Cipher")
    win = tk.Toplevel()
    win.title("Level 5: Vernam Cipher")
    win.geometry("500x400")

    tk.Label(win, text="Enter Text (letters only)").pack(pady=5)
    text_entry = tk.Entry(win, width=40)
    text_entry.pack(pady=5)

    tk.Label(win, text="Enter Key (same length as text)").pack(pady=5)
    key_entry = tk.Entry(win, width=40)
    key_entry.pack(pady=5)

    output = tk.Label(win, text="", wraplength=450)
    output.pack(pady=20)

    def generate_key():
        text = text_entry.get().upper()
        key = "".join(random.choice(string.ascii_uppercase) for _ in text if _.isalpha())
        key_entry.delete(0, tk.END)
        key_entry.insert(0, key)

    def vernam_encrypt_decrypt(text, key):
        text = "".join([c.upper() for c in text if c.isalpha()])
        key = "".join([c.upper() for c in key if c.isalpha()])
        if len(key) != len(text):
            return "Key length must match text length!"
        result = ""
        for t, k in zip(text, key):
            val = (ord(t)-65) ^ (ord(k)-65)  # XOR
            result += chr(val + 65)
        return result

    def encrypt():
        text = text_entry.get()
        key = key_entry.get()
        output.config(text="Encrypted: " + vernam_encrypt_decrypt(text, key))

    def decrypt():
        text = text_entry.get()
        key = key_entry.get()
        output.config(text="Decrypted: " + vernam_encrypt_decrypt(text, key))

    tk.Button(win, text="Generate Random Key", command=generate_key).pack(pady=5)
    tk.Button(win, text="Encrypt", command=encrypt).pack(pady=5)
    tk.Button(win, text="Decrypt", command=decrypt).pack(pady=5)


# =====================================================
# MAIN WINDOW
# =====================================================

root = tk.Tk()
root.title("Multi-Level Cryptography System")
root.geometry("400x300")

tk.Label(root, text="Multi-Level Cryptography System", font=("Arial", 14)).pack(pady=20)

tk.Button(root, text="Level 1: Caesar Cipher", command=level1).pack(pady=5)
tk.Button(root, text="Level 2: Monoalphabetic Cipher", command=level2).pack(pady=5)
tk.Button(root, text="Level 3: Playfair Cipher", command=level3).pack(pady=5)
tk.Button(root, text="Level 4: Hill Cipher", command=level4).pack(pady=5)
tk.Button(root, text="Level 5: Vernam Cipher", command=level5).pack(pady=5)

root.mainloop()

