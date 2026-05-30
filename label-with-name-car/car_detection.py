import cv2
from ultralytics import YOLO
model = YOLO("yolov8n.pt")   
video_path = "video.mp4"
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Error: Video open nahi ho rahi.")
    exit()
print("Car Detection Start... Press 'q' to exit")
while True:
    ret, frame = cap.read()
    if not ret:
        print("Video End")
        break
    results = model(frame, conf=0.25)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls_id = int(box.cls[0])
            if model.names[cls_id] == "car":
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                cv2.putText(frame,
                            "Car",
                            (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)
    cv2.imshow("YOLOv8 Car Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()