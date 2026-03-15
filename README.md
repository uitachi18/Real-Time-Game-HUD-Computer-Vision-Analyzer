# Real-Time Game HUD Computer Vision Analyzer

A highly optimized, high-FPS Python tool designed to monitor a game's HUD (like a health bar) in real-time and trigger alerts, using extremely low CPU and VRAM. Perfect for running alongside heavy games (e.g., The Witcher 3, Cyberpunk 2077) on mid-range hardware. 

## 🚀 Features

* **Zero VRAM Usage:** Relies on rapid `mss` screen-grabbing and lightweight OpenCV masking rather than heavy machine learning models like YOLO, keeping your GPU memory free for the game.
* **Low CPU Footprint:** Calculates processing delay and explicitly sleeps the thread to maintain a custom target FPS (e.g., 10 FPS), resulting in 1-2% CPU usage.
* **Micro-ROI Processing:** Grabs only the exact coordinates of the health bar (e.g., a 300x40 pixel block) rather than the entire 1080p/4K screen.
* **Real-time Calibration GUI:** Includes an interactive debug window with Trackbars to perfectly isolate the HUD element before you start playing.
* **Event Logging & Audio Alerts:** Plays a distinct sound and logs a timestamp to a CSV file when health drops below a user-defined threshold, with a built-in cooldown to prevent spam.

## 🛠️ Prerequisites & Installation

1. **Python 3.8+**
2. Clone or download the repository.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration & Calibration

Before depending on the tool in-game, you must adapt it to your specific monitor resolution and the physical color of the health bar.

1. Open `config.py` and set `DEBUG_MODE = True`.
2. Run the analyzer:
   ```bash
   python main.py
   ```
3. A debug window with 6 sliders will appear. Slide the **HSV (Hue, Saturation, Value)** ranges until your game's health bar shows up as a solid **white block** on a completely black background.
4. Note those 6 values and update `HSV_LOWER` and `HSV_UPPER` in `config.py`.
5. Adjust the `ROI` (Region of Interest) coordinates in `config.py` so the capture window tightly fits the HUD element you are tracking.
6. Once calibrated, set `DEBUG_MODE = False` to unleash maximum performance, and run the script while you game!

## 📂 Project Structure

* `main.py`: The core orchestration loop managing capture, analysis, and triggers.
* `config.py`: Centralized user settings (ROI, HSV bounds, FPS, thresholds).
* `screengrab.py`: Optimized `mss` capture logic.
* `vision_engine.py`: OpenCV operations that calculate the exact percentage of the visible health bar.
* `triggers.py`: Handles audio cues (`winsound`) and event logging (`pandas`).

## 🔑 License
MIT License
