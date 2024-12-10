import tkinter as tk
import time
import ttkbootstrap as ttk
import sqlite3
from datetime import datetime

class Pomodoro:
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