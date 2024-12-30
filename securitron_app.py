# securitron_app.py

from capture import camera
from messenger import telebot

import os
import dotenv
import time

dotenv.load_dotenv(override=True)

if __name__ == "__main__":

    print("=== Running Securitron ===")

    chatbot = telebot(
        os.environ.get("BOT_TOKEN"), 
        os.environ.get("CHAT_ID"), 
        os.environ.get("ADMIN_ID")
        )

    drivecam = camera(
        name="drivecam",
        ip=os.environ.get("DRIVECAM_IP"),
        port=os.environ.get("DRIVECAM_PORT"),
        username=os.environ.get("DRIVECAM_USERNAME"),
        password=os.environ.get("DRIVECAM_PASSWORD"),
        channel=os.environ.get("DRIVECAM_CHANNEL"),
        chatbot=chatbot,

        sensitivity=0.2,
        inference_interval=3,
    )

    # doorcam = camera(
    #     name="doorcam",
    #     ip=os.environ.get("DOORCAM_IP"),
    #     port=os.environ.get("DOORCAM_PORT"),
    #     username=os.environ.get("DOORCAM_USERNAME"),
    #     password=os.environ.get("DOORCAM_PASSWORD"),
    #     channel=os.environ.get("DOORCAM_CHANNEL"),
    #     chatbot=chatbot,

    #     sensitivity=0.2,
    #     inference_interval=60,
    # )

    # Keep the main program running
    try:
        while True:
            time.sleep(1000)
    except KeyboardInterrupt:
        print("\nExiting program.")