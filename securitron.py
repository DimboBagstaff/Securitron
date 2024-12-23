from capture import camera
import os
import dotenv

dotenv.load_dotenv()

print("=== Running Securitron ===")

drivecam = camera(
    name="testcam",
    ip=os.environ.get("DRIVECAM_IP"),
    port=os.environ.get("DRIVECAM_PORT"),
    username=os.environ.get("DRIVECAM_USERNAME"),
    password=os.environ.get("DRIVECAM_PASSWORD"),
    channel=os.environ.get("DRIVECAM_CHANNEL"),
)
drivecam.run_inference_loop(10)