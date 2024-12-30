# capture.py

import os
import time
import cv2
import shutil
import threading
from datetime import datetime
from pathlib import Path

from inference import *

class camera():
    """Automatically collects frames and saves mp4 videos to data folder"""
    def __init__(self, name, ip, port, username, password, channel, folder=None, 
                 chatbot=None, sensitivity=0.2, inference_interval=3, video_duration=60):
        self.name = name
        self.folder = Path("data") / (folder or self.name)

        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.channel = channel
        self.chatbot = chatbot

        self.save_video = True
        self.save_images = True
        self.cleanup_interval = 3600
        
        self.cam = self.connect_camera()
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        
        self.sensitivity = sensitivity
        self.inference_interval = inference_interval
        self.video_duration = video_duration
        
        self.previous_frame = None
        self.frames = []

        threading.Thread(target=self.run_inference_loop, daemon=True).start()
        threading.Thread(target=self.update, daemon=True).start()
        threading.Thread(target=self.cleanup, daemon=True).start()

    def update(self, frame_delay=0.025):
        """Background thread grabbing every frame, saving video every x frames"""

        timestamp = datetime.now()
        epoch = (time.time() // self.video_duration) 
        while True:
            ret, frame = self.cam.read()
            if ret:
                if ((time.time() // self.video_duration) > epoch):
                    epoch += 1
                    print("Creating video...")
                    self.create_vibeo(timestamp)

                    timestamp = datetime.now()
                    self.frames = [frame]
                else:
                    self.frames.append(frame)
                
            time.sleep(frame_delay)

    def run_inference_loop(self):
        """Process a frame every inference_interval"""

        interval = (time.time() // self.inference_interval) 
        while True:
            ts = datetime.now()
            self.process_frame(ts)
            interval += 1
            time.sleep((interval * self.inference_interval) - time.time())

    def cleanup(self, max_folders=3):
        """Delete old recordings to save space"""

        interval = (time.time() // self.cleanup_interval) 
        while True:
            delete_folders = sorted([f for f in os.listdir(self.folder)])

            for f in delete_folders[:-max_folders]:
                print(f"Deleting folder {self.folder / f}")
                shutil.rmtree(self.folder / f)
            interval += 1
            time.sleep((interval * self.cleanup_interval) - time.time())


    def send_message(self, message):
        if self.chatbot is not None:
            self.chatbot.message(message)

    def send_photo(self, photo):
        if self.chatbot is not None:
            photoBytes = cv2.imencode('.png', photo)[1].tobytes()
            res = self.chatbot.photo(photoBytes)
            print(res)

    def connect_camera(self):
        """Connect to camera using class parameters"""

        cam = cv2.VideoCapture(f'rtsp://{self.username}:{self.password}@{self.ip}:{self.port}/{self.channel}')
        assert cam.isOpened(), "Camera failed to connect!"
        return cam

    def get_filename(self, timestamp=None, ext=".png"):
        """Create filename using current timestamp"""
        
        if timestamp is None:
            timestamp = datetime.now()

        subfolder = self.folder / timestamp.strftime("%Y%m%d") / timestamp.strftime(f"%H")
        os.makedirs(subfolder, exist_ok=True)

        fpath = subfolder / timestamp.strftime(f"{self.name} %Y%m%d_%Hh%Mm%Ss{ext}")
        return fpath

    def process_frame(self, timestamp):
        """Capture and save an image"""

        if len(self.frames) == 0:
            return False
        
        image = self.frames[-1]
        fpath = self.get_filename(timestamp)

        new_frame = resize(image)
        if (self.previous_frame is not None):
            diff = compare(
                new_frame, 
                self.previous_frame
            )

            print(f"Image change: {diff}")
            if diff > self.sensitivity:
                # If hit -> save frame (with bounding boxes ideally...)
                self.send_photo(new_frame)

                if self.save_images: 
                    cv2.imwrite(fpath, image)
                    print(f"Saved frame to {fpath}")

        self.previous_frame = new_frame

    def create_vibeo(self, timestamp):
        """Save the current frames into an mp4 video"""

        if not self.save_video: 
            return None
        
        fname = self.get_filename(timestamp, ext=".mp4")
        print(f"Creating video... {fname}")

        height, width, layers = self.frames[0].shape
        fps = len(self.frames) / (datetime.now().timestamp() - timestamp.timestamp())

        video = cv2.VideoWriter(fname, self.fourcc, fps, (width,height))

        for image in self.frames:
            video.write(image)

        print("Video saved successfully.")

# if __name__ == "__main__":
#     print("Launching camera script")
#     cam = camera("testcam")
#     cam.run_inference_loop(10)