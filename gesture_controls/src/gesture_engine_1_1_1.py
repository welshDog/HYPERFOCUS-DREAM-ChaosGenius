"""
👋 HYPERFOCUS ZONE - GESTURE CONTROL ENGINE
Hand gesture recognition for neurodivergent productivity
Integrates with voice control and Discord community
"""

import cv2
import mediapipe as mp
import numpy as np
import requests
import json
import threading
import time
from datetime import datetime
import logging
from pathlib import Path
import sqlite3
import pyautogui
import subprocess
from collections import deque

# 🎯 Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('GestureControl')

class ChaosGeniusGestureEngine:
    def __init__(self):
        # 🤚 Initialize MediaPipe for hand tracking
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
        # 📹 Initialize camera
        self.cap = None
        self.camera_active = False
        
        # 🌐 Dashboard connection
        self.dashboard_url = "http://localhost:5000"
        
        # 🎯 Gesture recognition system
        self.gesture_buffer = deque(maxlen=10)  # Store last 10 gesture readings
        self.last_gesture_time = datetime.now()
        self.gesture_cooldown = 2.0  # 2 seconds between gesture commands
        
        # 🎮 Gesture command mappings for neurodivergent users
        self.gesture_commands = {
            "thumbs_up": self.gesture_thumbs_up,
            "peace_sign": self.gesture_peace_sign,
            "ok_sign": self.gesture_ok_sign,
            "pointing_up": self.gesture_pointing_up,
            "fist": self.gesture_fist,
            "open_palm": self.gesture_open_palm,
            "pinch": self.gesture_pinch,
            "wave": self.gesture_wave,
        }
        
        # 🔗 Discord webhook integration
        self.discord_webhook_url = None
        
        # 🧠 Gesture state tracking
        self.current_gesture = None
        self.gesture_confidence = 0.0
        self.is_active = False
        
        logger.info("👋 ChaosGenius Gesture Engine initialized!")
    
    def start_camera(self):
        """Initialize camera for gesture recognition"""
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                logger.error("Camera not found or already in use")
                return False
            
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.camera_active = True
            
            logger.info("📹 Camera initialized for gesture control")
            return True
            
        except Exception as e:
            logger.error(f"Camera initialization error: {e}")
            return False
    
    def detect_gesture(self, landmarks):
        """Analyze hand landmarks to detect specific gestures"""
        if not landmarks:
            return None, 0.0
        
        # Extract key landmark positions
        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]
        index_tip = landmarks[8]
        index_pip = landmarks[6]
        middle_tip = landmarks[12]
        middle_pip = landmarks[10]
        ring_tip = landmarks[16]
        ring_pip = landmarks[14]
        pinky_tip = landmarks[20]
        pinky_pip = landmarks[18]
        
        # 👍 Thumbs up detection
        if (thumb_tip.y < thumb_ip.y and  # Thumb pointing up
            index_tip.y > index_pip.y and  # Other fingers down
            middle_tip.y > middle_pip.y and
            ring_tip.y > ring_pip.y and
            pinky_tip.y > pinky_pip.y):
            return "thumbs_up", 0.9
        
        # ✌️ Peace sign detection
        if (index_tip.y < index_pip.y and  # Index and middle up
            middle_tip.y < middle_pip.y and
            ring_tip.y > ring_pip.y and  # Ring and pinky down
            pinky_tip.y > pinky_pip.y and
            thumb_tip.y > thumb_ip.y):  # Thumb down
            return "peace_sign", 0.85
        
        # 👌 OK sign detection
        thumb_index_distance = np.sqrt((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)
        if (thumb_index_distance < 0.05 and  # Thumb and index touching
            middle_tip.y < middle_pip.y and  # Other fingers extended
            ring_tip.y < ring_pip.y and
            pinky_tip.y < pinky_pip.y):
            return "ok_sign", 0.8
        
        # ☝️ Pointing up detection
        if (index_tip.y < index_pip.y and  # Only index finger up
            middle_tip.y > middle_pip.y and
            ring_tip.y > ring_pip.y and
            pinky_tip.y > pinky_pip.y and
            thumb_tip.y > thumb_ip.y):
            return "pointing_up", 0.8
        
        # ✊ Fist detection
        if (thumb_tip.y > thumb_ip.y and  # All fingers closed
            index_tip.y > index_pip.y and
            middle_tip.y > middle_pip.y and
            ring_tip.y > ring_pip.y and
            pinky_tip.y > pinky_pip.y):
            return "fist", 0.85
        
        # 🖐️ Open palm detection
        if (thumb_tip.y < thumb_ip.y and  # All fingers extended
            index_tip.y < index_pip.y and
            middle_tip.y < middle_pip.y and
            ring_tip.y < ring_pip.y and
            pinky_tip.y < pinky_pip.y):
            return "open_palm", 0.9
        
        # 🤏 Pinch detection
        if thumb_index_distance < 0.03:  # Very close thumb and index
            return "pinch", 0.75
        
        return None, 0.0
    
    def process_gesture_command(self, gesture, confidence):
        """Execute command based on detected gesture"""
        # Check cooldown to prevent spam
        time_since_last = (datetime.now() - self.last_gesture_time).total_seconds()
        if time_since_last < self.gesture_cooldown:
            return
        
        # Minimum confidence threshold
        if confidence < 0.7:
            return
        
        # Execute gesture command
        if gesture in self.gesture_commands:
            logger.info(f"👋 Executing gesture: {gesture} (confidence: {confidence:.2f})")
            self.gesture_commands[gesture]()
            self.last_gesture_time = datetime.now()
            
            # Log gesture activity
            self.log_gesture_activity(gesture, confidence)
    
    # 🎯 GESTURE COMMAND IMPLEMENTATIONS
    
    def gesture_thumbs_up(self):
        """Thumbs up = Dopamine boost + positive feedback"""
        try:
            # Send dopamine boost request to dashboard
            payload = {"type": "dopamine_boost", "source": "gesture", "gesture": "thumbs_up"}
            requests.post(f"{self.dashboard_url}/api/dopamine-boost", json=payload, timeout=5)
            
            # Send to Discord community
            if self.discord_webhook_url:
                self.send_discord_notification("👍 Thumbs up detected! Spreading positive vibes! 🌟")
            
            # Visual feedback
            self.show_gesture_feedback("👍 THUMBS UP!", "Dopamine boost activated!", (0, 255, 0))
            
        except Exception as e:
            logger.error(f"Thumbs up gesture error: {e}")
    
    def gesture_peace_sign(self):
        """Peace sign = Take a break / mindfulness mode"""
        try:
            # Trigger break mode
            payload = {"type": "break_mode", "source": "gesture", "gesture": "peace_sign"}
            requests.post(f"{self.dashboard_url}/api/break-mode", json=payload, timeout=5)
            
            # Send to Discord
            if self.discord_webhook_url:
                self.send_discord_notification("✌️ Peace sign detected! Time for a mindful break! 🧘‍♀️")
            
            # Visual feedback
            self.show_gesture_feedback("✌️ PEACE MODE!", "Break time activated!", (0, 191, 255))
            
        except Exception as e:
            logger.error(f"Peace sign gesture error: {e}")
    
    def gesture_ok_sign(self):
        """OK sign = Everything is good / status check"""
        try:
            # Get empire status
            response = requests.get(f"{self.dashboard_url}/api/empire-status", timeout=5)
            if response.status_code == 200:
                data = response.json()
                status = data.get('empire_health', 'Good')
                
                # Visual feedback with status
                self.show_gesture_feedback("👌 STATUS CHECK!", f"Empire health: {status}", (255, 165, 0))
            else:
                self.show_gesture_feedback("👌 ALL GOOD!", "Systems running smoothly!", (0, 255, 0))
            
            # Send to Discord
            if self.discord_webhook_url:
                self.send_discord_notification("👌 OK sign detected! Everything's running smoothly! ✨")
                
        except Exception as e:
            logger.error(f"OK sign gesture error: {e}")
    
    def gesture_pointing_up(self):
        """Pointing up = Ideas/inspiration mode"""
        try:
            # Trigger idea capture mode
            payload = {"type": "idea_mode", "source": "gesture", "gesture": "pointing_up"}
            requests.post(f"{self.dashboard_url}/api/idea-mode", json=payload, timeout=5)
            
            # Visual feedback
            self.show_gesture_feedback("☝️ IDEA MODE!", "Ready to capture inspiration!", (255, 20, 147))
            
            # Send to Discord
            if self.discord_webhook_url:
                self.send_discord_notification("☝️ Pointing up detected! Idea capture mode activated! 💡")
                
        except Exception as e:
            logger.error(f"Pointing up gesture error: {e}")
    
    def gesture_fist(self):
        """Fist = Power mode / hyperfocus activation"""
        try:
            # Activate hyperfocus mode
            payload = {"type": "hyperfocus", "source": "gesture", "gesture": "fist"}
            requests.post(f"{self.dashboard_url}/api/hyperfocus-mode", json=payload, timeout=5)
            
            # Close distracting applications
            distracting_apps = ["chrome.exe", "firefox.exe", "spotify.exe"]
            for app in distracting_apps:
                try:
                    subprocess.run(f"taskkill /f /im {app}", shell=True, capture_output=True)
                except:
                    pass
            
            # Visual feedback
            self.show_gesture_feedback("✊ POWER MODE!", "Hyperfocus activated!", (255, 0, 0))
            
            # Send to Discord
            if self.discord_webhook_url:
                self.send_discord_notification("✊ Fist detected! Hyperfocus mode engaged! 🔥")
                
        except Exception as e:
            logger.error(f"Fist gesture error: {e}")
    
    def gesture_open_palm(self):
        """Open palm = Reset/clear mind"""
        try:
            # Trigger mindfulness reset
            payload = {"type": "mindfulness_reset", "source": "gesture", "gesture": "open_palm"}
            requests.post(f"{self.dashboard_url}/api/mindfulness-reset", json=payload, timeout=5)
            
            # Visual feedback
            self.show_gesture_feedback("🖐️ RESET MODE!", "Mind cleared for fresh start!", (135, 206, 235))
            
            # Send to Discord
            if self.discord_webhook_url:
                self.send_discord_notification("🖐️ Open palm detected! Mind reset activated! 🌸")
                
        except Exception as e:
            logger.error(f"Open palm gesture error: {e}")
    
    def gesture_pinch(self):
        """Pinch = Precision mode / detailed work"""
        try:
            # Activate precision/detail mode
            payload = {"type": "precision_mode", "source": "gesture", "gesture": "pinch"}
            requests.post(f"{self.dashboard_url}/api/precision-mode", json=payload, timeout=5)
            
            # Visual feedback
            self.show_gesture_feedback("🤏 PRECISION MODE!", "Detail work activated!", (128, 0, 128))
            
            # Send to Discord
            if self.discord_webhook_url:
                self.send_discord_notification("🤏 Pinch detected! Precision mode for detailed work! 🎯")
                
        except Exception as e:
            logger.error(f"Pinch gesture error: {e}")
    
    def gesture_wave(self):
        """Wave = Social mode / community interaction"""
        try:
            # Activate social/community mode
            payload = {"type": "social_mode", "source": "gesture", "gesture": "wave"}
            requests.post(f"{self.dashboard_url}/api/social-mode", json=payload, timeout=5)
            
            # Visual feedback
            self.show_gesture_feedback("👋 SOCIAL MODE!", "Community interaction activated!", (255, 192, 203))
            
            # Send to Discord
            if self.discord_webhook_url:
                self.send_discord_notification("👋 Wave detected! Social mode activated! Let's connect! 💫")
                
        except Exception as e:
            logger.error(f"Wave gesture error: {e}")
    
    def show_gesture_feedback(self, title, message, color):
        """Show visual feedback for recognized gesture"""
        # This would display feedback on the video feed
        # Implementation depends on your display preferences
        logger.info(f"Gesture feedback: {title} - {message}")
    
    def run_gesture_recognition(self):
        """Main gesture recognition loop"""
        if not self.start_camera():
            logger.error("Failed to start camera for gesture recognition")
            return
        
        logger.info("👋 Starting gesture recognition...")
        self.is_active = True
        
        try:
            while self.is_active and self.camera_active:
                ret, frame = self.cap.read()
                if not ret:
                    continue
                
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Convert BGR to RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Process hand landmarks
                results = self.hands.process(rgb_frame)
                
                # Draw landmarks and detect gestures
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        # Draw hand landmarks
                        self.mp_drawing.draw_landmarks(
                            frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                        
                        # Detect gesture
                        gesture, confidence = self.detect_gesture(hand_landmarks.landmark)
                        
                        if gesture:
                            self.current_gesture = gesture
                            self.gesture_confidence = confidence
                            
                            # Add to gesture buffer for stability
                            self.gesture_buffer.append(gesture)
                            
                            # Check if gesture is consistent
                            if len(self.gesture_buffer) >= 3:
                                recent_gestures = list(self.gesture_buffer)[-3:]
                                if all(g == gesture for g in recent_gestures):
                                    self.process_gesture_command(gesture, confidence)
                        
                        # Display current gesture on frame
                        if self.current_gesture:
                            cv2.putText(frame, f"Gesture: {self.current_gesture}", 
                                      (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            cv2.putText(frame, f"Confidence: {self.gesture_confidence:.2f}", 
                                      (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # Display frame
                cv2.putText(frame, "ChaosGenius Gesture Control", 
                          (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.imshow('Gesture Control', frame)
                
                # Break on 'q' key press
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        
        except Exception as e:
            logger.error(f"Gesture recognition error: {e}")
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up camera and windows"""
        self.is_active = False
        self.camera_active = False
        
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        
        logger.info("👋 Gesture control stopped and cleaned up")
    
    def log_gesture_activity(self, gesture, confidence):
        """Log gesture activity to database"""
        try:
            conn = sqlite3.connect('chaosgenius.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO activity_log (action, type, details, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (f"Gesture: {gesture}", "gesture_control", 
                  f"Confidence: {confidence:.2f}", datetime.now().isoformat()))
            conn.commit()
            conn.close()
            
            logger.info(f"Gesture activity logged: {gesture} - {confidence:.2f}")
            
        except Exception as e:
            logger.error(f"Gesture logging error: {e}")
    
    def send_discord_notification(self, message):
        """Send notification to Discord webhook"""
        if not self.discord_webhook_url:
            return
        
        try:
            payload = {"content": message}
            requests.post(self.discord_webhook_url, json=payload, timeout=5)
        except Exception as e:
            logger.error(f"Discord notification error: {e}")

def main():
    """Main gesture control execution"""
    try:
        # Initialize gesture engine
        gesture_engine = ChaosGeniusGestureEngine()
        
        print("👋 ChaosGenius Gesture Control Starting!")
        print("Available gestures:")
        print("  👍 Thumbs up - Dopamine boost")
        print("  ✌️ Peace sign - Break time")
        print("  👌 OK sign - Status check")
        print("  ☝️ Pointing up - Idea mode")
        print("  ✊ Fist - Hyperfocus mode")
        print("  🖐️ Open palm - Reset mode")
        print("  🤏 Pinch - Precision mode")
        print("  👋 Wave - Social mode")
        print("\nPress 'q' to quit")
        
        # Start gesture recognition
        gesture_engine.run_gesture_recognition()
        
    except Exception as e:
        print(f"Gesture control error: {e}")
        print("Make sure you have installed: pip install opencv-python mediapipe")

if __name__ == "__main__":
    main()