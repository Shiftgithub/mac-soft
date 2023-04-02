from tkinter import *
from tkinter import messagebox
import mysql.connector

# Create a new window
root = Tk()
root.title("Task Manager")
root.geometry("800x600")
root.config(bg="#E5E5E5")

# Define the task list
tasks = []
# Create a connection to the MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="todonote"
)

# Create a cursor to execute SQL queries
mycursor = mydb.cursor()
# Function to add a new task to the list


def add_task():
    name = name_entry.get()
    deadline = deadline_entry.get()
    status = status_var.get()
    if name and deadline:
        task = {"name": name, "deadline": deadline, "status": status}
        tasks.append(task)
        sql = "INSERT INTO tasks (name, deadline, status) VALUES (%s, %s, %s)"
        val = (name, deadline, status)
        mycursor.execute(sql, val)
        mydb.commit()
        update_task_list()
    else:
        messagebox.showerror("Error", "Please enter task name and deadline.")

# Function to edit a task in the list


def edit_task():
    selected_task = task_list.curselection()
    if selected_task:
        task = tasks[selected_task[0]]
        task["name"] = name_entry.get()
        task["deadline"] = deadline_entry.get()
        task["status"] = status_var.get()
        sql = "UPDATE tasks SET name = %s, deadline = %s, status = %s WHERE id = %s"
        val = (name_entry.get(), deadline_entry.get(),
               status_var.get(), task["id"])
        mycursor.execute(sql, val)
        mydb.commit()
        update_task_list()

# Function to delete a task from the list


def delete_task():
    selected_task = task_list.curselection()
    if selected_task:
        task = tasks[selected_task[0]]
        sql = "DELETE FROM tasks WHERE id = %s"
        val = (task["id"],)
        mycursor.execute(sql, val)
        mydb.commit()
        tasks.pop(selected_task[0])
        update_task_list()

# Function to update the task list


def update_task_list():
    task_list.delete(0, END)
    mycursor.execute("SELECT * FROM tasks")
    rows = mycursor.fetchall()
    for row in rows:
        task = {"id": row[0], "name": row[1],
                "deadline": row[2], "status": row[3]}
        tasks.append(task)
        task_list.insert(
            END, f"{task['name']} - {task['deadline']} - {task['status']}")


# Create a label for the task list
task_list_label = Label(root, text="Task List",
                        font=("Arial Bold", 16), bg="#E5E5E5")
task_list_label.grid(row=0, column=0, padx=10, pady=10)

# Create a listbox for the task list
task_list = Listbox(root, font=("Arial", 12), width=50)
task_list.grid(row=1, column=0, padx=20, pady=(0, 10), columnspan=2)

# Create a label for the task form
task_form_label = Label(root, text="Task Form",
                        font=("Arial Bold", 16), bg="#E5E5E5")
task_form_label.grid(row=0, column=2, padx=10, pady=10)

# Create a label for the task name
name_label = Label(root, text="Task Name", font=("Arial", 12), bg="#E5E5E5")
name_label.grid(row=1, column=2, padx=10, pady=10, sticky=W)

# Create a label for the task name
name_label = Label(root, text="Task Name", font=("Arial", 12))
name_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

# Create an entry for the task name
name_entry = Entry(root, font=("Arial", 12))
name_entry.grid(row=2, column=1, padx=10, pady=10)

# Create a label for the deadline
deadline_label = Label(root, text="Deadline", font=("Arial", 12))
deadline_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

# Create an entry for the deadline
deadline_entry = Entry(root, font=("Arial", 12))
deadline_entry.grid(row=3, column=1, padx=10, pady=10)

# Create a label for the status
status_label = Label(root, text="Status", font=("Arial", 12))
status_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")

# Create a variable for the status
status_var = StringVar()
status_var.set("Not Started")

# Create a radio button for the not started status
not_started_radio = Radiobutton(
    root, text="Not Started", variable=status_var, value="Not Started", font=("Arial", 12))
not_started_radio.grid(row=5, column=0, padx=10, pady=10, sticky="w")

# Create a radio button for the in progress status
in_progress_radio = Radiobutton(
    root, text="In Progress", variable=status_var, value="In Progress", font=("Arial", 12))
in_progress_radio.grid(row=6, column=0, padx=10, pady=10, sticky="w")

# Create a radio button for the completed status
completed_radio = Radiobutton(
    root, text="Completed", variable=status_var, value="Completed", font=("Arial", 12))
completed_radio.grid(row=7, column=0, padx=10, pady=10, sticky="w")

# Create a button to add a task
add_button = Button(root, text="Add Task", command=add_task, font=(
    "Arial", 12), bg="green", fg="white", activebackground="darkgreen", activeforeground="white")
add_button.grid(row=8, column=0, padx=10, pady=10, sticky="w")

# Create a button to edit a task
edit_button = Button(root, text="Edit Task", command=edit_task, font=(
    "Arial", 12), bg="orange", fg="white", activebackground="darkorange", activeforeground="white")
edit_button.grid(row=8, column=1, padx=10, pady=10, sticky="e")

# Create a button to delete a task
delete_button = Button(root, text="Delete Task", command=delete_task, font=(
    "Arial", 12), bg="red", fg="white", activebackground="darkred", activeforeground="white")
delete_button.grid(row=8, column=2, padx=10, pady=10, sticky="e")
# Update the task list
update_task_list()

root.mainloop()
