# main.py
import time
import cv2
import sys

# Import configurations and custom modules
import config
from screengrab import ScreenGrabber
from vision_engine import calculate_health_percentage
from triggers import AlertSystem

def main():
    print("--- Starting Game HUD Analyzer ---")
    print("Hardware Profile: Low VRAM/CPU Mode Enabled.")
    print(f"Target FPS: {config.TARGET_FPS}")
    print(f"Debug Mode: {'ON' if config.DEBUG_MODE else 'OFF'}")
    
    # Initialize components
    grabber = ScreenGrabber(config.ROI)
    alerter = AlertSystem(config.HEALTH_THRESHOLD_PERCENT, config.COOLDOWN_SECONDS)
    
    # Calculate loop delay to maintain target FPS without maxing CPU
    frame_delay = 1.0 / config.TARGET_FPS if config.TARGET_FPS > 0 else 0
    
    # -------------------------------------------------------------
    # INTERACTIVE CALIBRATION UI
    # -------------------------------------------------------------
    if config.DEBUG_MODE:
        cv2.namedWindow("HUD Analyzer - Mask")
        def nothing(x): pass
        cv2.createTrackbar("H Min", "HUD Analyzer - Mask", config.HSV_LOWER[0], 179, nothing)
        cv2.createTrackbar("S Min", "HUD Analyzer - Mask", config.HSV_LOWER[1], 255, nothing)
        cv2.createTrackbar("V Min", "HUD Analyzer - Mask", config.HSV_LOWER[2], 255, nothing)
        cv2.createTrackbar("H Max", "HUD Analyzer - Mask", config.HSV_UPPER[0], 179, nothing)
        cv2.createTrackbar("S Max", "HUD Analyzer - Mask", config.HSV_UPPER[1], 255, nothing)
        cv2.createTrackbar("V Max", "HUD Analyzer - Mask", config.HSV_UPPER[2], 255, nothing)
        print("\n[INFO] Interactive HSV Trackbars enabled in the 'HUD Analyzer - Mask' window!")
        print("[INFO] Try sliding these values until your health bar is purely white in the mask.\n")
    
    try:
        while True:
            start_time = time.perf_counter()
            
            # 1. Capture the ROI
            frame = grabber.grab()
            
            # Read HSV values from trackbars in debug mode
            if config.DEBUG_MODE:
                # Essential for Windows OS GUI thread to process window events
                cv2.waitKey(1)
                
                try:
                    hsv_lower = [
                        cv2.getTrackbarPos("H Min", "HUD Analyzer - Mask"),
                        cv2.getTrackbarPos("S Min", "HUD Analyzer - Mask"),
                        cv2.getTrackbarPos("V Min", "HUD Analyzer - Mask")
                    ]
                    hsv_upper = [
                        cv2.getTrackbarPos("H Max", "HUD Analyzer - Mask"),
                        cv2.getTrackbarPos("S Max", "HUD Analyzer - Mask"),
                        cv2.getTrackbarPos("V Max", "HUD Analyzer - Mask")
                    ]
                except cv2.error:
                    hsv_lower, hsv_upper = config.HSV_LOWER, config.HSV_UPPER
            else:
                hsv_lower, hsv_upper = config.HSV_LOWER, config.HSV_UPPER

            # 2. Process Vision (Calculate Health)
            health_pct, annotated_frame, mask = calculate_health_percentage(
                frame, 
                hsv_lower, 
                hsv_upper, 
                debug=config.DEBUG_MODE
            )
            
            # 3. Check Triggers
            alerter.check_and_trigger(health_pct)
            
            # 4. Display Debug Window (if enabled)
            if config.DEBUG_MODE:
                # Add text overlay to the annotated frame
                cv2.putText(annotated_frame, f"Health: {health_pct:.1f}%", (10, 25), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                # Show standard frame and binary mask
                cv2.imshow("HUD Analyzer - Capture", annotated_frame)
                cv2.imshow("HUD Analyzer - Mask", mask)
                
                # cv2.waitKey is required to update imshow windows. 
                # 1ms delay is enough. If 'q' is pressed, exit.
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("Exiting...")
                    break
            
            # 5. Sleep to maintain low CPU usage
            elapsed = time.perf_counter() - start_time
            sleep_time = frame_delay - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Shutting down...")
    except Exception as e:
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup resources
        grabber.close()
        cv2.destroyAllWindows()
        print("HUD Analyzer closed cleanly.")

if __name__ == "__main__":
    main()
