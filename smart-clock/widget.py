import tkinter as tk
import sqlite3
# import requests
from datetime import datetime

class Widget:
    def __init__(self, root):
        # create knowledge and wellness label
        self.main_label = tk.Label(root, text="", font=("Helvetica", 16))
        self.main_label.pack(pady=30)

        # show the text on the label
        self.update_main_label()

    def update_main_label(self):
        # get a random task from the database
        task = self.get_task_from_db()

        # update label
        if task:
            self.main_label.config(text=f"One of your upcoming tasks:\n\n{task}")
        else:
            self.main_label.config(text="No upcoming tasks")

        # schedule function to be called again after 20 seconds
        self.main_label.after(20000, self.get_task_from_db)

        # random word definition here
        # # get the definition of a random word and update the label
        # self.get_definition(task)
        # # schedule function to be called again after 20 seconds
        # self.main_label.after(20000, self.update_main_label)

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

    # def get_definition(self, task):
    #     # random word url
    #     word_url = "https://random-word-api.herokuapp.com/word"

    #     # definition url
    #     definition_url = "https://api.dictionaryapi.dev/api/v2/entries/en/"
        
    #     try:
    #         word_response = requests.get(word_url)
    #         word_response.raise_for_status()
    #         word_data = word_response.json() # json response example: ["reduplicate"]
    #         word = word_data[0] # get the word

    #         definition_response = requests.get(definition_url + word) # append the word to the definition api call
    #         definition_response.raise_for_status()
    #         definition_data = definition_response.json()
    #         definition = definition_data[0]["meanings"][0]["definitions"][0]["definition"]

    #         # update label
    #         if task:
    #             combined_text = f"One of your upcoming tasks:\n\n{task}\n\nWord: {word}\n Definition: {definition}"
    #         else:
    #             combined_text = f"No upcoming tasks\n\n{word}: {definition}"
            
    #         # update the label
    #         self.main_label.config(text=combined_text)

    #     except requests.RequestException as e:
    #         self.main_label.config(text="")