import tkinter as tk
import time

def update_time(label_time, label_date):
    current_time = time.strftime("%I:%M %p")  # format time
    if current_time[0] == '0':  # remove leading zero for the hours 1-9
        current_time = current_time[1:]
    current_date = time.strftime("%A, %B %d, %Y")  # format date
    label_time.config(text=current_time)
    label_date.config(text=current_date)
    # schedule function to be called again after 1 second
    label_time.after(1000, update_time, label_time, label_date)

def main():
    root = tk.Tk()
    root.title("Smart Clock")
    root.geometry("1200x900")

    # date label
    label_date = tk.Label(root, text="", font=("Helvetica", 24))
    label_date.pack(pady=10)
    
    # time label
    label_time = tk.Label(root, text="", font=("Helvetica", 48))
    label_time.pack(pady=10)
    
    update_time(label_time, label_date)
    
    root.mainloop()

if __name__ == "__main__":
    main()