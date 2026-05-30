import sys

def verify_env():
    print("=== Environment Verification ===")
    
    # 1. OpenCV
    try:
        import cv2
        print("OpenCV OK")
    except ImportError as e:
        print(f"OpenCV FAILED: {e}")
        sys.exit(1)
        
    # 2. PyTorch
    try:
        import torch
        print("Torch OK")
    except ImportError as e:
        print(f"Torch FAILED: {e}")
        sys.exit(1)
        
    # 3. Ultralytics
    try:
        from ultralytics import YOLO
        print("Ultralytics OK")
    except ImportError as e:
        print(f"Ultralytics FAILED: {e}")
        sys.exit(1)
        
    print("All checks passed successfully.")

if __name__ == "__main__":
    verify_env()
