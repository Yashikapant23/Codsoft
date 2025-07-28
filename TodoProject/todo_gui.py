import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

FILENAME = "tasks.json"
tasks = []
edit_index = None

def load_tasks():
    global tasks
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as f:
            tasks = json.load(f)
    else:
        tasks = []

def save_tasks():
    with open(FILENAME, "w") as f:
        json.dump(tasks, f)

def refresh_list(display=None):
    if display is None:
        display = tasks
    for row in task_tree.get_children():
        task_tree.delete(row)
    for idx, t in enumerate(display):
        status = "✅" if t["done"] else "❌"
        priority = t["priority"]
        due = t["due_date"]
        tag = priority.lower()
        task_tree.insert(
            "",
            "end",
            iid=idx,
            values=(t["task"], status, due, priority),
            tags=(tag,)
        )

def add_task():
    global edit_index
    name = task_entry.get()
    due = due_entry.get()
    priority = priority_entry.get().capitalize()
    if priority not in ["High", "Medium", "Low"]:
        priority = "Medium"
    if name == "" or due == "":
        messagebox.showwarning("Warning", "Task and due date cannot be empty!")
        return
    try:
        datetime.strptime(due, "%Y-%m-%d")  # validate date
    except ValueError:
        messagebox.showerror("Error", "Due date must be YYYY-MM-DD")
        return
    if edit_index is None:
        tasks.append({"task": name, "due_date": due, "priority": priority, "done": False})
    else:
        tasks[edit_index]["task"] = name
        tasks[edit_index]["due_date"] = due
        tasks[edit_index]["priority"] = priority
        edit_index = None
        add_button.config(text="Add Task")
    save_tasks()
    refresh_list()
    task_entry.delete(0, tk.END)
    due_entry.delete(0, tk.END)
    priority_entry.delete(0, tk.END)

def mark_done():
    selected = task_tree.selection()
    if selected:
        idx = int(selected[0])
        tasks[idx]["done"] = True
        save_tasks()
        refresh_list()
    else:
        messagebox.showwarning("Warning", "No task selected")

def delete_task():
    selected = task_tree.selection()
    if selected:
        idx = int(selected[0])
        tasks.pop(idx)
        save_tasks()
        refresh_list()
    else:
        messagebox.showwarning("Warning", "No task selected")

def search_tasks():
    keyword = search_entry.get().lower()
    filtered = []
    for t in tasks:
        if keyword in t["task"].lower() or keyword in t["priority"].lower():
            filtered.append(t)
    refresh_list(filtered)

def clear_search():
    search_entry.delete(0, tk.END)
    refresh_list()

def edit_task():
    global edit_index
    selected = task_tree.selection()
    if selected:
        idx = int(selected[0])
        edit_index = idx
        task_entry.delete(0, tk.END)
        due_entry.delete(0, tk.END)
        priority_entry.delete(0, tk.END)
        task_entry.insert(0, tasks[idx]["task"])
        due_entry.insert(0, tasks[idx]["due_date"])
        priority_entry.insert(0, tasks[idx]["priority"])
        add_button.config(text="Update Task")
    else:
        messagebox.showwarning("Warning", "No task selected")

def show_reminders():
    today = datetime.today().date()
    overdue = []
    due_today = []
    for t in tasks:
        try:
            due_date = datetime.strptime(t["due_date"], "%Y-%m-%d").date()
            if not t["done"]:
                if due_date < today:
                    overdue.append(t["task"])
                elif due_date == today:
                    due_today.append(t["task"])
        except Exception:
            continue
    if overdue:
        messagebox.showwarning("Overdue Tasks", f"The following tasks are overdue:\n{chr(10).join(overdue)}")
    if due_today:
        messagebox.showinfo("Due Today", f"The following tasks are due today:\n{chr(10).join(due_today)}")

# Load tasks at startup
load_tasks()

# Create window
root = tk.Tk()
root.title("To-Do List")

# Entry fields
tk.Label(root, text="Task").grid(row=0, column=0)
task_entry = tk.Entry(root, width=30)
task_entry.grid(row=0, column=1)

tk.Label(root, text="Due Date (YYYY-MM-DD)").grid(row=1, column=0)
due_entry = tk.Entry(root, width=30)
due_entry.grid(row=1, column=1)

tk.Label(root, text="Priority (High/Medium/Low)").grid(row=2, column=0)
priority_entry = tk.Entry(root, width=30)
priority_entry.grid(row=2, column=1)

# Buttons
add_button = tk.Button(root, text="Add Task", command=add_task)
add_button.grid(row=3, column=0, columnspan=2, pady=5)

mark_done_button = tk.Button(root, text="Mark Done", command=mark_done)
mark_done_button.grid(row=4, column=0, pady=5)

delete_button = tk.Button(root, text="Delete Task", command=delete_task)
delete_button.grid(row=4, column=1, pady=5)

edit_button = tk.Button(root, text="Edit Task", command=edit_task)
edit_button.grid(row=5, column=0, columnspan=2, pady=5)

# Search box
tk.Label(root, text="Search").grid(row=6, column=0)
search_entry = tk.Entry(root, width=30)
search_entry.grid(row=6, column=1)

search_button = tk.Button(root, text="Search", command=search_tasks)
search_button.grid(row=7, column=0)

clear_button = tk.Button(root, text="Clear Search", command=clear_search)
clear_button.grid(row=7, column=1)

# Treeview for task list
columns = ("Task", "Status", "Due Date", "Priority")
task_tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
for col in columns:
    task_tree.heading(col, text=col)
task_tree.grid(row=8, column=0, columnspan=2, pady=10)

# Add color tags
task_tree.tag_configure("high", foreground="red")
task_tree.tag_configure("medium", foreground="orange")
task_tree.tag_configure("low", foreground="green")

refresh_list()
show_reminders()

root.mainloop()
