import tkinter as tk
import time
import ttkbootstrap as ttk
import sqlite3
from datetime import datetime

DESCRIPTION_KEY = "description"
START_TIME_KEY = "start_time"
TIME_PERIOD_KEY = "time_period"
DATE_KEY = "date"

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

        # delete task button
        self.delete_task_button = tk.Button(self.task_buttons_frame, text="Delete Task", font=("Helvetica", 16), command=self.delete_task)
        self.delete_task_button.pack(side=tk.LEFT, padx=20)

        # create a frame for new task and edit task entry area
        self.task_entry_frame = tk.Frame(root)
        self.task_entry_frame.pack(pady=10)

        self.update_to_do_list()

    def show_create_task(self):
        # clear the entry area
        self.clear_task_entry_frame()

        # create entry for creating task
        self.create_task_label = tk.Label(self.task_entry_frame, text="Task Description", font=("Helvetica", 16))
        self.create_task_label.pack(pady=5)
        self.create_task_entry = tk.Entry(self.task_entry_frame, width=40)
        self.create_task_entry.pack(pady=5)

        # create frame for the start time entries
        self.start_time_frame = tk.Frame(self.task_entry_frame)
        self.start_time_frame.pack(pady=5)

        # create spinboxes for start hour and minute
        self.start_time_label = tk.Label(self.start_time_frame, text="Start Time", font=("Helvetica", 16))
        self.start_time_label.pack(pady=5)
        self.start_hour_spinbox = tk.Spinbox(self.start_time_frame, from_=1, to=12, width=3, format="%02.0f")
        self.start_hour_spinbox.pack(side=tk.LEFT, padx=5)
        self.start_minute_spinbox = tk.Spinbox(self.start_time_frame, from_=0, to=59, width=3, format="%02.0f")
        self.start_minute_spinbox.pack(side=tk.LEFT, padx=5)

        # create AM/PM radio box (limited to one selection by the 'variable' parameter)
        self.time_period = tk.StringVar(value="AM")
        self.am_radio_button = tk.Radiobutton(self.start_time_frame, text="AM", variable=self.time_period, value="AM")
        self.pm_radio_button = tk.Radiobutton(self.start_time_frame, text="PM", variable=self.time_period, value="PM")
        self.am_radio_button.pack(side=tk.LEFT, padx=5)
        self.pm_radio_button.pack(side=tk.LEFT, padx=5)

        # create date selector
        self.date_entry = ttk.DateEntry(self.start_time_frame)
        self.date_entry.pack(side=tk.LEFT, padx=5)

        # add task to to do list button
        self.create_task_button = tk.Button(self.task_entry_frame, text="Add Task", command=self.add_task)
        self.create_task_button.pack(pady=5)

        # cancel create task button
        self.cancel_button = tk.Button(self.task_entry_frame, text="Cancel", command=self.clear_task_entry_frame)
        self.cancel_button.pack(pady=5)
    
    def clear_task_entry_frame(self):
        # remove all widgets from the new task and edit task entry frame
        for widget in self.task_entry_frame.winfo_children():
            widget.destroy()

    def add_task(self):
        # get the text from the create task entry box
        description = self.create_task_entry.get()
        time_period = self.time_period.get()
        start_hour = int(self.start_hour_spinbox.get())

        # format the time in 24 hour to store in database
        if time_period == "PM" and start_hour != 12:
            start_hour += 12
        if time_period == "AM" and start_hour == 12:
            start_hour = 0
        start_time = f"{start_hour:02}:{self.start_minute_spinbox.get()}"

        date = self.date_entry.entry.get()

        # format the date in YYYY-MM-DD in database
        date_obj = datetime.strptime(date, "%m/%d/%y")
        formatted_date = date_obj.strftime("%Y-%m-%d")

        # check if all fields are filled
        if description != "" and start_time and time_period and date:
            task_id = self.add_task_to_db(description, start_time, time_period, formatted_date)
            self.update_to_do_list() # update the to do list to display the new task
            self.clear_task_entry_frame() # clear the entry area

    
    def delete_task(self):
        # get the index of the selected task(s)
        selected_task_indices = self.tasks_listbox.curselection()

        # check if a task was selected
        if selected_task_indices:
            # query the tasks
            tasks = self.get_tasks_from_db()
            # delete every task that was selected
            for i in selected_task_indices[::-1]: # delete in reverse order to avoid index issues
                task_id = tasks[i][0]
                self.delete_task_from_db(task_id)
            
            # update the to do list to reflect changes
            self.update_to_do_list()

    def update_to_do_list(self):
        # remove everything from the listbox
        self.tasks_listbox.delete(0, tk.END)

        # add every task in the list to the to do list
        for task in self.get_tasks_from_db():
            # convert date back to MM/DD/YYYY
            date_obj = datetime.strptime(task[4], "%Y-%m-%d")
            formatted_date = date_obj.strftime("%m/%d/%y")

            # convert time back to 12 hour
            time_obj = datetime.strptime(task[2], "%H:%M")
            formatted_time = time_obj.strftime("%I:%M")

            full_task = f"{task[1]} | {formatted_time} {task[3]} | {formatted_date}"
            self.tasks_listbox.insert(tk.END, full_task)

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

    def add_task_to_db(self, description, start_time, time_period, date):
        # create database or connect to it
        conn = sqlite3.connect("smart_clock.db")

        # create cursor
        cursor = conn.cursor()

        # insert into tasks table
        cursor.execute("""INSERT INTO tasks (description, start_time, time_period, date)
                       VALUES (?, ?, ?, ?)
                       """, (description, start_time, time_period, date))
        
        # get the inserted task's id
        task_id = cursor.lastrowid

        # commit changes
        conn.commit()

        # close connection
        conn.close()

        return task_id
    
    def get_tasks_from_db(self):
        conn = sqlite3.connect("smart_clock.db")
        cursor = conn.cursor()

        # query the tasks table
        cursor.execute("SELECT * FROM tasks ORDER BY date, start_time")

        # get all the tasks (will return a list of tuples)
        tasks = cursor.fetchall()

        conn.commit()
        conn.close()

        return tasks
    
    def delete_task_from_db(self, task_id):
        conn = sqlite3.connect("smart_clock.db")
        cursor = conn.cursor()

        # query the tasks table
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

        conn.commit()
        conn.close()