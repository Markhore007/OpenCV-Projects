import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDEO_PATH = os.path.join(BASE_DIR, "video.mp4")
OUTPUT_PATH = os.path.join(BASE_DIR, "output.mp4")
CSV_PATH = os.path.join(BASE_DIR, "traffic_report.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "yolov8n.pt")

os.makedirs(MODEL_DIR, exist_ok=True)

# YOLO and Tracker settings
# Classes: 2: car, 3: motorcycle, 5: bus, 7: truck
TARGET_CLASSES = [2, 3, 5, 7]
CONFIDENCE_THRESHOLD = 0.3
TRACKER_TYPE = "botsort.yaml"

# Line configuration for counting
# Assuming 1080p, adjust these based on the actual video
# We use a horizontal line roughly across the middle of the frame
COUNTING_LINE_Y = 540  # Mid point vertically for 1080p
COUNTING_LINE_START = (0, COUNTING_LINE_Y)
COUNTING_LINE_END = (1920, COUNTING_LINE_Y)

# Direction Logic
# If y increases (top to bottom), vehicle is going IN
# If y decreases (bottom to top), vehicle is going OUT

# Display settings
SHOW_WINDOW = True
