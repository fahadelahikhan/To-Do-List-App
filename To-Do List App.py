import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime


class TodoApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Task Manager")
        self.window.geometry("500x600")
        self.window.minsize(400, 500)
        self.setup_ui()

    def setup_ui(self):
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')

        # Main frame
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights for responsiveness
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="Task Manager",
                                font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Input section
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)

        self.task_entry = ttk.Entry(input_frame, font=('Arial', 11))
        self.task_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.task_entry.bind('<Return>', self.add_task)

        self.add_btn = ttk.Button(input_frame, text="Add Task", command=self.add_task)
        self.add_btn.grid(row=0, column=1)

        # Task list with scrollbar
        list_frame = ttk.Frame(main_frame)
        list_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        # Create listbox with scrollbar
        self.task_listbox = tk.Listbox(list_frame, selectmode=tk.SINGLE,
                                       font=('Arial', 10), height=15)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.task_listbox.yview)
        self.task_listbox.configure(yscrollcommand=scrollbar.set)

        self.task_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=(10, 0))

        self.remove_btn = ttk.Button(button_frame, text="Remove Selected",
                                     command=self.remove_task, state='disabled')
        self.remove_btn.grid(row=0, column=0, padx=(0, 10))

        self.clear_btn = ttk.Button(button_frame, text="Clear All",
                                    command=self.clear_all_tasks)
        self.clear_btn.grid(row=0, column=1, padx=(0, 10))

        self.mark_done_btn = ttk.Button(button_frame, text="Mark Done",
                                        command=self.mark_task_done, state='disabled')
        self.mark_done_btn.grid(row=0, column=2)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var,
                               relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))

        # Bind listbox selection event
        self.task_listbox.bind('<<ListboxSelect>>', self.on_task_select)

        # Focus on entry
        self.task_entry.focus()

    def add_task(self, event=None):
        task_text = self.task_entry.get().strip()
        if task_text:
            # Add timestamp for better organization
            timestamp = datetime.now().strftime("%H:%M")
            formatted_task = f"[{timestamp}] {task_text}"

            self.task_listbox.insert(tk.END, formatted_task)
            self.task_entry.delete(0, tk.END)
            self.update_status(f"Task added: {task_text}")
            self.update_button_states()
        else:
            messagebox.showwarning("Warning", "Please enter a task!")

    def remove_task(self):
        try:
            selected_indices = self.task_listbox.curselection()
            if selected_indices:
                index = selected_indices[0]
                task_text = self.task_listbox.get(index)
                self.task_listbox.delete(index)
                self.update_status(f"Task removed: {task_text.split('] ', 1)[-1]}")
                self.update_button_states()
            else:
                messagebox.showinfo("Info", "Please select a task to remove!")
        except tk.TclError:
            messagebox.showerror("Error", "Failed to remove task!")

    def mark_task_done(self):
        try:
            selected_indices = self.task_listbox.curselection()
            if selected_indices:
                index = selected_indices[0]
                current_task = self.task_listbox.get(index)

                if not current_task.startswith("✓"):
                    completed_task = f"✓ {current_task}"
                    self.task_listbox.delete(index)
                    self.task_listbox.insert(index, completed_task)
                    self.task_listbox.selection_set(index)
                    self.update_status("Task marked as completed!")
                else:
                    messagebox.showinfo("Info", "Task is already marked as done!")
            else:
                messagebox.showinfo("Info", "Please select a task to mark as done!")
        except tk.TclError:
            messagebox.showerror("Error", "Failed to mark task as done!")

    def clear_all_tasks(self):
        if self.task_listbox.size() > 0:
            result = messagebox.askyesno("Confirm", "Are you sure you want to clear all tasks?")
            if result:
                self.task_listbox.delete(0, tk.END)
                self.update_status("All tasks cleared!")
                self.update_button_states()
        else:
            messagebox.showinfo("Info", "No tasks to clear!")

    def on_task_select(self, event):
        self.update_button_states()

    def update_button_states(self):
        has_selection = bool(self.task_listbox.curselection())
        has_tasks = self.task_listbox.size() > 0

        self.remove_btn.config(state='normal' if has_selection else 'disabled')
        self.mark_done_btn.config(state='normal' if has_selection else 'disabled')
        self.clear_btn.config(state='normal' if has_tasks else 'disabled')

    def update_status(self, message):
        self.status_var.set(message)
        self.window.after(3000, lambda: self.status_var.set("Ready"))

    def run(self):
        self.window.mainloop()


# Create and run the application
if __name__ == "__main__":
    app = TodoApp()
    app.run()