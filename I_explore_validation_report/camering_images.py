import pyautogui
import time
import os
from datetime import datetime

# Directory to save screenshots
save_dir = r"."  # Use raw string

# Create the directory if it doesn't exist
os.makedirs(save_dir, exist_ok=True)

def take_screenshot():
    # Generate a timestamp for unique filenames
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(save_dir, f"picture_{timestamp}.png")
    # Take screenshot and save
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)
    print(f"Saved screenshot: {filename}")

if __name__ == "__main__":
    print("Press Ctrl+C to stop the script.")
    try:
        while True:
            take_screenshot()
            time.sleep(300)  # Wait for 300 seconds
    except KeyboardInterrupt:
        print("Program stopped.")
