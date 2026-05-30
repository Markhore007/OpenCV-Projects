import cv2
import supervision as sv
from ultralytics import YOLO
import sys

def main():
    # Load YOLOv8 model
    model = YOLO("yolov8s.pt")  # or yolov8n.pt for faster speed

    VIDEO_PATH = "video.mp4"

    # Get video size so line is always visible
    try:
        video_info = sv.VideoInfo.from_video_path(video_path=VIDEO_PATH)
        H, W = video_info.height, video_info.width
    except Exception as e:
        print(f"Error: Could not get video info from {VIDEO_PATH}: {e}")
        sys.exit()

    # Place line in the middle of the frame
    line_zone = sv.LineZone(
        start=sv.Point(0, H // 2),
        end=sv.Point(W, H // 2)
    )
    line_annotator = sv.LineZoneAnnotator()

    # Tracking & counting loop
    for result in model.track(source=VIDEO_PATH, stream=True, classes=[2], imgsz=640):
        frame = result.orig_img
        detections = sv.Detections.from_ultralytics(result)

        # Count when objects cross the line
        line_zone.trigger(detections)
        line_annotator.annotate(frame, line_zone)

        cv2.putText(frame, f"Cars (In): {line_zone.in_count}", (30, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Cars (Out): {line_zone.out_count}", (30, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Tracking & Counting", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # 27 is the ESC key
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()