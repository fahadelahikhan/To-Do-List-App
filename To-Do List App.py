import tkinter as tk
from tkinter import messagebox


class TodoApp:
    def __init__(self):
        # Create the main window
        self.window = tk.Tk()
        self.window.title("My To-Do List")
        self.window.geometry("400x500")  # Set initial window size
        self.window.minsize(350, 400)  # Set minimum window size

        # Configure the window to be resizable
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)

        # Create the main frame
        self.main_frame = tk.Frame(self.window)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Initialize instance attributes that will be created in setup_widgets
        self.task_listbox = None
        self.task_entry = None
        self.count_label = None

        self.setup_widgets()

    def setup_widgets(self):
        # Title label
        title_label = tk.Label(
            self.main_frame,
            text="My To-Do List",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 10))

        # Frame for the listbox and scrollbar
        listbox_frame = tk.Frame(self.main_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Create scrollbar for the listbox
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create listbox with scrollbar
        self.task_listbox = tk.Listbox(
            listbox_frame,
            selectmode=tk.SINGLE,
            yscrollcommand=scrollbar.set,
            font=("Arial", 10),
            height=15
        )
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.task_listbox.yview)

        # Frame for entry and add button
        entry_frame = tk.Frame(self.main_frame)
        entry_frame.pack(fill=tk.X, pady=(0, 10))

        # Entry widget for new tasks
        self.task_entry = tk.Entry(
            entry_frame,
            font=("Arial", 10),
            width=30
        )
        self.task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        # Bind Enter key to add task
        self.task_entry.bind('<Return>', lambda event: self.add_task())

        # Add task button
        add_btn = tk.Button(
            entry_frame,
            text="Add Task",
            command=self.add_task,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 9, "bold")
        )
        add_btn.pack(side=tk.RIGHT)

        # Frame for action buttons
        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X)

        # Remove task button
        remove_btn = tk.Button(
            button_frame,
            text="Remove Selected Task",
            command=self.remove_task,
            bg="#f44336",
            fg="white",
            font=("Arial", 9, "bold")
        )
        remove_btn.pack(side=tk.LEFT, padx=(0, 5))

        # Clear all tasks button
        clear_btn = tk.Button(
            button_frame,
            text="Clear All Tasks",
            command=self.clear_all_tasks,
            bg="#FF9800",
            fg="white",
            font=("Arial", 9, "bold")
        )
        clear_btn.pack(side=tk.LEFT)

        # Task count label
        self.count_label = tk.Label(
            button_frame,
            text="Tasks: 0",
            font=("Arial", 9),
            fg="gray"
        )
        self.count_label.pack(side=tk.RIGHT)

    def add_task(self):
        """Add a new task to the list"""
        task_text = self.task_entry.get().strip()

        if task_text:
            # Check if task already exists
            current_tasks = self.task_listbox.get(0, tk.END)
            if task_text in current_tasks:
                messagebox.showwarning("Duplicate Task", "This task already exists!")
                return

            # Add the task to the listbox
            self.task_listbox.insert(tk.END, task_text)
            self.task_entry.delete(0, tk.END)
            self.update_task_count()

            # Auto-scroll to the bottom to show new task
            self.task_listbox.see(tk.END)
        else:
            messagebox.showwarning("Empty Task", "Please enter a task before adding!")

    def remove_task(self):
        """Remove the selected task from the list"""
        selected_indices = self.task_listbox.curselection()

        if selected_indices:
            # Get the selected task text for confirmation
            selected_task = self.task_listbox.get(selected_indices[0])

            # Ask for confirmation
            confirm = messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to remove:\n'{selected_task}'?"
            )

            if confirm:
                self.task_listbox.delete(selected_indices[0])
                self.update_task_count()
        else:
            messagebox.showinfo("No Selection", "Please select a task to remove!")

    def clear_all_tasks(self):
        """Clear all tasks from the list"""
        if self.task_listbox.size() > 0:
            confirm = messagebox.askyesno(
                "Clear All Tasks",
                "Are you sure you want to remove all tasks?"
            )

            if confirm:
                self.task_listbox.delete(0, tk.END)
                self.update_task_count()
        else:
            messagebox.showinfo("Empty List", "There are no tasks to clear!")

    def update_task_count(self):
        """Update the task count display"""
        count = self.task_listbox.size()
        self.count_label.config(text=f"Tasks: {count}")

    def run(self):
        """Start the application"""
        # Focus on the entry widget when app starts
        self.task_entry.focus()
        # Update initial task count
        self.update_task_count()
        # Start the main event loop
        self.window.mainloop()


# Create and run the application
if __name__ == "__main__":
    app = TodoApp()
    app.run()