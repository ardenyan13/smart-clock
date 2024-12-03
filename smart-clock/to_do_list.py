import tkinter as tk
import time

class ToDoList:
    def __init__(self, root, show_date_time):
        # frame for date and time at the top of the page
        self.date_time_frame = tk.Frame(root)
        self.date_time_frame.pack(pady=10)

        # create date label
        self.date_label = tk.Label(self.date_time_frame, text="", font=("Helvetica", 16))
        self.date_label.pack(side=tk.LEFT, padx=20)

        # create time label
        self.time_label = tk.Label(self.date_time_frame, text="", font=("Helvetica", 16))
        self.time_label.pack(side=tk.LEFT, padx=20)
        
        # call update_time() to display the correct info
        self.update_time()

        # crate button to go back to home page
        self.date_time_button = tk.Button(root, text="Home", font=("Helvetica", 20), command=show_date_time)
        self.date_time_button.pack()
        
        # create a frame for the to do list
        self.tasks_frame = tk.Frame(root)
        self.tasks_frame.pack(pady=10)

        # list to hold tasks
        self.tasks = []

        # create a label and listbox for to do list
        self.tasks_listbox_label = tk.Label(self.tasks_frame, text="Tasks to Do:", font=("Helvetica", 24))
        self.tasks_listbox_label.pack(pady=10)
        self.tasks_listbox = tk.Listbox(self.tasks_frame, width=80, height=20, bd=0, highlightthickness=0, 
                                        highlightcolor="#a6a6a6", activestyle="none", selectmode=tk.MULTIPLE)
        self.tasks_listbox.pack(side=tk.LEFT, fill=tk.BOTH, pady=10)

        # create scrollbar for listbox
        scrollbar = tk.Scrollbar(self.tasks_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

        # add the scroll bar to the listbox
        self.tasks_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tasks_listbox.yview)

        # create a frame for to do list buttons
        self.task_buttons_frame = tk.Frame(root)
        self.task_buttons_frame.pack(pady=10)

        # create task button
        self.create_task_button = tk.Button(self.task_buttons_frame, text="Create Task", font=("Helvetica", 16), command=self.show_create_task)
        self.create_task_button.pack(side=tk.LEFT, padx=20)

        # edit task button
        self.edit_task_button = tk.Button(self.task_buttons_frame, text="Edit Task", font=("Helvetica", 16), command=self.show_update_task)
        self.edit_task_button.pack(side=tk.LEFT, padx=20)

        # delete task button
        self.delete_task_button = tk.Button(self.task_buttons_frame, text="Delete Task", font=("Helvetica", 16), command=self.delete_task)
        self.delete_task_button.pack(side=tk.LEFT, padx=20)

        # create a frame for new task and edit task entry area
        self.task_entry_frame = tk.Frame(root)
        self.task_entry_frame.pack(pady=10)

    def show_create_task(self):
        # clear the entry area
        self.clear_task_entry_frame()

        # create entry for creating task
        self.create_task_entry = tk.Entry(self.task_entry_frame, width=40)
        self.create_task_entry.pack(pady=5)

        # add task to to do list button
        self.create_task_button = tk.Button(self.task_entry_frame, text="Add Task", command=self.add_task)
        self.create_task_button.pack(pady=5)

        # cancel create task button
        self.cancel_button = tk.Button(self.task_entry_frame, text="Cancel", command=self.clear_task_entry_frame)
        self.cancel_button.pack(pady=5)
    
    def show_update_task(self):
        # clear the entry area
        self.clear_task_entry_frame()

        # get the index of the selected task
        selected_task_index = self.tasks_listbox.curselection()

        # check if a task was selected
        if selected_task_index:
            # since we allow multiple selections, we only need the first index task from those selected
            selected_task_index = selected_task_index[0]

            # create entry for the task to be updated
            self.task_update_entry = tk.Entry(self.task_entry_frame, width=40)
            self.task_update_entry.insert(0, self.tasks[selected_task_index]) # put the selected task in the entry in case of edit for typos
            self.task_update_entry.pack(pady=5)

            # update task in to do list button
            self.update_task_button = tk.Button(self.task_entry_frame, text="Update Task", command=lambda: self.update_selected_task(selected_task_index))
            self.update_task_button.pack(pady=5)

            # cancel update tasks button
            self.cancel_button = tk.Button(self.task_entry_frame, text="Cancel", command=self.clear_task_entry_frame)
            self.cancel_button.pack(pady=5)
    
    def clear_task_entry_frame(self):
        # remove all widgets from the new task and edit task entry frame
        for widget in self.task_entry_frame.winfo_children():
            widget.destroy()

    def add_task(self):
        # get the text from the create task entry box
        task = self.create_task_entry.get()

        # check if there is text
        if task != "":
            self.tasks.append(task) # add the tasks to the list (will be changed to database later)
            self.update_to_do_list() # update the to do list to display the new task
            self.clear_task_entry_frame() # clear the entry area
    
    def update_selected_task(self, task_index):
        # get the text from the update task entry box
        updated_task = self.task_update_entry.get()

        # check if there is text
        if updated_task != "":
            self.tasks[task_index] = updated_task # update the task in the list (will be changed to database later)
            self.update_to_do_list() # update the to do list to display the new task
            self.clear_task_entry_frame() # clear the entry area
    
    def delete_task(self):
        # get the index of the selected task(s)
        selected_task_indices = self.tasks_listbox.curselection()

        # check if a task was selected
        if selected_task_indices:
            # delete every task that was selected
            for i in selected_task_indices[::-1]: # delete in reverse order to avoid index issues
                del self.tasks[i]
            
            # update the to do list to reflect changes
            self.update_to_do_list()

    def update_to_do_list(self):
        # remove everything from the listbox
        self.tasks_listbox.delete(0, tk.END)

        # add every task in the list to the to do list
        for task in self.tasks:
            self.tasks_listbox.insert(tk.END, task)

    def update_time(self):
        # get the current time
        current_time = time.strftime("%I:%M %p")  # format time

        # remove leading zero for the hours 1-9
        if current_time[0] == '0':
            current_time = current_time[1:]
        
        # get the current date
        current_date = time.strftime("%A, %B %d, %Y")  # format date

        # adjust labels to display date and time
        self.date_label.config(text=current_date)
        self.time_label.config(text=current_time)

        # schedule function to be called again after 1 second
        self.time_label.after(1000, self.update_time)