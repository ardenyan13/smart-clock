import tkinter as tk
import sqlite3
import requests
from datetime import datetime
import threading
from dotenv import load_dotenv
import os

class Widget:
    def __init__(self, root):
        load_dotenv()

        # create random task label
        self.main_label = tk.Label(root, text="", font=("Helvetica", 16))
        self.main_label.pack(pady=30)

        # show the text on the label
        self.update_main_label()

    def update_main_label(self):
        # start api call in separate thread
        threading.Thread(target=self.get_task_and_update_label).start()

    def get_task_and_update_label(self):
        # get a random task from the db
        task = self.get_task_from_db()

        # update label on main thread
        self.main_label.after(0, self.update_label_text, task)
    
    def update_label_text(self, task):
        # update label
        if task:
            text = f"One of your upcoming tasks:\n\n{task}"
        else:
            text = "No upcoming tasks"

        # text += f"\n\n{self.get_random_word()}"

        self.main_label.config(text=text)

        # schedule function to be called again after 10 seconds
        self.main_label.after(10000, self.update_main_label)

    def get_task_from_db(self):
        # create database or connect to it
        conn = sqlite3.connect("smart_clock.db")

        # create cursor
        cursor = conn.cursor()

        # query for random task
        cursor.execute("SELECT * FROM tasks ORDER BY RANDOM() LIMIT 1")
        task = cursor.fetchone()

        # Close the connection
        conn.close()

        if task:
            # unpack tuple
            task_id, description, start_time, time_period, date = task
            
            # convert date back to MM/DD/YYYY
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%m/%d/%y")

            # convert time back to 12 hour
            time_obj = datetime.strptime(start_time, "%H:%M")
            formatted_time = time_obj.strftime("%I:%M")

            formatted_task = f"{description} | {formatted_time} {time_period} | {formatted_date}"

            return formatted_task
        
        else:
            return ""

    def get_random_word(self):
        # random word url
        word_url = "https://word-generator2.p.rapidapi.com/"

        querystring = {"count":"1"}

        headers = {
	        "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"), # get the api key from enviornment variable
	        "x-rapidapi-host": "word-generator2.p.rapidapi.com"
        }

        # definition url
        definition_url = "https://api.dictionaryapi.dev/api/v2/entries/en/"
        
        try:
            word_response = requests.get(word_url, headers=headers, params=querystring)
            word_response.raise_for_status()
            word_data = word_response.json()
            words = word_data["body"] # get the words
            word = words[0] # get the first word

            definition_response = requests.get(definition_url + word) # append the word to the definition api call
            definition_response.raise_for_status()
            definition_data = definition_response.json()
            definition = definition_data[0]["meanings"][0]["definitions"][0]["definition"]

            if len(definition) > 50:
                return f"{word}: {definition[0:50]}\n{definition[50:]}"

            return f"{word}: {definition}"
        
        except Exception as e:
            return ""