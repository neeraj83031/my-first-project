import cv2
import pyautogui
import numpy as np
import easyocr
import re
import time

print("[INFO] Loading Local AI Models...")
reader = easyocr.Reader(['en'], gpu=False) 
print("[INFO] Models Loaded Successfully.")
AADHAAR_PATTERN = r'\b\d{4}\s\d{4}\s\d{4}\b'
RISK_WORDS = ["password", "secret", "cvv", "otp", "api_key", "pin"]

def scan_screen():
    screenshot = pyautogui.screenshot()
    
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    results = reader.readtext(frame, detail=0)
    text_found = " ".join(results).lower()
    
    risk_detected = False
    alert_message = ""
    
    if re.search(AADHAAR_PATTERN, text_found):
        risk_detected = True
        alert_message = "Indian ID (Aadhaar Card) Pattern"
        
    for word in RISK_WORDS:
        if word in text_found:
            risk_detected = True
            alert_message = f"Sensitive Keyword: '{word.upper()}'"
            break
            
    if risk_detected:
        print(f"\n🚨 [PRIVACY ALERT]: Screen par risk mila - {alert_message}!")
    else:
        print(".", end="", flush=True) 

try:
    print("[RUNNING] Local Screen Privacy Guard Activated. Press Ctrl+C to Stop.")
    while True:
        scan_screen()
        time.sleep(2.0) 
except KeyboardInterrupt:
    print("\n[STOPPED] Software turned off.")
