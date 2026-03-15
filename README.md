# Real-Time Game HUD Computer Vision Analyzer

A highly optimized, high-FPS Python tool designed to monitor a game's HUD (like a health bar) in real-time and trigger alerts, using extremely low CPU and VRAM. Perfect for running alongside heavy games (e.g., The Witcher 3, Cyberpunk 2077) on mid-range hardware.

## ❓ Why This Was Created

Modern game state monitoring often requires heavy machine learning models (like YOLO) or slow screen-grabbing methods (like PIL/PyAutoGUI). On mid-range hardware (e.g., RTX 4050, 16GB RAM), running these alongside a demanding game like *The Witcher 3* often results in:
*   **Significant VRAM overhead** causing game crashes.
*   **CPU spikes** causing micro-stutters and input lag.
*   **Inaccurate detection** due to in-game lighting changes.

This project was built to provide a **surgical, low-overhead alternative**. By using pure computer vision and optimized system hooks, it achieves its goal with near-zero impact on gaming performance.

## ⚙️ How It Works

The analyzer operates through a four-stage pipeline:

1.  **Optimized Capture (`mss`):** Instead of capturing the whole screen, we pull a tiny **Region of Interest (ROI)** directly from the Windows Desktop Duplication API. This is significantly faster and uses less bandwidth than traditional methods.
2.  **HSV Color Isolation:** The captured frame is converted from BGR to **HSV (Hue, Saturation, Value)**. HSV is superior for game-state detection because it isolates color (Hue) from lighting/shadows (Value), preventing false negatives when your character enters a dark cave or bright field.
3.  **Binary Masking & Contours:** We apply a threshold to the HSV image, turning everything into black-and-white. OpenCV then identifies the "Contour" (the solid shape) of the health bar.
4.  **Geometric Percentage Calculation:** The tool measures the pixel width of the detected health bar relative to the total width of the ROI. This allows it to compute a precise percentage (e.g., 24.5% health remaining) without needing a complex trained model.

## 🚀 Features

*   **Zero VRAM Usage:** Pure CPU-bound OpenCV operations keep your GPU dedicated to rendering.
*   **Low CPU Footprint:** Explicit thread-sleeping maintains a stable 10 FPS (customizable), resulting in ~1% CPU usage.
*   **Interactive Calibration:** Real-time sliders allow you to "dial in" the perfect color range while the game is running.
*   **Debounced Alerts:** CSV logging and audio alerts with a configurable cooldown to prevent sound spam.

## 🛠️ Prerequisites & Installation

1.  **Python 3.8+**
2.  Clone or download the repository.
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Configuration & Calibration

Before depending on the tool in-game, you must adapt it to your specific monitor resolution and the physical color of the health bar.

1.  Open `config.py` and set `DEBUG_MODE = True`.
2.  Run the analyzer:
    ```bash
    python main.py
    ```
3.  A debug window with 6 sliders will appear. Slide the **HSV (Hue, Saturation, Value)** ranges until your game's health bar shows up as a solid **white block** on a completely black background.
4.  Note those 6 values and update `HSV_LOWER` and `HSV_UPPER` in `config.py`.
5.  Adjust the `ROI` (Region of Interest) coordinates in `config.py` so the capture window tightly fits the HUD element you are tracking.
6.  Once calibrated, set `DEBUG_MODE = False` to unleash maximum performance, and run the script while you game!

## 📂 Project Structure

*   `main.py`: The core orchestration loop managing capture, analysis, and triggers.
*   `config.py`: Centralized user settings (ROI, HSV bounds, FPS, thresholds).
*   `screengrab.py`: Optimized `mss` capture logic.
*   `vision_engine.py`: OpenCV operations that calculate the exact percentage of the visible health bar.
*   `triggers.py`: Handles audio cues (`winsound`) and event logging (`pandas`).

## 🔑 License
MIT License
