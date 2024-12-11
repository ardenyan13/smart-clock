import tkinter as tk
from date_time import DateTime
from to_do_list import ToDoList
from alarm import Alarm
from pomodoro import Pomodoro
from background_alarm import BackgroundAlarm
import ttkbootstrap as ttk
import sqlite3

# import os
# os.environ['SDL_AUDIODRIVER'] = 'pulse'

def show_date_time():
    # remove all widgets and display the date and time page
    for widget in root.winfo_children():
        if isinstance(widget, tk.Toplevel):
            continue
        widget.pack_forget()
    date_time = DateTime(root, show_to_do_list, show_alarms, show_pomodoro)

def show_to_do_list():
    # remove all widgets and display the to do list page
    for widget in root.winfo_children():
        if isinstance(widget, tk.Toplevel):
            continue
        widget.pack_forget()
    to_do_list = ToDoList(root, show_date_time)

def show_alarms():
    for widget in root.winfo_children():
        if isinstance(widget, tk.Toplevel):
            continue
        widget.pack_forget()
    alarm = Alarm(root, show_date_time)

def show_pomodoro():
    for widget in root.winfo_children():
        if isinstance(widget, tk.Toplevel):
            continue
        widget.pack_forget()
    pomodoro = Pomodoro(root, show_date_time)

def create_tables():
    # create database or connect to it
    conn = sqlite3.connect("smart_clock.db")

    # create cursor
    cursor = conn.cursor()

    # create to do list table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT,
        start_time TEXT,
        time_period TEXT,
        date TEXT
    )
    """)

    # create alarm table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alarms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT,
        alarm_time TEXT,
        time_period TEXT,
        date TEXT,
        triggered BOOLEAN DEFAULT 0
    )
    """)

    # create shabbat mode tabel
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shabbat (
            enabled BOOLEAN DEFAULT 0
    )
    """)

    # create an initial default shabbat mode if this is the first time running main
    cursor.execute("INSERT INTO shabbat (enabled) SELECT 0 WHERE NOT EXISTS (SELECT 1 FROM shabbat)")

    # commit changes
    conn.commit()

    # close connection
    conn.close()

def main():
    # make root global so the functions can access it
    global root
    root = ttk.Window(themename="litera")
    root.title("Smart Clock")
    root.geometry("1200x900")

    # initialize the background alarm checker
    background_alarm = BackgroundAlarm(root)

    # initally show the date and time page
    show_date_time()
    
    root.mainloop()

if __name__ == "__main__":
    create_tables()
    main()