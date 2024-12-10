import tkinter as tk
import time
from widget import Widget

class DateTime:
    def __init__(self, root, show_to_do_list, show_alarms):
        # create date label
        self.date_label = tk.Label(root, text="", font=("Helvetica", 24))
        self.date_label.pack(pady=10)

        # create time label
        self.time_label = tk.Label(root, text="", font=("Helvetica", 48))
        self.time_label.pack(pady=10)

        # call update_time() to display the correct info
        self.update_time()

        # create to do list button that will switch to the to do list page
        self.to_do_list_button = tk.Button(root, text="To Do List", font=("Helvetica", 20), command=show_to_do_list)
        self.to_do_list_button.pack(pady=10)

        # create alarms button that will switch to the alarms page
        self.alarm_button = tk.Button(root, text="Alarms", font=("Helvetica", 20), command=show_alarms)
        self.alarm_button.pack(pady=10)

        # create pomodoro timer button that will switch to the pomodoro timer page
        self.pomodoro_button = tk.Button(root, text="Pomodoro Timer", font=("Helvetica", 20))
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