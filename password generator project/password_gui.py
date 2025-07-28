import tkinter as tk
from tkinter import messagebox
import random
import string

def generate_password():
    try:
        length = int(length_entry.get())
        if length < 4:
            messagebox.showwarning("Warning", "Password length should be at least 4 characters.")
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
            messagebox.showerror("Error", "Please select at least one character set.")
            return
        
        password = ''.join(random.choice(characters) for _ in range(length))
        password_var.set(password)
        evaluate_strength(password)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number.")

def copy_password():
    root.clipboard_clear()
    root.clipboard_append(password_var.get())
    messagebox.showinfo("Copied", "Password copied to clipboard!")

def save_password():
    password = password_var.get()
    if password == "":
        messagebox.showwarning("Warning", "No password to save.")
        return
    try:
        with open("saved_passwords.txt", "a") as f:
            f.write(password + "\n")
        messagebox.showinfo("Saved", "Password saved to saved_passwords.txt")
    except Exception as e:
        messagebox.showerror("Error", f"Could not save: {e}")

def evaluate_strength(password):
    strength = "Weak"
    color = "red"
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)
    
    if len(password) >= 12 and has_upper and has_lower and has_digit and has_special:
        strength = "Strong"
        color = "green"
    elif len(password) >= 8 and ((has_upper and has_lower) or (has_lower and has_digit)):
        strength = "Medium"
        color = "orange"
        
    strength_label.config(text=f"Strength: {strength}", fg=color)

# main window
root = tk.Tk()
root.title("Password Generator")

# labels and entries
tk.Label(root, text="Enter password length:").grid(row=0, column=0, padx=10, pady=5)
length_entry = tk.Entry(root)
length_entry.grid(row=0, column=1, padx=10, pady=5)

# checkboxes for complexity
uppercase_var = tk.BooleanVar(value=True)
lowercase_var = tk.BooleanVar(value=True)
digits_var = tk.BooleanVar(value=True)
special_var = tk.BooleanVar(value=True)

tk.Checkbutton(root, text="Include Uppercase", variable=uppercase_var).grid(row=1, column=0, sticky="w", padx=10)
tk.Checkbutton(root, text="Include Lowercase", variable=lowercase_var).grid(row=1, column=1, sticky="w", padx=10)
tk.Checkbutton(root, text="Include Digits", variable=digits_var).grid(row=2, column=0, sticky="w", padx=10)
tk.Checkbutton(root, text="Include Special Characters", variable=special_var).grid(row=2, column=1, sticky="w", padx=10)

# generate button
generate_button = tk.Button(root, text="Generate Password", command=generate_password)
generate_button.grid(row=3, column=0, columnspan=2, pady=10)

# password display
password_var = tk.StringVar()
password_entry = tk.Entry(root, textvariable=password_var, width=40)
password_entry.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# password strength label
strength_label = tk.Label(root, text="Strength: ", font=("Helvetica", 12, "bold"))
strength_label.grid(row=5, column=0, columnspan=2, pady=5)

# copy button
copy_button = tk.Button(root, text="Copy to Clipboard", command=copy_password)
copy_button.grid(row=6, column=0, pady=5)

# save button
save_button = tk.Button(root, text="Save to File", command=save_password)
save_button.grid(row=6, column=1, pady=5)

root.mainloop()
