import requests
import datetime
import json

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
    def __init__(self, ID, chat_ID=None, admin_ID=None):
        self.ID = ID
        self.chat_ID = chat_ID
        self.admin_ID = admin_ID or chat_ID
        self.command_timestamp = None
        print("*beep boop* Initialized telegram robit *beep boop*")

        # self.message(f"Online @ {datetime.datetime.now().strftime('%H:%M:%S %d/%m/%y')}")

        # Check messages to ignore existing messages
        self.command("-check_messages", execute=True)

    def message(self, message):
        """Send a text message"""

        url = f"https://api.telegram.org/bot{self.ID}/sendMessage"
        print("Sending message:", message)
        payload = {
            "chat_id": self.chat_ID,
            "text": message
        }
        response = requests.post(url, json=payload)

        return response.json()

    def photo(self, photo):
        """Send an image, pass the photo file in binary mode"""
        
        url = f"https://api.telegram.org/bot{self.ID}/sendPhoto"
        print("Sending photo")
        payload = {
            "chat_id": self.chat_ID,
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
        print("Reading messages")
        payload = {
            "chat_id": self.chat_ID,
        }

        response = requests.get(url, data=payload)
        content = json.loads(response.content)
        results =  content.get("results")

        for update in results:
            message = update.get("message", {})
            if message is not None:
                msg_txt = message.get("text")
                if msg_txt and execute:
                    self.command(msg_txt)
                else:
                    self.log("Not executing: " + msg_txt)


        print(response.json())

        # for message in messages...

    def log(self, stuff):
        print(stuff)
    
    def command(self, cmd_txt, ts=None):
        """Execute command"""

        self.log((cmd_txt, ts))

        if cmd_txt[0] == "-":
            cmd, *args = cmd_txt[1:].split(" ")
            if args:
                cmd = getattr(self, cmd)(args)
            else:
                cmd = getattr(self, cmd)()

        # try:

        # except Exception as e:

    def help(self):
        print(HELPTXT)
        # self.message(HELPTXT)