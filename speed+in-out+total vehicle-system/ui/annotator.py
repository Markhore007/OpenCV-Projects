import cv2
import numpy as np

class Annotator:
    def __init__(self):
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 0.6
        self.thickness = 2
        
        self.color_bbox = (255, 144, 30) # Professional blue-ish/orange depending on BGR
        self.color_text = (255, 255, 255)
        self.color_bg = (40, 40, 40)
        self.color_line = (0, 0, 255) # Red counting line

    def draw_dashboard(self, frame, in_count, out_count, total_count, current_count):
        h, w = frame.shape[:2]
        
        # Draw translucent background
        overlay = frame.copy()
        cv2.rectangle(overlay, (20, 20), (400, 220), self.color_bg, -1)
        frame = cv2.addWeighted(overlay, 0.7, frame, 0.3, 0)

        # Draw text
        cv2.putText(frame, "================================", (30, 50), self.font, self.font_scale, self.color_text, self.thickness)
        cv2.putText(frame, "TRAFFIC ANALYTICS", (30, 80), self.font, self.font_scale, (0, 255, 255), self.thickness)
        cv2.putText(frame, f"IN VEHICLES: {in_count}", (30, 110), self.font, self.font_scale, self.color_text, self.thickness)
        cv2.putText(frame, f"OUT VEHICLES: {out_count}", (30, 140), self.font, self.font_scale, self.color_text, self.thickness)
        cv2.putText(frame, f"TOTAL VEHICLES: {total_count}", (30, 170), self.font, self.font_scale, self.color_text, self.thickness)
        cv2.putText(frame, f"CURRENT ON SCREEN: {current_count}", (30, 200), self.font, self.font_scale, self.color_text, self.thickness)

        return frame

    def draw_line(self, frame, start_pt, end_pt):
        cv2.line(frame, start_pt, end_pt, self.color_line, 2)
        cv2.putText(frame, "COUNTING LINE", (start_pt[0] + 10, start_pt[1] - 10), self.font, self.font_scale, self.color_line, self.thickness)
        return frame

    def draw_vehicle(self, frame, bbox, vehicle_number, vehicle_type, direction, tracker_id):
        x1, y1, x2, y2 = map(int, bbox)
        
        # Bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), self.color_bbox, 2)
        
        # Label text
        dir_text = direction if direction else "WAITING"
        label = f"Vehicle #{vehicle_number} | {vehicle_type} | {dir_text}"
        
        # Text background
        (tw, th), _ = cv2.getTextSize(label, self.font, self.font_scale, self.thickness)
        cv2.rectangle(frame, (x1, y1 - th - 10), (x1 + tw + 10, y1), self.color_bbox, -1)
        
        # Text
        cv2.putText(frame, label, (x1 + 5, y1 - 5), self.font, self.font_scale, self.color_text, self.thickness)

        return frame
