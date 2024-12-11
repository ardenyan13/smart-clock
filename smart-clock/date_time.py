import tkinter as tk
import time
import ttkbootstrap as ttk
from widget import Widget
import sqlite3
from background_alarm import BackgroundAlarm

class DateTime:
    def __init__(self, root, show_to_do_list, show_alarms, show_pomodoro):
        # initialize the background alarm checker
        self.background_alarm = BackgroundAlarm(root)

        # create date label
        self.date_label = tk.Label(root, text="", font=("Helvetica", 24))
        self.date_label.pack(pady=10)

        # create time label
        self.time_label = tk.Label(root, text="", font=("Helvetica", 48))
        self.time_label.pack(pady=10)

        # call update_time() to display the correct info
        self.update_time()

        # create a shabbat mode toggle check button
        self.shabbat_mode_var = tk.BooleanVar(value=self.get_curr_shabbat_mode()) # variable to hold the current shabbat mode setting
        self.shabbat_mode_button = ttk.Checkbutton(root, text="Shabbat Mode", style="Roundtoggle.Toolbutton", variable=self.shabbat_mode_var, command=self.change_shabbat_mode)
        self.shabbat_mode_button.pack(pady=10)

        # create to do list button that will switch to the to do list page
        self.to_do_list_button = tk.Button(root, text="To Do List", font=("Helvetica", 20), command=show_to_do_list)
        self.to_do_list_button.pack(pady=10)

        # create alarms button that will switch to the alarms page
        self.alarm_button = tk.Button(root, text="Alarms", font=("Helvetica", 20), command=show_alarms)
        self.alarm_button.pack(pady=10)

        # create pomodoro timer button that will switch to the pomodoro timer page
        self.pomodoro_button = tk.Button(root, text="Pomodoro Timer", font=("Helvetica", 20), command=show_pomodoro)
        self.pomodoro_button.pack(pady=10)

        # create random task and word definitin widget
        self.random_widget = Widget(root)

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
    
    def change_shabbat_mode(self):
        # get the state from button and save it to database
        state = self.shabbat_mode_var.get()
        self.save_shabbat_mode(state)

        # let the background process know the shabbat mode was changed
        self.background_alarm.update_shabbat_mode()
    
    def save_shabbat_mode(self, state):
        conn = sqlite3.connect("smart_clock.db")
        cursor = conn.cursor()

        # delete the old shabbat mode and then insert the new state
        cursor.execute("DELETE FROM shabbat")
        cursor.execute("INSERT INTO shabbat (enabled) VALUES (?)", (state,))

        conn.commit()
        conn.close()
    
    def get_curr_shabbat_mode(self):
        conn = sqlite3.connect("smart_clock.db")
        cursor = conn.cursor()

        # query the shabbat mode state
        cursor.execute("SELECT enabled FROM shabbat")
        result = cursor.fetchone()

        conn.commit()
        conn.close()

        if (result):
            return bool(result[0])
        else:
            return False