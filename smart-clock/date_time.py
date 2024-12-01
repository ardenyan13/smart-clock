import tkinter as tk
import time

class DateTime:
    def __init__(self, root):
        self.root = root

        # create date label
        self.date_label = tk.Label(root, text="", font=("Helvetica", 24))
        self.date_label.pack(pady=10)

        # create time label
        self.time_label = tk.Label(root, text="", font=("Helvetica", 48))
        self.time_label.pack(pady=10)

        self.update_time()

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