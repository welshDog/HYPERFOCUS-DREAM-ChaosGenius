"""
🎤 HYPERFOCUS ZONE - VOICE CONTROL ENGINE
Ultra-responsive voice commands for neurodivergent productivity
Integrates with Discord bot and ChaosGenius dashboard
"""

import speech_recognition as sr
import pyttsx3
import requests
import json
import threading
import time
from datetime import datetime
import logging
import sqlite3
from pathlib import Path
import asyncio
import websockets
import pyautogui
import subprocess
import os

# 🎯 Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('VoiceControl')

class ChaosGeniusVoiceEngine:
    def __init__(self):
        # 🎤 Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # 🔊 Initialize text-to-speech
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 180)  # Slightly faster for ADHD brains
        self.tts_engine.setProperty('volume', 0.8)
        
        # 🌐 Dashboard connection
        self.dashboard_url = "http://localhost:5000"
        
        # 🎯 Command patterns for neurodivergent users
        self.commands = {
            # 🧠 Focus & Energy Commands
            "hyperfocus mode": self.activate_hyperfocus,
            "focus timer": self.start_focus_timer,
            "energy check": self.check_energy_status,
            "dopamine boost": self.trigger_dopamine_boost,
            "break time": self.initiate_break_mode,
            
            # 🚀 Productivity Commands  
            "create product": self.voice_create_product,
            "brain dump": self.capture_brain_dump,
            "idea capture": self.quick_idea_capture,
            "launch ai squad": self.launch_ai_squad,
            "status report": self.empire_status_report,
            
            # 🎛️ System Controls
            "open dashboard": self.open_dashboard,
            "discord mode": self.activate_discord_mode,
            "ultra mode": self.activate_ultra_mode,
            "system optimization": self.run_system_optimization,
            
            # 🧘 Wellness Commands
            "breathing exercise": self.guided_breathing,
            "motivation boost": self.neurodivergent_motivation,
            "chaos organizing": self.organize_chaos_mode,
            "reflection time": self.reflection_prompt,
        }
        
        # 🎮 Initialize voice control state
        self.is_listening = False
        self.is_speaking = False
        self.last_command_time = datetime.now()
        
        # 🔗 Discord webhook integration
        self.discord_webhook_url = None  # Set this for Discord integration
        
        logger.info("🎤 ChaosGenius Voice Engine initialized!")
    
    def speak(self, text):
        """Text-to-speech with neurodivergent-friendly pacing"""
        if self.is_speaking:
            return
        
        self.is_speaking = True
        logger.info(f"🔊 Speaking: {text}")
        
        # Add emotional context markers for better TTS
        if "error" in text.lower() or "failed" in text.lower():
            text = f"Hmm, {text}. Let's try a different approach."
        elif "success" in text.lower() or "complete" in text.lower():
            text = f"Awesome! {text} Your brain is crushing it!"
        
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
        self.is_speaking = False
    
    def listen_for_wake_word(self):
        """Listen for 'Hey Chaos' wake word"""
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        
        logger.info("🎤 Listening for wake word: 'Hey Chaos'...")
        
        while True:
            try:
                with self.microphone as source:
                    # Listen with timeout for ADHD-friendly responsiveness
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                
                text = self.recognizer.recognize_google(audio).lower()
                
                if "hey chaos" in text or "chaos genius" in text:
                    self.speak("Yes! How can I help your beautiful neurodivergent brain?")
                    self.process_command()
                    
            except sr.WaitTimeoutError:
                pass  # Normal timeout, keep listening
            except sr.UnknownValueError:
                pass  # Couldn't understand, keep listening  
            except Exception as e:
                logger.error(f"Wake word error: {e}")
                time.sleep(1)
    
    def process_command(self):
        """Process voice command after wake word detected"""
        try:
            with self.microphone as source:
                self.speak("I'm listening...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            command_text = self.recognizer.recognize_google(audio).lower()
            logger.info(f"🎯 Command received: {command_text}")
            
            # Log to database
            self.log_voice_activity("command_received", command_text)
            
            # Find matching command
            command_executed = False
            for pattern, function in self.commands.items():
                if pattern in command_text:
                    self.speak(f"Executing {pattern}...")
                    function(command_text)
                    command_executed = True
                    break
            
            if not command_executed:
                self.speak("I didn't catch that command. Try saying it a different way, or say 'help' for available commands.")
                
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't catch that. Your ADHD brain can try again!")
        except sr.RequestError as e:
            self.speak("Voice recognition service error. Switching to offline mode.")
            logger.error(f"Speech recognition error: {e}")
        except Exception as e:
            logger.error(f"Command processing error: {e}")
            self.speak("Something went sideways. Let's try that again!")
    
    # 🧠 FOCUS & ENERGY COMMANDS
    
    def activate_hyperfocus(self, command_text):
        """Activate hyperfocus environment"""
        try:
            # Set focus environment
            self.speak("Activating hyperfocus zone! Optimizing your environment for deep work.")
            
            # Close distracting apps (customize as needed)
            distracting_apps = ["chrome.exe", "firefox.exe", "spotify.exe"]
            for app in distracting_apps:
                try:
                    subprocess.run(f"taskkill /f /im {app}", shell=True, capture_output=True)
                except:
                    pass
            
            # Launch focus tools
            subprocess.Popen(["python", "dashboard_api.py"], cwd=os.getcwd())
            
            # Send to Discord if webhook configured
            if self.discord_webhook_url:
                self.send_discord_notification("🧠 Hyperfocus mode activated! Do not disturb.")
            
            # Log focus session
            self.log_voice_activity("hyperfocus_activated", "Deep work session started")
            
            self.speak("Hyperfocus zone is active! Your neurodivergent superpowers are now engaged. Time to create something amazing!")
            
        except Exception as e:
            logger.error(f"Hyperfocus activation error: {e}")
            self.speak("Hyperfocus activation had a hiccup. But your brain is still awesome!")
    
    def start_focus_timer(self, command_text):
        """Start a focus timer (Pomodoro-style)"""
        # Extract duration from command
        import re
        numbers = re.findall(r'\d+', command_text)
        duration = int(numbers[0]) if numbers else 25  # Default 25 minutes
        
        self.speak(f"Starting {duration} minute focus session. I'll check on you when it's done!")
        
        # Send timer info to dashboard
        try:
            payload = {"type": "focus_timer", "duration": duration, "source": "voice"}
            requests.post(f"{self.dashboard_url}/api/start-focus-timer", json=payload, timeout=5)
        except:
            pass
        
        # Start timer in background
        threading.Thread(target=self.focus_timer_background, args=(duration,)).start()
        
        self.log_voice_activity("focus_timer_started", f"{duration} minutes")
    
    def focus_timer_background(self, duration_minutes):
        """Background focus timer"""
        time.sleep(duration_minutes * 60)  # Convert to seconds
        self.speak(f"Focus session complete! Your {duration_minutes} minutes of neurodivergent genius time is done. Time for a well-deserved break!")
        
        # Optional: Send completion notification to Discord
        if self.discord_webhook_url:
            self.send_discord_notification(f"🎯 {duration_minutes}-minute focus session completed! Great work!")
    
    def check_energy_status(self, command_text):
        """Check current energy and dopamine levels"""
        try:
            response = requests.get(f"{self.dashboard_url}/api/empire-status", timeout=5)
            if response.status_code == 200:
                data = response.json()
                empire_health = data.get('empire_health', 'Unknown')
                self.speak(f"Your empire health is {empire_health}. Your neurodivergent brain is {empire_health.lower()} and ready for action!")
            else:
                self.speak("Energy check complete! You're running on pure neurodivergent determination right now!")
        except:
            self.speak("Energy systems are offline, but your brain energy feels strong! Trust your ADHD intuition!")
        
        self.log_voice_activity("energy_check", "Status requested")
    
    def trigger_dopamine_boost(self, command_text):
        """Trigger immediate dopamine boost activities"""
        boost_activities = [
            "Quick win achieved! You just activated voice control like a tech wizard!",
            "Dopamine boost incoming! Remember: your ADHD brain is literally wired for innovation!",
            "Instant gratification unlocked! Your hyperfocus abilities are a genuine superpower!",
            "Brain chemistry optimized! You're exactly the right kind of weird for world-changing success!",
            "Neurotransmitter party activated! Your scattered thoughts create connections others miss!"
        ]
        
        import random
        boost_message = random.choice(boost_activities)
        self.speak(boost_message)
        
        # Send encouraging message to Discord
        if self.discord_webhook_url:
            self.send_discord_notification(f"💎 Dopamine boost delivered! {boost_message}")
        
        self.log_voice_activity("dopamine_boost", "Positive reinforcement delivered")
    
    # 🚀 PRODUCTIVITY COMMANDS
    
    def voice_create_product(self, command_text):
        """Create product via voice description"""
        self.speak("Tell me your product idea! I'll capture every brilliant detail.")
        
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=30)
            
            product_description = self.recognizer.recognize_google(audio)
            
            # Send to dashboard API
            payload = {
                "name": product_description[:50],
                "description": product_description,
                "source": "voice_command",
                "energy_level": "high"
            }
            
            response = requests.post(f"{self.dashboard_url}/api/create-product", json=payload, timeout=5)
            
            if response.status_code == 200:
                self.speak(f"Product idea captured! Your concept about {product_description[:30]} is now in the empire pipeline!")
            else:
                # Fallback to local storage
                self.save_product_locally(product_description)
                
        except Exception as e:
            logger.error(f"Product creation error: {e}")
            self.speak("Product capture had a glitch, but your idea is still brilliant! Try the dashboard manually.")
    
    def capture_brain_dump(self, command_text):
        """Capture unstructured thoughts and ideas"""
        self.speak("Brain dump mode activated! Let all your thoughts flow - I'll organize the beautiful chaos!")
        
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=15, phrase_time_limit=60)
            
            brain_dump = self.recognizer.recognize_google(audio)
            
            # Save to brain dump file
            dump_dir = Path("temp/brain_dumps")
            dump_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            dump_file = dump_dir / f"voice_dump_{timestamp}.txt"
            
            with open(dump_file, 'w', encoding='utf-8') as f:
                f.write(f"Voice Brain Dump - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 50 + "\n\n")
                f.write(brain_dump)
                f.write("\n\n--- PROCESSING NOTES ---\n")
                f.write("Add categories, action items, and next steps here.\n")
            
            self.speak("Brain dump captured! Your thoughts are safely stored and ready for your genius brain to organize later.")
            
            # Send to Discord for community engagement
            if self.discord_webhook_url:
                self.send_discord_notification(f"🧠 New brain dump captured via voice! File: {dump_file.name}")
            
            self.log_voice_activity("brain_dump", f"Captured: {len(brain_dump)} characters")
            
        except Exception as e:
            logger.error(f"Brain dump error: {e}")
            self.speak("Brain dump had a hiccup, but your thoughts are still valid! Try writing them down for now.")
    
    def launch_ai_squad(self, command_text):
        """Launch AI Squad via voice command"""
        self.speak("AI Squad deployment initiated! Your digital army is assembling!")
        
        try:
            payload = {
                "type": "business_creator",
                "energy_level": "high", 
                "source": "voice_command"
            }
            
            response = requests.post(f"{self.dashboard_url}/api/launch-ai-squad", json=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.speak("AI Squad deployed successfully! Your neurodivergent empire is expanding!")
            else:
                self.speak("AI Squad is currently offline, but your human genius is still online and ready!")
        except:
            self.speak("AI Squad deployment had network issues, but your creativity doesn't need wifi to be amazing!")
        
        self.log_voice_activity("ai_squad_launched", "Voice deployment successful")
    
    # 🎛️ SYSTEM CONTROLS
    
    def open_dashboard(self, command_text):
        """Open ChaosGenius dashboard"""
        try:
            import webbrowser
            webbrowser.open(f"{self.dashboard_url}")
            self.speak("Dashboard opening! Your empire control center is ready for command!")
        except:
            self.speak("Dashboard launch had issues. Try opening localhost 5000 manually.")
        
        self.log_voice_activity("dashboard_opened", "Voice activation")
    
    def activate_discord_mode(self, command_text):
        """Activate Discord community mode"""
        try:
            # Check if Discord bot is running
            response = requests.get(f"{self.dashboard_url}/api/discord-status", timeout=5)
            if response.status_code == 200:
                self.speak("Discord community mode activated! Your neurodivergent tribe awaits!")
            else:
                self.speak("Discord bot is currently offline. But your community spirit is always online!")
        except:
            self.speak("Discord connection is spotty, but your community building energy is strong!")
        
        self.log_voice_activity("discord_mode", "Community activation")
    
    # 🧘 WELLNESS COMMANDS
    
    def guided_breathing(self, command_text):
        """Lead guided breathing exercise"""
        self.speak("Let's reset your nervous system! Follow my breathing guide.")
        
        for i in range(3):  # 3 cycles
            self.speak("Breathe in slowly... 2... 3... 4...")
            time.sleep(4)
            self.speak("Hold... 2... 3... 4...")
            time.sleep(4)  
            self.speak("Breathe out slowly... 2... 3... 4... 5... 6...")
            time.sleep(6)
        
        self.speak("Breathing exercise complete! Your ADHD brain just got a reset. You're ready to conquer the world!")
        self.log_voice_activity("breathing_exercise", "3 cycles completed")
    
    def neurodivergent_motivation(self, command_text):
        """Deliver neurodivergent-specific motivation"""
        motivations = [
            "Your ADHD brain is literally designed for innovation! Those rapid connections others call scattered are actually genius-level pattern recognition!",
            "Hyperfocus isn't a bug, it's a feature! When you find your zone, you can accomplish what takes others weeks!",
            "Your weird is your superpower! The things that make you different are exactly what the world needs!",
            "Neurodivergent minds built the internet, revolutionized art, and changed science! You're part of that legacy!",
            "Your brain doesn't work like everyone else's - and that's exactly why you'll succeed where others can't!"
        ]
        
        import random
        motivation = random.choice(motivations)
        self.speak(motivation)
        
        # Send to Discord for community boost
        if self.discord_webhook_url:
            self.send_discord_notification(f"🌟 Motivation boost delivered: {motivation}")
        
        self.log_voice_activity("motivation_boost", "Neurodivergent affirmation")
    
    # 🔧 UTILITY FUNCTIONS
    
    def log_voice_activity(self, action, details):
        """Log voice command activity"""
        try:
            conn = sqlite3.connect('chaosgenius.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO activity_log (action, type, details, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (f"Voice: {action}", "voice_control", details, datetime.now().isoformat()))
            conn.commit()
            conn.close()
            
            logger.info(f"Voice activity logged: {action} - {details}")
            
        except Exception as e:
            logger.error(f"Voice logging error: {e}")
    
    def send_discord_notification(self, message):
        """Send notification to Discord webhook"""
        if not self.discord_webhook_url:
            return
        
        try:
            payload = {"content": message}
            requests.post(self.discord_webhook_url, json=payload, timeout=5)
        except Exception as e:
            logger.error(f"Discord notification error: {e}")
    
    def save_product_locally(self, description):
        """Save product idea locally when API is unavailable"""
        try:
            products_dir = Path("production_assets/product_ideas")
            products_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            product_file = products_dir / f"voice_product_{timestamp}.txt"
            
            with open(product_file, 'w', encoding='utf-8') as f:
                f.write(f"VOICE PRODUCT IDEA - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Description: {description}\n\n")
                f.write("--- DEVELOPMENT NOTES ---\n")
                f.write("Add features, target market, and implementation notes here.\n")
            
            self.speak(f"Product saved locally! File created: {product_file.name}")
            
        except Exception as e:
            logger.error(f"Local product save error: {e}")
    
    def start_listening(self):
        """Start the voice control system"""
        self.speak("ChaosGenius Voice Control is online! Say 'Hey Chaos' to activate commands!")
        self.is_listening = True
        
        # Start listening in a separate thread
        listening_thread = threading.Thread(target=self.listen_for_wake_word)
        listening_thread.daemon = True
        listening_thread.start()
        
        logger.info("🎤 Voice control system started!")
        return listening_thread

def main():
    """Main voice control execution"""
    try:
        # Initialize voice engine
        voice_engine = ChaosGeniusVoiceEngine()
        
        # Start listening
        listening_thread = voice_engine.start_listening()
        
        print("🎤 ChaosGenius Voice Control Active!")
        print("Say 'Hey Chaos' followed by your command")
        print("Available commands:")
        for command in voice_engine.commands.keys():
            print(f"  - {command}")
        print("\nPress Ctrl+C to stop")
        
        # Keep main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🎤 Voice control stopped!")
            voice_engine.is_listening = False
            
    except Exception as e:
        print(f"Voice control error: {e}")
        print("Make sure you have installed: pip install speechrecognition pyttsx3 pyaudio")

if __name__ == "__main__":
    main()