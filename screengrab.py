# screengrab.py
import mss
import numpy as np
import cv2

class ScreenGrabber:
    """
    Highly optimized screen capture using mss.
    Reuses the mss instance to prevent memory leaks and high overhead.
    """
    def __init__(self, roi):
        self.sct = mss.mss()
        self.roi = roi

    def grab(self):
        """
        Grabs the specific Region of Interest (ROI) from the screen.
        Returns the image as an OpenCV format numpy array (BGR).
        """
        # sct.grab returns an essentially raw BGRA byte array
        sct_img = self.sct.grab(self.roi)
        
        # Convert to numpy array
        img = np.array(sct_img, dtype=np.uint8)
        
        # Drop the alpha channel (BGRA -> BGR) since OpenCV operations 
        # (like HSV conversion) typically expect 3 channels.
        # Ensure the array is contiguous for OpenCV processing.
        return np.ascontiguousarray(img[:, :, :3])
        
    def close(self):
        """Clean up resources."""
        self.sct.close()
