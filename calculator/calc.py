import tkinter as tk
from tkinter import messagebox

# Function to perform calculation
def calculate():
    try:
        num1 = float(entry1.get())
        num2 = float(entry2.get())
        operation = operation_var.get()

        if operation == "Addition":
            result = num1 + num2
        elif operation == "Subtraction":
            result = num1 - num2
        elif operation == "Multiplication":
            result = num1 * num2
        elif operation == "Division":
            if num2 == 0:
                messagebox.showerror("Error", "Cannot divide by zero!")
                return
            result = num1 / num2
        else:
            messagebox.showerror("Error", "Select a valid operation")
            return

        result_label.config(text=f"Result: {result}")

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers")

# Main window
root = tk.Tk()
root.title("Simple Calculator")
root.geometry("300x300")

# Number inputs
tk.Label(root, text="Enter first number:").pack(pady=5)
entry1 = tk.Entry(root)
entry1.pack(pady=5)

tk.Label(root, text="Enter second number:").pack(pady=5)
entry2 = tk.Entry(root)
entry2.pack(pady=5)

# Dropdown for operation
operation_var = tk.StringVar(value="Addition")
tk.Label(root, text="Choose Operation:").pack(pady=5)
operations = ["Addition", "Subtraction", "Multiplication", "Division"]
operation_menu = tk.OptionMenu(root, operation_var, *operations)
operation_menu.pack(pady=5)

# Calculate button
calc_button = tk.Button(root, text="Calculate", command=calculate)
calc_button.pack(pady=10) 

# Result label
result_label = tk.Label(root, text="Result: ", font=("Arial", 14, "bold"))
result_label.pack(pady=10)

# Run the application
root.mainloop()
