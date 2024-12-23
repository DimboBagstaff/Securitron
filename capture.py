# capture.py
__version__ = "1.0.0"

import os
import time
import cv2
import threading
from datetime import datetime
from pathlib import Path

class camera():
    """Automatically collects frames and saves mp4 videos to data folder"""
    def __init__(self, name, ip, port, username, password, channel, folder=None):
        self.name = name
        self.folder = Path("data") / (folder or self.name)

        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.channel = channel
        
        self.cam = self.connect_camera()
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        
        self.frames = []
        threading.Thread(target=self.update, daemon=True).start()

    def update(self, interval=0.02, nframes=1000):
        """Background thread grabbing every frame, saving video every x frames"""

        timestamp = datetime.now()
        while True:
            ret, frame = self.cam.read()
            if ret:
                # if duration < (datetime.now().timestamp() - timestamp.timestamp()):
                if len(self.frames) > nframes:
                    self.create_vibeo(timestamp)
                    timestamp = datetime.now()
                    self.frames = [frame]
                else:
                    self.frames.append(frame)
                
            time.sleep(interval)

    def connect_camera(self):
        """Connect to camera using class parameters"""

        cam = cv2.VideoCapture(f'rtsp://{self.username}:{self.password}@{self.ip}:{self.port}/{self.channel}')
        assert cam.isOpened(), "Camera failed to connect!"
        return cam

    def get_filename(self, timestamp=None, ext=".png"):
        """Create filename using current timestamp"""
        
        if timestamp is None:
            timestamp = datetime.now()

        subfolder = self.folder / timestamp.strftime("%d%m%Y") / timestamp.strftime(f"%H")
        os.makedirs(subfolder, exist_ok=True)

        fpath = subfolder / timestamp.strftime(f"{self.name} %d%m%Y_%Hh%Mm%Ss{ext}")
        return fpath

    def process_frame(self, timestamp):
        """Capture and save an image"""

        if len(self.frames) == 0:
            return False
        
        image = self.frames[-1]
        fpath = self.get_filename(timestamp)

        # TODO run inference

        # TODO Send notification

        # If hit -> save frame (with bounding boxes)
        cv2.imwrite(fpath, image)
        # print(f"Saved frame to {fpath}")

    def run_inference_loop(self, interval=3):
        """Process a frame every x seconds"""

        timestamp = datetime.now()
        while True:
            if interval < (datetime.now().timestamp() - timestamp.timestamp()):
                self.process_frame(timestamp)
                timestamp = datetime.now()


    def create_vibeo(self, timestamp):
        """Save the current frames into an mp4 video"""

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