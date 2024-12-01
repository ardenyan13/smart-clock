import tkinter as tk
from date_time import DateTime

def main():
    root = tk.Tk()
    root.title("Smart Clock")
    root.geometry("1200x900")

    # create insatnce of DateTime
    date_time = DateTime(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()