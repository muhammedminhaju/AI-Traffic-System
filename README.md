# 🚦 Smart Traffic Signal System using AI & Arduino

##  Overview

This project implements an **AI-powered smart traffic signal system** that dynamically controls traffic lights based on real-time vehicle density and emergency vehicle detection.

It integrates:

*  Computer Vision (YOLOv8)
*  Ambulance Detection (custom-trained model)
*  Arduino Nano for hardware signal control
*  Multi-road video input processing

---

##  Features

*  **Vehicle Density Detection** using YOLOv8
*  **Ambulance Priority Override System**
*  **Dynamic Signal Switching Algorithm**
*  **Adaptive Timing based on traffic load**
*  **Real-time visualization dashboard**
*  **Serial communication with Arduino Nano**

---

##  How It Works

1. **Video Input**

   * 3 road video feeds are processed simultaneously

2. **Object Detection**

   * YOLOv8 detects vehicles
   * Custom model detects ambulances

3. **Decision Engine**

   * Chooses signal based on:

     * Maximum vehicle count
     * Idle roads
     * Ambulance priority

4. **Signal Encoding**

   * Signals encoded as:

     * `GRR` → Road 1 Green
     * `RGR` → Road 2 Green
     * `RRG` → Road 3 Green

5. **Arduino Control**

   * Signal sent via Serial (USB)
   * Arduino activates LEDs/relays accordingly

---

## Tech Stack

| Category        | Technology                    |
| --------------- | ----------------------------- |
| Programming     | Python, C++                   |
| AI/ML           | YOLOv8 (Ultralytics), PyTorch |
| Computer Vision | OpenCV                        |
| Hardware        | Arduino Nano                  |
| Communication   | Serial (pyserial)             |

---

##  Project Structure

```
smart-traffic-signal-ai/
│
├── arduino/
│   └── traffic_signal.ino
│
├── models/
│   ├── best.pt
│   └── yolov8n.pt
├── videos 
│
├── recordings/
├── requirements.txt
├── main.py
└── README.md
```

---

##  Installation & Setup

### 1️⃣ Clone the Repository

```
git clone https://github.com/muhammedminhaju/AI-Traffic-System
cd smart-traffic-signal-ai
```

---

### 2️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

### 3️⃣ Setup Arduino

* Upload `traffic_signal.ino` to Arduino Nano
* Connect Arduino via USB


### 4️⃣ Run the Project

```
python main.py
```

---

##  Signal Encoding Logic

| Code | Meaning      |
| ---- | ------------ |
| GRR  | Road 1 Green |
| RGR  | Road 2 Green |
| RRG  | Road 3 Green |
| YYY  | All Yellow   |
| RRR  | All Red      |
| stop | System Stop  |

---

## Author

**Muhammed Minhaju A.**

---

## 📄 License

MIT License

Copyright (c) 2026 Muhammed Minhaju A.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

