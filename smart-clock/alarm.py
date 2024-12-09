import tkinter as tk
import time
import ttkbootstrap as ttk
import sqlite3
from datetime import datetime

class Alarm:
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
        
        # create a frame for the alarms list
        self.alarms_frame = tk.Frame(root)
        self.alarms_frame.pack(pady=10)

        # create a label and listbox for alarms list
        self.alarms_listbox_label = tk.Label(self.alarms_frame, text="Alarms:", font=("Helvetica", 24))
        self.alarms_listbox_label.pack(pady=10)
        self.alarms_listbox = tk.Listbox(self.alarms_frame, width=80, height=20, bd=0, highlightthickness=0, 
                                        highlightcolor="#a6a6a6", activestyle="none", selectmode=tk.MULTIPLE)
        self.alarms_listbox.pack(side=tk.LEFT, fill=tk.BOTH, pady=10)

        # create scrollbar for listbox
        scrollbar = tk.Scrollbar(self.alarms_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

        # add the scroll bar to the listbox
        self.alarms_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.alarms_listbox.yview)

        # create a frame for to do alarm buttons
        self.alarm_buttons_frame = tk.Frame(root)
        self.alarm_buttons_frame.pack(pady=10)

        # create alarm button
        self.create_alarm_button = tk.Button(self.alarm_buttons_frame, text="Create Alarm", font=("Helvetica", 16), command=self.show_create_alarm)
        self.create_alarm_button.pack(side=tk.LEFT, padx=20)

        # delete alarm button
        self.delete_alarm_button = tk.Button(self.alarm_buttons_frame, text="Delete Alarm", font=("Helvetica", 16), command=self.delete_alarm)
        self.delete_alarm_button.pack(side=tk.LEFT, padx=20)

        # create a frame for new alarm and edit alarm entry area
        self.alarm_entry_frame = tk.Frame(root)
        self.alarm_entry_frame.pack(pady=10)

        self.update_alarm_list()
    
    def show_create_alarm(self):
        # clear the entry area
        self.clear_alarm_entry_frame()

        # create entry for creating alarm
        self.create_alarm_label = tk.Label(self.alarm_entry_frame, text="Alarm Description (Optional)", font=("Helvetica", 16))
        self.create_alarm_label.pack(pady=5)
        self.create_alarm_entry = tk.Entry(self.alarm_entry_frame, width=40)
        self.create_alarm_entry.pack(pady=5)

        # create frame for the alarm time entries
        self.alarm_time_frame = tk.Frame(self.alarm_entry_frame)
        self.alarm_time_frame.pack(pady=5)

        # create spinboxes for alarm hour and minute
        self.alarm_time_label = tk.Label(self.alarm_time_frame, text="Set Alarm Time", font=("Helvetica", 16))
        self.alarm_time_label.pack(pady=5)
        self.alarm_hour_spinbox = tk.Spinbox(self.alarm_time_frame, from_=1, to=12, width=3, format="%02.0f")
        self.alarm_hour_spinbox.pack(side=tk.LEFT, padx=5)
        self.alarm_minute_spinbox = tk.Spinbox(self.alarm_time_frame, from_=0, to=59, width=3, format="%02.0f")
        self.alarm_minute_spinbox.pack(side=tk.LEFT, padx=5)

        # create AM/PM radio box (limited to one selection by the 'variable' parameter)
        self.time_period = tk.StringVar(value="AM")
        self.am_radio_button = tk.Radiobutton(self.alarm_time_frame, text="AM", variable=self.time_period, value="AM")
        self.pm_radio_button = tk.Radiobutton(self.alarm_time_frame, text="PM", variable=self.time_period, value="PM")
        self.am_radio_button.pack(side=tk.LEFT, padx=5)
        self.pm_radio_button.pack(side=tk.LEFT, padx=5)

        # create date selector
        self.date_entry = ttk.DateEntry(self.alarm_time_frame)
        self.date_entry.pack(side=tk.LEFT, padx=5)

        # add task to to do list button
        self.create_task_button = tk.Button(self.alarm_entry_frame, text="Add Alarm", command=self.add_alarm)
        self.create_task_button.pack(pady=5)

        # cancel create task button
        self.cancel_button = tk.Button(self.alarm_entry_frame, text="Cancel", command=self.clear_alarm_entry_frame)
        self.cancel_button.pack(pady=5)
    
    def clear_alarm_entry_frame(self):
        # remove all widgets from the new alarm and edit alarm entry frame
        for widget in self.alarm_entry_frame.winfo_children():
            widget.destroy()
    
    def add_alarm(self):
        # get the text from the create alarm entry box
        description = self.create_alarm_entry.get()
        time_period = self.time_period.get()
        alarm_hour = int(self.alarm_hour_spinbox.get())

        # format the time in 24 hour to store in database
        if time_period == "PM" and alarm_hour != 12:
            alarm_hour += 12
        if time_period == "AM" and alarm_hour == 12:
            alarm_hour = 0
        formatted_alarm_time = f"{alarm_hour:02}:{self.alarm_minute_spinbox.get()}"

        date = self.date_entry.entry.get()

        # format the date in YYYY-MM-DD in database
        date_obj = datetime.strptime(date, "%m/%d/%y")
        formatted_date = date_obj.strftime("%Y-%m-%d")

        # check if the alarm time fields are filled
        if formatted_alarm_time and date:
            if not description:
                self.add_alarm_to_db("", formatted_alarm_time, time_period, formatted_date)
            else:
                self.add_alarm_to_db(description, formatted_alarm_time, time_period, formatted_date)
            self.update_alarm_list() # update the alarm list to display the new alarm
            self.clear_alarm_entry_frame() # clear the entry area

    def delete_alarm(self):
        # get the index of the selected alarm(s)
        selected_alarm_indices = self.alarms_listbox.curselection()

        # check if an alarm was selected
        if selected_alarm_indices:
            # query the alarms
            alarms = self.get_alarms_from_db()
            # delete every alarm that was selected
            for i in selected_alarm_indices[::-1]: # delete in reverse order to avoid index issues
                alarm_id = alarms[i][0]
                self.delete_alarm_from_db(alarm_id)
            
            # update the alarm list to reflect changes
            self.update_alarm_list()

    def update_alarm_list(self):
        # remove everything from the listbox
        self.alarms_listbox.delete(0, tk.END)

        # add every alarm in the db to the alarm list
        for alarm in self.get_alarms_from_db():
            # convert date back to MM/DD/YYYY
            date_obj = datetime.strptime(alarm[4], "%Y-%m-%d")
            formatted_date = date_obj.strftime("%m/%d/%y")

            # convert time back to 12 hour
            time_obj = datetime.strptime(alarm[2], "%H:%M")
            formatted_time = time_obj.strftime("%I:%M")

            # check if the alarm has a description (the string to be displayed differs)
            if (alarm[1]):
                full_task = f"{alarm[1]} | {formatted_time} {alarm[3]} | {formatted_date}" 
            else:
                full_task = f"{formatted_time} {alarm[3]} | {formatted_date}"
            
            self.alarms_listbox.insert(tk.END, full_task)

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
    
    def add_alarm_to_db(self, description, alarm_time, time_period, date):
        # create database or connect to it
        conn = sqlite3.connect("smart_clock.db")

        # create cursor
        cursor = conn.cursor()

        # insert into alarms table
        cursor.execute("""INSERT INTO alarms (description, alarm_time, time_period, date)
                       VALUES (?, ?, ?, ?)
                       """, (description, alarm_time, time_period, date))
        
        # get the inserted alarm's id
        alarm_id = cursor.lastrowid

        # commit changes
        conn.commit()

        # close connection
        conn.close()

        return alarm_id

    def get_alarms_from_db(self):
        conn = sqlite3.connect("smart_clock.db")
        cursor = conn.cursor()

        # query the alarms table
        cursor.execute("SELECT * FROM alarms ORDER BY date, alarm_time, description")

        # get all the alarms (will return a list of tuples)
        alarms = cursor.fetchall()
        for alarm in alarms:
            print(alarm)

        conn.commit()
        conn.close()

        return alarms

    def delete_alarm_from_db(self, alarm_id):
        conn = sqlite3.connect("smart_clock.db")
        cursor = conn.cursor()

        # query the tasks table
        cursor.execute("DELETE FROM alarms WHERE id = ?", (alarm_id,))

        conn.commit()
        conn.close()