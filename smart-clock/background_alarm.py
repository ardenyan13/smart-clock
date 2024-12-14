import tkinter as tk
import time
import sqlite3
from datetime import datetime, timedelta
import threading
import pygame
from astral.sun import sun
from astral import LocationInfo
import pytz  # Added for timezone handling

class BackgroundAlarm:
    def __init__(self, root):
        self.root = root

        # Set the alarm ringing boolean to false
        self.alarm_ringing = False

        # Initialize Shabbat mode state
        self.shabbat_mode_enabled = False

        # Set static location (Bay Area)
        self.location = LocationInfo("San Jose", "USA", "America/Los_Angeles", 37.3382, -121.8863)

        # Initialize Shabbat and holiday times
        self.update_shabbat_and_holiday_times()

        # Start the alarm checking thread
        self.start_alarm_checker()

        # Start Shabbat mode checker thread
        self.start_shabbat_mode_checker()

    def update_shabbat_and_holiday_times(self):
        today = datetime.now()
        friday = today + timedelta((4 - today.weekday()) % 7)  # Get next Friday
        saturday = friday + timedelta(days=1)

        # Calculate sunset for Friday (Shabbat start) and Saturday (Shabbat end)
        shabbat_times = sun(self.location.observer, date=friday, tzinfo=self.location.timezone)
        self.shabbat_start = shabbat_times["sunset"]

        shabbat_times_end = sun(self.location.observer, date=saturday, tzinfo=self.location.timezone)
        self.shabbat_end = shabbat_times_end["sunset"] + timedelta(minutes=42)  # Add 42 minutes for nightfall

        print(f"Shabbat starts: {self.shabbat_start}")
        print(f"Shabbat ends: {self.shabbat_end}")

    def update_shabbat_mode_automatically(self):
        """Automatically enable/disable Shabbat mode based on Shabbat times."""
        timezone = pytz.timezone(self.location.timezone)  # Convert string to tzinfo object
        now = datetime.now(timezone)  # Make 'now' timezone-aware
        # Enable Shabbat mode if current time is during Shabbat
        if self.shabbat_start <= now <= self.shabbat_end:
            self.shabbat_mode_enabled = True
        else:
            self.shabbat_mode_enabled = False

    def start_shabbat_mode_checker(self):
        """Start a thread to periodically check and update Shabbat mode."""
        def shabbat_checker():
            while True:
                # Update Shabbat and holiday times daily
                self.update_shabbat_and_holiday_times()
                # Automatically toggle Shabbat mode
                self.update_shabbat_mode_automatically()
                # Check every 5 minutes
                time.sleep(3600)

        threading.Thread(target=shabbat_checker, daemon=True).start()

    def get_alarms_from_db(self):
        conn = sqlite3.connect("smart_clock.db")
        cursor = conn.cursor()

        # Query the alarms table
        cursor.execute("SELECT * FROM alarms ORDER BY date, alarm_time, description")

        # Get all the alarms (will return a list of tuples)
        alarms = cursor.fetchall()

        conn.commit()
        conn.close()

        return alarms

    def show_alarm_popup(self, alarm):
        self.alarm_ringing = True

        # Thread to play alarm sound
        threading.Thread(target=self.play_alarm_sound).start()

        # Create alarm popup window
        popup = tk.Toplevel(self.root)
        popup.title("Alarm")
        popup.geometry("600x450")
        
        # Create label
        alarm_label = tk.Label(popup, text="", font=("Helvetica", 20))
        alarm_label.pack(pady=5)

        # Format the alarm string
        date_obj = datetime.strptime(alarm[4], "%Y-%m-%d")
        formatted_date = date_obj.strftime("%m/%d/%y")
        time_obj = datetime.strptime(alarm[2], "%H:%M")
        formatted_time = time_obj.strftime("%I:%M %p")

        if alarm[1]:
            full_alarm = f"{alarm[1]} | {formatted_time} {alarm[3]} | {formatted_date}" 
        else:
            full_alarm = f"{formatted_time} {alarm[3]} | {formatted_date}"

        alarm_label.config(text=f"Alarm!\n{full_alarm}")

        # Create silence button
        silence_button = tk.Button(popup, text="Silence Alarm", command=lambda: self.silence_alarm(popup))
        silence_button.pack(pady=5)

        # Automatically silence the alarm popup in Shabbat mode
        if self.shabbat_mode_enabled:
            popup.after(5000, lambda: self.silence_alarm(popup))

    def play_alarm_sound(self):
        pygame.mixer.init()
        pygame.mixer.music.load("alarm.wav")
        pygame.mixer.music.play(-1)  # Loop indefinitely while alarm is ringing
        while self.alarm_ringing:
            time.sleep(1)

    def silence_alarm(self, popup):
        self.alarm_ringing = False
        pygame.mixer.music.stop()
        popup.destroy()

    def check_alarms(self):
        while True:
            # Get the current time
            curr_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            # Compare each alarm in database to the current time
            for alarm in self.get_alarms_from_db():
                alarm_time = f"{alarm[4]} {alarm[2]}"
                if curr_time == alarm_time and not alarm[5]:
                    self.set_alarm_triggered(alarm[0])  # Mark the alarm as triggered
                    self.show_alarm_popup(alarm)
                    break
            time.sleep(1)
    
    def set_alarm_triggered(self, alarm_id):
        conn = sqlite3.connect("smart_clock.db")
        cursor = conn.cursor()

        # Update alarm triggered column in database
        cursor.execute("UPDATE alarms SET triggered = 1 WHERE id = ?", (alarm_id,))
        conn.commit()
        conn.close()

    def start_alarm_checker(self):
        threading.Thread(target=self.check_alarms, daemon=True).start()
