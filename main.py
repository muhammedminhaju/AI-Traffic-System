import sys
from datetime import datetime
import cv2
import numpy as np
import torch
import time
import os
import serial
from ultralytics import YOLO


# ARDUINO NANO SERIAL CONNECTION


try:
    nano = serial.Serial("COM3", 9600, timeout=1)  # Change COM if needed
    time.sleep(2)
    print("Connected to Arduino Nano")
except:
    nano = None
    print("Arduino not connected")


# PATH HANDLER

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# EXPIRY DATE CHECK

EXPIRY_DATE = datetime(2026, 12, 31)
if datetime.now() > EXPIRY_DATE:
    print("❌")
    sys.exit(0)

# FRAME SKIP (FPS BOOST)

frame_skip = 5
frame_counter = 0


# LOAD YOLO MODELS

model = YOLO(resource_path("models/yolov8n.pt"))
modelam = YOLO(resource_path("models/best.pt"))

# device = "cuda" if torch.cuda.is_available() else "cpu"
device = "cuda" 
model.to(device)
modelam.to(device)
print("Using device:", device)


# VIDEO INPUTS (3 ROADS)

caps = [
    cv2.VideoCapture(resource_path("videos/part1.mp4")),
    cv2.VideoCapture(resource_path("videos/part2.mp4")),
    cv2.VideoCapture(resource_path("videos/part3.mp4"))
]

vehicle_classes = [2, 3, 5, 7]
ambulance_classes = [0]  # class 0 is ambulance in best.pt

# FRAME SETTINGS
W, H = 640, 640
blank_frame = np.zeros((H, W, 3), dtype=np.uint8)

WINDOW_NAME = "Smart Traffic Signal"
WINDOW_W, WINDOW_H = 960, 960


cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
cv2.resizeWindow(WINDOW_NAME, WINDOW_W, WINDOW_H)

# VIDEO SAVING SETUP

