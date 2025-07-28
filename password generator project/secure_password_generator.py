import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import string
import os
try:
    from cryptography.fernet import Fernet
except ImportError:
    print("Error: 'cryptography' module not found. Install it using 'pip install cryptography'.")
    exit(1)

# Initialize Tkinter root window first
root = tk.Tk()
root.title("Secure Password Generator with Master Password")

# Master password setup
MASTER_PASSWORD = None

def set_master_password():
    global MASTER_PASSWORD
    while True:
        MASTER_PASSWORD = simpledialog.askstring("Master Password", "Set master password:", show="*", parent=root)
        if MASTER_PASSWORD is None:
            messagebox.showwarning("Warning", "Master password is required to continue.", parent=root)
        elif MASTER_PASSWORD.strip() == "":
            messagebox.showwarning("Warning", "Master password cannot be empty.", parent=root)
        else:
            break

# Generate or load encryption key after root is defined
KEY_FILE = "secret.key"
try:
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    else:
        with open(KEY_FILE, "rb") as f:
            key = f.read()
    cipher = Fernet(key)
except (PermissionError, IOError) as e:
    messagebox.showerror("Error", f"Cannot access key file: {e}", parent=root)
    root.quit()
    exit(1)
except ValueError as e:
    messagebox.showerror("Error", f"Invalid encryption key: {e}", parent=root)
    root.quit()
    exit(1)

def generate_password():
    try:
        length = int(length_entry.get())
        if length < 4:
            messagebox.showwarning("Warning", "Password length should be at least 4 characters.", parent=root)
            return
        
        characters = ""
        if uppercase_var.get():
            characters += string.ascii_uppercase
        if lowercase_var.get():
            characters += string.ascii_lowercase
        if digits_var.get():
            characters += string.digits
        if special_var.get():
            characters += string.punctuation
        
        if not characters:
            messagebox.showerror("Error", "Please select at least one character set.", parent=root)
            return
        
        password = ''.join(random.choice(characters) for _ in range(length))
        password_var.set(password)
        evaluate_strength(password)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number.", parent=root)

def copy_password():
    password = password_var.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        messagebox.showinfo("Copied", "Password copied to clipboard! Be cautious with sensitive data.", parent=root)
    else:
        messagebox.showwarning("Warning", "No password to copy.", parent=root)

def save_password():
    password = password_var.get()
    if not password:
        messagebox.showwarning("Warning", "No password to save.", parent=root)
        return
    try:
        encrypted = cipher.encrypt(password.encode())
        with open("saved_passwords.secure", "ab") as f:
            f.write(encrypted + b"\n")
        messagebox.showinfo("Saved", "Password saved to saved_passwords.secure (encrypted)", parent=root)
    except (PermissionError, IOError) as e:
        messagebox.showerror("Error", f"Could not save: {e}", parent=root)

def view_passwords():
    entered_password = simpledialog.askstring("Master Password", "Enter master password:", show="*", parent=root)
    if entered_password is None:
        return
    if entered_password != MASTER_PASSWORD:
        messagebox.showerror("Access Denied", "Incorrect master password.", parent=root)
        return

    if not os.path.exists("saved_passwords.secure"):
        messagebox.showinfo("No File", "No saved passwords found.", parent=root)
        return
    
    try:
        with open("saved_passwords.secure", "rb") as f:
            lines = f.readlines()
        if not lines:
            messagebox.showinfo("No Passwords", "No passwords saved.", parent=root)
            return
        decrypted_passwords = []
        for line in lines:
            decrypted_passwords.append(cipher.decrypt(line.strip()).decode())
        passwords_str = "\n".join(decrypted_passwords)
        messagebox.showinfo("Saved Passwords", passwords_str, parent=root)
    except Exception as e:
        messagebox.showerror("Error", f"Could not decrypt: {e}", parent=root)

def evaluate_strength(password):
    strength = "Weak"
    color = "red"
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)
    
    types_count = sum([has_upper, has_lower, has_digit, has_special])
    
    if len(password) >= 12 and types_count >= 3:
        strength = "Strong"
        color = "green"
    elif len(password) >= 8 and types_count >= 2:
        strength = "Medium"
        color = "orange"
    elif len(password) >= 6:
        strength = "Weak"
        color = "red"
        
    strength_label.config(text=f"Strength: {strength}", fg=color)

# Set master password after root is defined
set_master_password()

# GUI setup
tk.Label(root, text="Enter password length:").grid(row=0, column=0, padx=10, pady=5)
length_entry = tk.Entry(root)
length_entry.grid(row=0, column=1, padx=10, pady=5)

# Checkboxes for complexity
uppercase_var = tk.BooleanVar(value=True)
lowercase_var = tk.BooleanVar(value=True)
digits_var = tk.BooleanVar(value=True)
special_var = tk.BooleanVar(value=True)

tk.Checkbutton(root, text="Include Uppercase", variable=uppercase_var).grid(row=1, column=0, sticky="w", padx=10)
tk.Checkbutton(root, text="Include Lowercase", variable=lowercase_var).grid(row=1, column=1, sticky="w", padx=10)
tk.Checkbutton(root, text="Include Digits", variable=digits_var).grid(row=2, column=0, sticky="w", padx=10)
tk.Checkbutton(root, text="Include Special Characters", variable=special_var).grid(row=2, column=1, sticky="w", padx=10)

# Generate button
generate_button = tk.Button(root, text="Generate Password", command=generate_password)
generate_button.grid(row=3, column=0, columnspan=2, pady=10)

# Password display
password_var = tk.StringVar()
password_entry = tk.Entry(root, textvariable=password_var, width=40) 
password_entry.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Password strength label
strength_label = tk.Label(root, text="Strength: ", font=("Helvetica", 12, "bold"))
strength_label.grid(row=5, column=0, columnspan=2, pady=5)

# Buttons
copy_button = tk.Button(root, text="Copy to Clipboard", command=copy_password)
copy_button.grid(row=6, column=0, pady=5)

save_button = tk.Button(root, text="Save Encrypted", command=save_password)
save_button.grid(row=6, column=1, pady=5)

view_button = tk.Button(root, text="View Saved Passwords", command=view_passwords)
view_button.grid(row=7, column=0, columnspan=2, pady=10)

root.mainloop()