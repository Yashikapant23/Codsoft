# todo.py

tasks = []

def show_menu():
    print("\n===== TO-DO LIST MENU =====")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Mark Task as Done")
    print("4. Delete Task")
    print("5. Exit")

def add_task():
    task = input("Enter task: ")
    tasks.append({"task": task, "done": False})
    print("Task added.")

def view_tasks():
    if not tasks:
        print("No tasks yet.")
    else:
        print("\nYour tasks:")
        for idx, t in enumerate(tasks, start=1):
            status = "✅" if t["done"] else "❌"
            print(f"{idx}. {t['task']} [{status}]")

def mark_done():
    view_tasks()
    try:
        num = int(input("Enter task number to mark done: "))
        if 1 <= num <= len(tasks):
            tasks[num - 1]["done"] = True
            print("Task marked as done.")
        else:
            print("Invalid number.")
    except ValueError:
        print("Invalid input.")

def delete_task():
    view_tasks()
    try:
        num = int(input("Enter task number to delete: "))
        if 1 <= num <= len(tasks):
            removed = tasks.pop(num - 1)
            print(f"Deleted: {removed['task']}")
        else:
            print("Invalid number.")
    except ValueError:
        print("Invalid input.")

# main loop
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
