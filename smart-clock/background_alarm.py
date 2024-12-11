import tkinter as tk
import time
import ttkbootstrap as ttk
import sqlite3
from datetime import datetime
import threading
import pygame

class BackgroundAlarm:
    def __init__(self, root):
        self.root = root

        # set the alarm ringing boolean to false
        self.alarm_ringing = False

        # start the alarm checking thread
        self.start_alarm_checker()
    
    def get_alarms_from_db(self):
        conn = sqlite3.connect("smart_clock.db")
        cursor = conn.cursor()

        # query the alarms table
        cursor.execute("SELECT * FROM alarms ORDER BY date, alarm_time, description")

        # get all the alarms (will return a list of tuples)
        alarms = cursor.fetchall()

        conn.commit()
        conn.close()

        return alarms
    
    def show_alarm_popup(self, alarm):
        self.alarm_ringing = True

        # thread to play alarm sound
        threading.Thread(target=self.play_alarm_sound).start()

        # create alarm popup window
        popup = tk.Toplevel(self.root)
        popup.title("Alarm")
        popup.geometry("300x150")
        
        # create label
        alarm_label = tk.Label(popup, text="", font=("Helvetica", 20))
        alarm_label.pack(pady=5)

        # format the alarm string
        # convert date back to MM/DD/YYYY
        date_obj = datetime.strptime(alarm[4], "%Y-%m-%d")
        formatted_date = date_obj.strftime("%m/%d/%y")

        # convert time back to 12 hour
        time_obj = datetime.strptime(alarm[2], "%H:%M")
        formatted_time = time_obj.strftime("%I:%M")

        # check if the alarm has a description (the string to be displayed differs)
        if (alarm[1]):
            full_alarm = f"{alarm[1]} | {formatted_time} {alarm[3]} | {formatted_date}" 
        else:
            full_alarm = f"{formatted_time} {alarm[3]} | {formatted_date}"

        alarm_label.config(text=f"Alarm!\n{full_alarm}")

        # create dismiss button
        dismiss_button = tk.Button(popup, text="Dismiss", command=lambda: self.dismiss_alarm(popup))
        dismiss_button.pack(pady=5)

        # Bind the event for window close button (X button)
        popup.protocol("WM_DELETE_WINDOW", lambda: self.dismiss_alarm(popup))

    def play_alarm_sound(self):
        pygame.mixer.init()
        pygame.mixer.music.load("alarm.wav")
        pygame.mixer.music.play(-1)  # The -1 parameter makes the sound loop indefinitely while `self.alarm_ringing` is True
        while self.alarm_ringing:
            time.sleep(1)

    def dismiss_alarm(self, popup):
        self.alarm_ringing = False
        pygame.mixer.music.stop()
        popup.destroy()

    def check_alarms(self):
        while True:
            curr_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            for alarm in self.get_alarms_from_db():
                alarm_time = f"{alarm[4]} {alarm[2]}"
                if curr_time == alarm_time and not alarm[5]:
                    self.mark_alarm_triggered(alarm[0])  # Mark alarm as triggered
                    self.show_alarm_popup(alarm)
                    break
            time.sleep(1)
    
    def mark_alarm_triggered(self, alarm_id):
        conn = sqlite3.connect("smart_clock.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE alarms SET triggered = 1 WHERE id = ?", (alarm_id,))
        conn.commit()
        conn.close()
    
    def start_alarm_checker(self):
        threading.Thread(target=self.check_alarms, daemon=True).start()