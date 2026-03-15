# vision_engine.py
import cv2
import numpy as np

def calculate_health_percentage(frame, hsv_lower, hsv_upper, debug=False):
    """
    Processes the ROI frame to extract the health bar and calculate its percentage.
    Uses lightweight HSV color thresholding instead of heavy ML models.
    """
    # 1. Convert BGR (OpenCV default) to HSV for reliable color detection
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # 2. Create numpy arrays for the color bounds
    lower_bound = np.array(hsv_lower, dtype=np.uint8)
    upper_bound = np.array(hsv_upper, dtype=np.uint8)
    
    # 3. Create a binary mask where pixels in the color range are white (255) and others are black (0)
    mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)
    
    # Optional: Apply slight morphological operations to remove noise
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # 4. Calculate percentage
    # Find contours to get the exact width of the detected health bar
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    health_percent = 0.0
    
    if contours:
        # Assume the largest contour by area is the health bar
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        # Draw a bounding box in debug mode
        if debug:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
        # Calculate percentage based on the bounding box width vs the total ROI width
        # Note: This assumes the health bar scales horizontally from left to right.
        total_width = frame.shape[1] 
        # Calculate percentage (capped at 100%)
        health_percent = min((w / total_width) * 100.0, 100.0)
    
    # Return the calculated percentage, the original frame (potentially annotated), and the mask
    return health_percent, frame, mask
