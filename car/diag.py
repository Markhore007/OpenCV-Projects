import sys
import importlib.metadata as md
import os
import subprocess

def check_package(name):
    try:
        ver = md.version(name)
        print(f"[PASS] {name} is installed (version: {ver})")
        return True
    except md.PackageNotFoundError:
        print(f"[FAIL] {name} is NOT installed")
        return False

print("=== Environment Diagnosis ===")
print(f"Python Version: {sys.version}")

packages_to_check = ['torch', 'torchvision', 'torchaudio', 'ultralytics', 'opencv-python', 'numpy']
for pkg in packages_to_check:
    check_package(pkg)

# Check OpenCV import
try:
    import cv2
    print(f"[PASS] cv2 imported successfully (version: {cv2.__version__})")
except ImportError as e:
    print(f"[FAIL] cv2 import failed: {e}")

# Check Torch import and CUDA
try:
    import torch
    print(f"[PASS] torch imported successfully")
    print(f"CUDA Available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"CUDA Version: {torch.version.cuda}")
except Exception as e:
    print(f"[FAIL] torch import failed: {e}")

