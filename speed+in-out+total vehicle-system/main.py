import sys
import os

def startup_checks():
    print("Running startup environment checks...")
    missing_deps = []
    
    try:
        import cv2
    except ImportError:
        missing_deps.append("opencv-python")
        
    try:
        import torch
    except ImportError as e:
        print(f"\n[ERROR] Torch initialization error: {e}")
        missing_deps.append("torch")
        
    try:
        from ultralytics import YOLO
    except ImportError:
        missing_deps.append("ultralytics")
        
    if missing_deps:
        print(f"\n[CRITICAL ERROR] Missing dependencies: {', '.join(missing_deps)}")
        print("Please run the environment setup guide or use the verification script.")
        sys.exit(1)

startup_checks()

import cv2
import csv
from ultralytics import YOLO

try:
    from config import settings
except ImportError:
    print("\n[CRITICAL ERROR] Could not import config.settings.")
    sys.exit(1)

if not os.path.exists(settings.MODEL_PATH):
    print(f"\n[CRITICAL ERROR] Model file not found: {settings.MODEL_PATH}")
    sys.exit(1)
    
if not os.path.exists(settings.VIDEO_PATH):
    print(f"\n[CRITICAL ERROR] Video file not found: {settings.VIDEO_PATH}")
    sys.exit(1)

from tracker.vehicle_tracker import VehicleTracker
from utils.counter import Counter
from ui.annotator import Annotator

def main():
    # Initialize YOLO Model
    print(f"Loading YOLO model from {settings.MODEL_PATH}...")
    model = YOLO(settings.MODEL_PATH)
    
    # Initialize Tracker, Counter, Annotator
    tracker = VehicleTracker()
    counter = Counter(settings.COUNTING_LINE_Y)
    annotator = Annotator()

    # Open Video
    print(f"Opening video {settings.VIDEO_PATH}...")
    cap = cv2.VideoCapture(settings.VIDEO_PATH)
    if not cap.isOpened():
        print(f"Error: Could not open {settings.VIDEO_PATH}")
        return

    # Video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    # Open Video Writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(settings.OUTPUT_PATH, fourcc, fps, (width, height))

    # Initialize CSV Log
    with open(settings.CSV_PATH, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Vehicle Number", "Tracker ID", "Vehicle Type", "Direction", "Frame Number", "Timestamp"])

    frame_num = 0
    print("Processing video...")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_num += 1
        timestamp = frame_num / fps

        # We will keep track of vehicles on screen
        current_vehicles_on_screen = 0

        # Run YOLO with BotSort
        results = model.track(frame, persist=True, tracker=settings.TRACKER_TYPE, classes=settings.TARGET_CLASSES, conf=settings.CONFIDENCE_THRESHOLD)
        
        # We need to process the detections
        track_ids = []
        if results[0].boxes is not None and results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            track_ids = results[0].boxes.id.cpu().numpy()
            class_indices = results[0].boxes.cls.cpu().numpy()
            
            current_vehicles_on_screen = len(track_ids)

            for bbox, track_id, cls_idx in zip(boxes, track_ids, class_indices):
                x1, y1, x2, y2 = bbox
                centroid = ((x1 + x2) / 2, (y1 + y2) / 2)
                
                # Get permanent vehicle number
                vehicle_number = tracker.update(int(track_id), centroid, frame_num)
                history = tracker.get_history(vehicle_number)
                
                # Check for line crossing
                direction = counter.check_crossing(vehicle_number, history)
                
                # If crossed in this specific frame, log it
                if direction is not None and counter.vehicle_directions.get(vehicle_number) == direction and len(history) >= 2:
                    prev_y = history[-2][1]
                    curr_y = history[-1][1]
                    # Only log when the crossing JUST happened this frame
                    if (prev_y < counter.line_y and curr_y >= counter.line_y) or (prev_y > counter.line_y and curr_y <= counter.line_y):
                        # Log to CSV
                        vehicle_type = model.names[int(cls_idx)]
                        with open(settings.CSV_PATH, mode='a', newline='') as f:
                            csv.writer(f).writerow([vehicle_number, int(track_id), vehicle_type, direction, frame_num, timestamp])

                # Current known direction (might be None if hasn't crossed)
                current_dir = counter.vehicle_directions.get(vehicle_number)

                # Draw vehicle and its movement trail
                vehicle_type_name = model.names[int(cls_idx)]
                frame = annotator.draw_vehicle(frame, bbox, vehicle_number, vehicle_type_name, current_dir, int(track_id), history)

        # Prune inactive tracks after each frame so trails disappear after a timeout
        tracker.prune_inactive(set(track_ids), frame_num)

        # Draw counting line
        frame = annotator.draw_line(frame, settings.COUNTING_LINE_START, settings.COUNTING_LINE_END)
        
        # Draw Dashboard
        total = counter.get_total_count()
        frame = annotator.draw_dashboard(frame, counter.in_count, counter.out_count, total, current_vehicles_on_screen)

        # Write frame
        out.write(frame)

        # Show live window if enabled
        if settings.SHOW_WINDOW:
            cv2.imshow("Traffic Analysis", frame)
            if cv2.waitKey(int(1000 / max(fps, 1))) & 0xFF == ord('q'):
                print("User requested exit.")
                break

        if frame_num % 100 == 0:
            print(f"Processed frame {frame_num}...")

    cap.release()
    out.release()
    if settings.SHOW_WINDOW:
        cv2.destroyAllWindows()
    print("Processing complete!")
    print(f"Output saved to {settings.OUTPUT_PATH}")
    print(f"CSV saved to {settings.CSV_PATH}")

if __name__ == "__main__":
    main()
