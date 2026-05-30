# Clean Environment Setup Guide

If your environment becomes corrupted again, follow these steps to create a clean, working environment for the YOLOv8 + BotSort + OpenCV traffic monitoring project on Windows.

## Step 1: Create a Virtual Environment

Open your terminal (PowerShell or Command Prompt) in your project directory (`d:\car`) and run:
```powershell
python -m venv venv
```

## Step 2: Activate the Virtual Environment

**For PowerShell:**
```powershell
venv\Scripts\Activate.ps1
```

**For Command Prompt:**
```cmd
venv\Scripts\activate.bat
```

*(You should see `(venv)` appear at the beginning of your command prompt).*

## Step 3: Upgrade pip

Ensure you have the latest pip installed to avoid wheel building errors:
```powershell
python -m pip install --upgrade pip
```

## Step 4: Install Dependencies

Install the packages in the following exact sequence to prevent DLL collisions and conflicts.

**1. Install PyTorch (Stable CPU Version):**
*(If you do not have an NVIDIA GPU or if your CPU doesn't support AVX2 instructions used in PyTorch 2.3+).*
```powershell
pip install torch==2.2.2 torchvision==0.17.2 torchaudio==2.2.2 --index-url https://download.pytorch.org/whl/cpu
```

**2. Install OpenCV:**
```powershell
pip install opencv-python>=4.8.0
```

**3. Install Ultralytics and Other Dependencies:**
```powershell
pip install ultralytics numpy pandas
```

## Step 5: Verification

Run the verification script to ensure everything loaded correctly:
```powershell
python verify_env.py
```

If it prints `All checks passed successfully.`, you are ready to run:
```powershell
python main.py
```