record_folder = resource_path("recordings")
os.makedirs(record_folder, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_path = os.path.join(record_folder, f"traffic_output_{timestamp}.mp4")

fourcc = cv2.VideoWriter_fourcc(*'mp4v')

fps = 10

out = cv2.VideoWriter(output_path, fourcc, fps, (WINDOW_W, WINDOW_H))

print(" Recording started:", output_path)

stop_clicked = False
BTN_WIDTH = 180
BTN_HEIGHT = 60

btn_x2 = WINDOW_W - 10
btn_y2 = WINDOW_H - 10
btn_x1 = btn_x2 - BTN_WIDTH
btn_y1 = btn_y2 - BTN_HEIGHT

def mouse_callback(event, x, y, flags, param):
    global stop_clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        if btn_x1 <= x <= btn_x2 and btn_y1 <= y <= btn_y2:
            stop_clicked = True

cv2.setMouseCallback(WINDOW_NAME, mouse_callback)


# SIGNAL PARAMETERS

YELLOW_DURATION = 5
LOW_DENSITY_THRESHOLD = 2
LOW_DENSITY_GREEN = 15
IDLE_TIME_LIMIT = 90

signal_index = 0
signal_state = "GREEN"
signal_start_time = time.time()
signal_duration = 20

ambulance_override = False
pending_ambulance = False
pending_ambulance_index = -1
idle_start_times = [None, None, None]


# SIGNAL ENCODER

def encode_signal(signal_index, signal_state):
    code = ['R', 'R', 'R']
    if signal_state == "GREEN":
        code[signal_index] = 'G'
    elif signal_state == "YELLOW":
        code[signal_index] = 'Y'
    return "".join(map(str, code))


# DETECTION CONTROL

detect_every = 10
frame_counter = 0
vehicle_counts = [0, 0, 0]
ambulance_roads = [False, False, False]




while True:
    frame_counter += 1
    
    frames = []

    for cap in caps:
        ret, frame = cap.read()
        if not ret:
            frame = blank_frame.copy()
        else:
            frame = cv2.resize(frame, (W, H))
        frames.append(frame)
        
    if frame_counter % detect_every == 0:
        new_vehicle_counts = []
        new_ambulance_roads = []
      
        for frame in frames:
          
            results = model(frame, conf=0.2, verbose=False,half=True)
          
            count = sum(1 for r in results for box in r.boxes if int(box.cls[0]) in vehicle_classes)
            am_results = modelam(frame, conf=0.9, verbose=False,half=True)
            
            ambulance_found = any(
    int(box.cls[0]) in ambulance_classes
    for r in am_results
    for box in r.boxes
)
            new_vehicle_counts.append(count)
            new_ambulance_roads.append(ambulance_found)
    
        vehicle_counts = new_vehicle_counts
        ambulance_roads = new_ambulance_roads
    current_time = time.time()

    # Idle tracking
    for i, count in enumerate(vehicle_counts):
        if count <= LOW_DENSITY_THRESHOLD:
            if idle_start_times[i] is None:
                idle_start_times[i] = current_time
        else:
            idle_start_times[i] = None

    # Ambulance logic
    if any(ambulance_roads) and not ambulance_override and not pending_ambulance:
        pending_ambulance = True
        pending_ambulance_index = ambulance_roads.index(True)

    if pending_ambulance:
        if signal_state != "YELLOW":
            signal_state = "YELLOW"
            signal_start_time = current_time
        elif current_time - signal_start_time > YELLOW_DURATION:
            signal_index = pending_ambulance_index
            signal_state = "GREEN"
            signal_duration = 40
            signal_start_time = current_time
            ambulance_override = True
            pending_ambulance = False

    elif ambulance_override:
        if current_time - signal_start_time > signal_duration:
            ambulance_override = False
            signal_state = "YELLOW"
            signal_start_time = current_time

    else:
        if signal_state == "GREEN" and current_time - signal_start_time > signal_duration:
            signal_state = "YELLOW"
            signal_start_time = current_time

        elif signal_state == "YELLOW" and current_time - signal_start_time > YELLOW_DURATION:
            idle_candidates = [
                i for i, t in enumerate(idle_start_times)
                if t and (current_time - t > IDLE_TIME_LIMIT)
            ]

            if idle_candidates:
                signal_index = idle_candidates[0]
                signal_duration = LOW_DENSITY_GREEN
            elif len(set(vehicle_counts)) == 1:
                signal_index = (signal_index + 1) % 3
                signal_duration = 20
            else:
                signal_index = vehicle_counts.index(max(vehicle_counts))
                signal_duration = 20

            signal_state = "GREEN"
            signal_start_time = current_time

    # Timer
    if signal_state == "GREEN":
        remaining = signal_duration - (current_time - signal_start_time)
    else:
        remaining = YELLOW_DURATION - (current_time - signal_start_time)

    remaining = max(0, int(remaining))

    # Send to Arduino
    signal_code = encode_signal(signal_index, signal_state)
    if nano:
        nano.write((signal_code + "\n").encode())
    print("Sent:", signal_code)

    # Display
    processed = []
    for i, frame in enumerate(frames):
        if i == signal_index:
            color = (0, 255, 0) if signal_state == "GREEN" else (0, 255, 255)
            signal = signal_state
        else:
            color = (0, 0, 255)
            signal = "RED"

        cv2.putText(frame, f"Road {i+1}", (20, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        cv2.putText(frame, f"Vehicles: {vehicle_counts[i]}", (20, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        cv2.putText(frame, f"Signal: {signal}", (20, 105),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        cv2.putText(frame, f"Time Left: {remaining}s", (20, 140),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        if ambulance_roads[i]:
            cv2.putText(frame, "AMBULANCE!", (20, 175),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
       
        processed.append(frame)

    top = np.hstack((processed[0], processed[1]))
    bottom = np.hstack((processed[2], blank_frame))
    combined = np.vstack((top, bottom))

   
    combined_resized = cv2.resize(combined, (WINDOW_W, WINDOW_H))

    cv2.imshow(WINDOW_NAME, combined_resized)
    out.write(combined_resized)

    if stop_clicked:
        break

    if cv2.waitKey(1) & 0xFF == ord("q"):
         if nano:
            nano.write(('stop' + "\n").encode())
         print("Sent:", 'stop')
         break

# Cleanup
for cap in caps:
    cap.release()

out.release()
cv2.destroyAllWindows()

if nano:
    nano.close()


print(" Program finished.")
print(" Saved video at:", output_path)
