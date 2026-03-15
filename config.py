# config.py
"""
Centralized settings for the HUD Analyzer.
Adjust these values based on your specific monitor resolution and the game's UI.
"""

# ---------------------------------------------------------
# 1. SCREEN CAPTURE SETTINGS (Region of Interest)
# ---------------------------------------------------------
# Define the bounding box for the health bar.
# This prevents capturing the entire 1080p/4K screen, saving massive CPU/VRAM.
# Example for a 1920x1080 monitor where health is in the top left:
ROI = {
    "top": 50,       # Y coordinate from top of screen
    "left": 50,      # X coordinate from left of screen
    "width": 300,    # Width of the health bar area
    "height": 40     # Height of the health bar area
}

# ---------------------------------------------------------
# 2. COMPUTER VISION SETTINGS (HSV Color Ranges)
# ---------------------------------------------------------
# The HSV (Hue, Saturation, Value) range for the health bar color (e.g., Red for health)
# You will need to calibrate this using the debug mode.
# In OpenCV, Hue is 0-179, Saturation is 0-255, Value is 0-255.
HSV_LOWER = [0, 150, 100]    # Lower bound (e.g., dark red)
HSV_UPPER = [10, 255, 255]   # Upper bound (e.g., bright red)

# Note: Red wraps around in HSV. If your health bar is pure red, you might need
# two ranges (0-10 and 170-179), but for simplicity, we start with 0-10.

# ---------------------------------------------------------
# 3. ALERT & TRIGGER SETTINGS
# ---------------------------------------------------------
HEALTH_THRESHOLD_PERCENT = 20.0  # Trigger alert when health is below this %
COOLDOWN_SECONDS = 5.0           # Minimum seconds between back-to-back alerts to avoid spam

# ---------------------------------------------------------
# 4. DEBUG SETTINGS
# ---------------------------------------------------------
# Set to True to open an OpenCV window showing the capture and mask.
# CRITICAL: Set to False when actually playing the game to save resources!
DEBUG_MODE = True
TARGET_FPS = 10                  # How many times per second to check health (lower = less CPU)
