import cv2
import numpy as np
import imutils
from imutils.video import VideoStream
import requests
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import queue

frame_queue = queue.Queue()

def notify_bat_detected():
    requests.post("http://127.0.0.1:8080/on")

def process_camera(rtsp_url):
    global frame_queue
    vs = VideoStream(rtsp_url).start()
    fgbg = cv2.createBackgroundSubtractorMOG2()

    while True:
        frame = vs.read()

        if frame is None:
            print(f"Error: Unable to load video stream from {rtsp_url}")
            break

        frame = imutils.resize(frame, width=600)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        fgmask = fgbg.apply(gray_frame)

        contours = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)

        for c in contours:
            if cv2.contourArea(c) < 1000:
                continue

            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            notify_bat_detected()

        frame_queue.put(frame)

    vs.stop()

def display_frames():
    global frame_queue
    while True:
        if not frame_queue.empty():
            frame = frame_queue.get()
            plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            plt.pause(0.01)
            plt.clf()

# Replace with your cameras' RTSP stream URLs
rtsp_url_camera1 = "rtsps://192.168.100.22:1341/xxxxx"
rtsp_url_camera2 = "rtsps://192.168.100.22:1341/xxxxxx"

# Start processing both cameras in separate threads
thread1 = threading.Thread(target=process_camera, args=(rtsp_url_camera1,))
thread2 = threading.Thread(target=process_camera, args=(rtsp_url_camera2,))

thread1.start()
thread2.start()

# Start display thread
display_thread = threading.Thread(target=display_frames)
display_thread.start()

thread1.join()
thread2.join()
display_thread.join()

plt.close()
