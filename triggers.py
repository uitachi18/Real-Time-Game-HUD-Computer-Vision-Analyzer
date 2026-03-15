# triggers.py
import time
import winsound
import pandas as pd
import os
from datetime import datetime

class AlertSystem:
    def __init__(self, threshold, cooldown):
        self.threshold = threshold
        self.cooldown = cooldown
        self.last_alert_time = 0.0
        self.log_file = "health_events.csv"
        
        # Initialize CSV log if it doesn't exist
        if not os.path.exists(self.log_file):
            df = pd.DataFrame(columns=["timestamp", "health_percent", "event_type"])
            df.to_csv(self.log_file, index=False)

    def check_and_trigger(self, current_health):
        """
        Checks if health is below threshold and triggers if cooldown has passed.
        """
        current_time = time.time()
        
        # If health is 0, we might be dead or the bar isn't on screen (e.g. paused/loading).
        # We trigger > 0 and <= threshold.
        # This prevents spamming when navigating menus where the health bar disappears.
        if 0 < current_health <= self.threshold:
            if (current_time - self.last_alert_time) >= self.cooldown:
                self._trigger_alert(current_health)
                self.last_alert_time = current_time
                return True
        return False

    def _trigger_alert(self, current_health):
        """Executes the audio alert and logs the event."""
        print(f"[ALERT] Health critical! ({current_health:.1f}%)")
        
        # Play a system beep (Frequency in Hz, Duration in ms)
        # Using a distinct, urgent double-beep pattern without blocking too long
        try:
            winsound.Beep(1000, 200)
            winsound.Beep(1200, 200)
        except Exception as e:
            print(f"Audio failed: {e}")
            
        # Log to CSV using pandas
        new_event = pd.DataFrame([{
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "health_percent": round(current_health, 2),
            "event_type": "LOW_HEALTH_WARNING"
        }])
        
        # Append to CSV
        new_event.to_csv(self.log_file, mode='a', header=False, index=False)
