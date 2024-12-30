# messenger.py

import os
import sys
import time
import requests
import datetime
import json

import threading

DEBUG = True

HELPTXT = """
Friendly neighbourhood Telegram bot.

Functionality
- post messages to chat
- log everything
- perform commands from chat

Commands:
- help: list all commands
- reboot: restart pi
- addcam: add camera details
- delcam: delete camera details
- pull: pull updates from github repo
- exec: execute command text in python
- status: post status of pi, storage details
"""

class telebot():
    def __init__(self, ID, chat_ID=None, admin_ID=None, check_interval=10):
        self.ID = ID
        self.chat_ID = chat_ID
        self.admin_ID = admin_ID or chat_ID
        self.command_timestamp = None
        self.check_interval = check_interval
        print("*beep boop* Initialized telegram robit *beep boop*")

        self.message(f"Online @ {datetime.datetime.now().strftime('%H:%M:%S %d/%m/%y')}")
        self.check_messages(execute=False)

        threading.Thread(target=self.check_loop, daemon=True).start()

    def check_loop(self):
        """Check for messages every check_interval"""

        interval = (time.time() // self.check_interval) 
        while True:
            self.check_messages()
            interval += 1
            time.sleep((interval * self.check_interval) - time.time())


    def message(self, message):
        """Send a text message"""

        url = f"https://api.telegram.org/bot{self.ID}/sendMessage"
        print("Sending message:", message)
        payload = {
            "chat_id": self.admin_ID,
            "text": message
        }
        response = requests.post(url, json=payload)

        return response.json()

    def photo(self, photo):
        """Send an image, pass the photo file in binary mode"""
        
        url = f"https://api.telegram.org/bot{self.ID}/sendPhoto"
        print("Sending photo")
        payload = {
            "chat_id": self.admin_ID,
        }
        files = {'photo': photo}

        # Send the POST request to the Telegram Bot API
        response = requests.post(url, data=payload, files=files)

        return response.json()
    
    def check_messages(self, chat_ID=None, execute=True):
        """Read messages from conversation, commands are prefixed with -"""

        if chat_ID is None:
            chat_ID = self.admin_ID
        
        url = f"https://api.telegram.org/bot{self.ID}/getUpdates"
        payload = {
            "chat_id": self.chat_ID,
        }

        response = requests.get(url, data=payload)
        content = json.loads(response.content)
        results =  content.get("result")
        new_timestamps = []

        for update in results:
            message = update.get("message", {})
            if message.get("date"):
                date = int(message.get("date"))
                new_timestamps.append(date)
                if self.command_timestamp is not None:
                    if date <= self.command_timestamp:
                        continue

                msg_txt = message.get("text")
                if msg_txt:
                    if execute:
                        self.command(msg_txt)
                    # else:
                    #     self.log("Not executing: " + msg_txt)

        if len(new_timestamps) > 0:
            if (
            (self.command_timestamp is None) or
            (max(new_timestamps) > self.command_timestamp)
            ):
                self.command_timestamp = max(new_timestamps)

    def log(self, stuff):
        self.message(stuff)
    
    def command(self, cmd_txt, ts=None):
        """Execute command"""

        self.log((cmd_txt, ts))

        try:
            if cmd_txt[0] == "-":
                cmd, *args = cmd_txt[1:].split(" ")
                if hasattr(self, cmd):
                    if args:
                        result = getattr(self, cmd)(args)
                    else:
                        result = getattr(self, cmd)()
                else:
                    result = f"Unknown command: {cmd}"

                if result:
                    self.log(result)
        except Exception as e:
            print(str(e))
            self.message(f"Error processing command: {cmd}\nError: {e}")

    def help(self):
        self.message(HELPTXT)

    def restart(self):
        self.message("Restarting application")
        time.sleep(1)
        # sys.exit()
        os._exit()

    def status(self):
        self.message("I'm online")

    def reboot(self):
        self.message("Rebooting")
        time.sleep(1)
        os.system("sudo shutdown now -r")

    def pull(self):
        self.message(f"Pulling in {os.getcwd()}")
        # response = os.system("git pull")
        response = os.system("pwd")
        self.message(str(response))