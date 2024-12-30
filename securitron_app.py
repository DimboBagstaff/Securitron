# securitron_app.py

from capture import camera
from messenger import telebot

import os
import dotenv

dotenv.load_dotenv(override=True)

print("=== Running Securitron ===")

chatbot = telebot(
    os.environ.get("BOT_TOKEN"), 
    os.environ.get("CHAT_ID"), 
    os.environ.get("ADMIN_ID")
    )

if __name__ == "__main__":

    drivecam = camera(
        name="drivecam",
        ip=os.environ.get("DRIVECAM_IP"),
        port=os.environ.get("DRIVECAM_PORT"),
        username=os.environ.get("DRIVECAM_USERNAME"),
        password=os.environ.get("DRIVECAM_PASSWORD"),
        channel=os.environ.get("DRIVECAM_CHANNEL"),
        chatbot=chatbot,

        sensitivity=0.2,
        inference_interval=10,
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