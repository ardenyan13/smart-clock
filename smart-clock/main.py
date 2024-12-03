import tkinter as tk
from date_time import DateTime
from to_do_list import ToDoList

def show_date_time():
    # remove all widgets and display the date and time page
    for widget in root.winfo_children():
        widget.pack_forget()
    date_time = DateTime(root, show_to_do_list)

def show_to_do_list():
    # remove all widgets and display the to do list page
    for widget in root.winfo_children():
        widget.pack_forget()
    to_do_list = ToDoList(root, show_date_time)

def main():
    # make root global so the functions can access it
    global root
    root = tk.Tk()
    root.title("Smart Clock")
    root.geometry("1200x900")

    # initally show the date and time page
    show_date_time()
    
    root.mainloop()

if __name__ == "__main__":
    main()