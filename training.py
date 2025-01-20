import cv2
import time
import sys
import pyautogui as gui
import keyboard
import mouse
import csv
import PIL.ImageOps
from PIL import Image

sleepytime = 0.041666666666666664
def dataCollection():
    count = 0
    click_detected = False

    def on_click():
        nonlocal click_detected
        click_detected = True
        print("click detected")
    mouse.on_click(on_click)

    while True:
        if keyboard.is_pressed("H"):
            sys.exit()
        count += 1
        time.sleep(sleepytime)
        image = gui.screenshot(region=[150, 200, 1000, 600])
        image_path = f"unmodified_photos\\photo{count}.png"
        image.save(image_path)

        frame = cv2.imread(f'unmodified_photos\\photo{count}.png')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, threshold1=50, threshold2=150)

        # Save processed frame
        processed_frame_name = f'unmodified_photos\\photo{count}.png'
        cv2.imwrite(f'modified_photos\\photo{count}.png', edges)

        with open("dataset.csv", mode="a", newline='\n') as data:
            fieldnames = ['photo', 'label']
            writer = csv.DictWriter(data, fieldnames=fieldnames)

            if click_detected:
                writer.writerow({"photo": processed_frame_name, "label": 1})
                click_detected = False
            else:
                writer.writerow({"photo": processed_frame_name, "label": 0})

while True:
    if keyboard.is_pressed("R"):
        import os, shutil
        folder = r"unmodified_photos"
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.remove(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        dataCollection()