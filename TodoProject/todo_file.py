import json
import os

FILENAME = "tasks.json"
tasks = []

def load_tasks():
    global tasks
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r") as f:
                tasks = json.load(f)
        except json.JSONDecodeError:
            print("Error loading tasks. Starting with an empty list.")
            tasks = []
    else:
        tasks = []

def save_tasks():
    with open(FILENAME, "w") as f:
        json.dump(tasks, f)

def show_menu():
    print("\n===== TO-DO LIST MENU =====")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Mark Task as Done")
    print("4. Delete Task")
    print("5. Exit")

def add_task():
    task = input("Enter task: ").strip()
    if task:
        tasks.append({"task": task, "done": False})
        save_tasks()
        print("Task added.")
    else:
        print("Task cannot be empty.")

def view_tasks():
    if not tasks:
        print("No tasks yet.")
    else:
        print("\nYour tasks:")
        for idx, t in enumerate(tasks, start=1):
            status = "[Done]" if t["done"] else "[Pending]"
            print(f"{idx}. {t['task']} {status}")

def mark_done():
    if not tasks:
        print("No tasks to mark as done.")
        return
    view_tasks()
    try:
        num = int(input("Enter task number to mark done: "))
        if 1 <= num <= len(tasks):
            tasks[num - 1]["done"] = True
            save_tasks()
            print("Task marked as done.")
        else:
            print("Invalid number.")
    except ValueError:
        print("Invalid input.")

def delete_task():
    if not tasks:
        print("No tasks to delete.")
        return
    view_tasks()
    try:
        num = int(input("Enter task number to delete: "))
        if 1 <= num <= len(tasks):
            removed = tasks.pop(num - 1)
            save_tasks()
            print(f"Deleted: {removed['task']}")
        else:
            print("Invalid number.")
    except ValueError:
        print("Invalid input.")

# Main loop
load_tasks()

while True:
    show_menu()
    choice = input("Choose an option: ")
    if choice == "1":
        add_task()
    elif choice == "2":
        view_tasks()
    elif choice == "3":
        mark_done()
    elif choice == "4":
        delete_task()
    elif choice == "5":
        print("Goodbye!")
        break
    else:
        print("Invalid choice.")