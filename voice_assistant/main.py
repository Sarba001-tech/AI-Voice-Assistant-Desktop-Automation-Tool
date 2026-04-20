import speech_recognition as sr
import pyttsx3
import whisper
import tempfile
import numpy as np
import torch
import warnings
import os
import random
import time
from commands import execute_command
import sys

# Suppress warnings
warnings.filterwarnings("ignore")

class VoiceAssistantCore:
    def __init__(self, cli_mode=False):
        self.cli_mode = cli_mode
        self.engine = None
        self.model = None
        self.recognizer = None
        self.mic = None
        self.initialize_tts()
        
        if not self.cli_mode:
            self.initialize_stt()
            self.initialize_microphone()
        else:
            print("⌨️ CLI Mode Activated: Voice recognition disabled.")
        
    def initialize_tts(self):
        """Initialize Text-to-Speech engine"""
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty("rate", 170)
            
            # Configure voice
            voices = self.engine.getProperty('voices')
            
            # Try to find natural-sounding voices
            preferred_voices = []
            
            # Windows voices
            if sys.platform == 'win32':
                preferred_voices = [
                    v for v in voices 
                    if any(name in v.name.lower() for name in ['zira', 'david', 'mark', 'hazel'])
                ]
            
            # Linux/Mac voices
            elif sys.platform in ['linux', 'darwin']:
                preferred_voices = [
                    v for v in voices 
                    if any(name in v.name.lower() for name in ['samantha', 'alex', 'daniel', 'karen'])
                ]
            
            if preferred_voices:
                self.engine.setProperty('voice', preferred_voices[0].id)
            elif len(voices) > 0:
                self.engine.setProperty('voice', voices[0].id)
            
            print(f"✅ TTS initialized with: {self.engine.getProperty('voice')}")
            
        except Exception as e:
            print(f"❌ Error initializing TTS: {e}")
            self.speak_error("Failed to initialize speech engine")
            exit(1)
    
    def initialize_stt(self):
        """Initialize Speech-to-Text model"""
        print("🔧 Loading speech recognition model...")
        try:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"📊 Using device: {device}")
            
            # Try to load Whisper model
            self.model = whisper.load_model("base", device=device)
            print("✅ Speech recognition model loaded")
            
        except Exception as e:
            print(f"❌ Error loading speech model: {e}")
            self.speak_error("Failed to load voice recognition")
            exit(1)
    
    def initialize_microphone(self):
        """Initialize microphone"""
        try:
            self.recognizer = sr.Recognizer()
            
            # Optimize recognition settings
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.energy_threshold = 400
            self.recognizer.dynamic_energy_adjustment_damping = 0.15
            self.recognizer.pause_threshold = 1.0
            self.recognizer.phrase_threshold = 0.3
            self.recognizer.non_speaking_duration = 0.5
            
            # List available microphones
            mic_list = sr.Microphone.list_microphone_names()
            print(f"\n🎤 Found {len(mic_list)} audio devices:")
            
            # Auto-select best microphone
            mic_index = self.select_microphone(mic_list)
            
            if mic_index is not None:
                self.mic = sr.Microphone(device_index=mic_index)
                print(f"✅ Selected: {mic_list[mic_index]}")
            else:
                print("⚠️ Using default microphone")
                self.mic = sr.Microphone()
            
            print("🎤 Microphone ready")
            
        except Exception as e:
            print(f"❌ Error initializing microphone: {e}")
            self.speak_error("Failed to initialize microphone")
            exit(1)
    
    def select_microphone(self, mic_list):
        """Select the best available microphone"""
        # Priority keywords for microphone selection
        priority_keywords = [
            'microphone', 'mic', 'input', 'recording',
            'usb', 'external', 'headset', 'headphone'
        ]
        
        for i, name in enumerate(mic_list):
            name_lower = name.lower()
            
            # Check for priority keywords
            for keyword in priority_keywords:
                if keyword in name_lower:
                    return i
        
        # Fallback: return first available if any
        return 0 if len(mic_list) > 0 else None
    
    def speak(self, text, rate=None):
        """Speak text with emotion detection and rate adjustment"""
        print(f"\n{'='*60}")
        print(f"🤖 ASSISTANT: {text}")
        print(f"{'='*60}")
        
        try:
            # Save current rate
            current_rate = self.engine.getProperty('rate')
            
            # Adjust rate based on content
            if rate is None:
                # Auto-adjust based on text length and content
                text_length = len(text)
                if text_length > 200:
                    rate = 160  # Slightly slower for long responses
                elif "error" in text.lower() or "failed" in text.lower():
                    rate = 155  # Slower for error messages
                elif "warning" in text.lower() or "caution" in text.lower():
                    rate = 165  # Medium for warnings
                else:
                    rate = 170  # Normal speed
            
            self.engine.setProperty('rate', rate)
            
            # Add slight pauses for better comprehension
            if len(text) > 100:
                # Insert pauses at natural breakpoints
                sentences = text.split('. ')
                for i, sentence in enumerate(sentences):
                    if sentence.strip():
                        self.engine.say(sentence.strip() + ('.' if not sentence.endswith('.') else ''))
                        if i < len(sentences) - 1:
                            self.engine.runAndWait()
                            time.sleep(0.1)
            else:
                self.engine.say(text)          
            
            self.engine.runAndWait()
            
            # Restore original ra
            self.engine.setProperty('rate', current_rate)
            
        except Exception as e:
            print(f"❌ Speech error: {e}")
    
    def speak_error(self, message):
        """Speak error message with appropriate tone"""
        error_responses = [
            f"I encountered an issue: {message}",
            f"Sorry, there was a problem: {message}",
            f"Unable to proceed: {message}"
        ]
        self.speak(random.choice(error_responses), rate=160)
    
    def listen_for_command(self):
        """Listen for voice command with enhanced processing"""
        with self.mic as source:
            try:
                print("\n" + "🔈"*20)
                print("🎧 LISTENING... (Speak your command)")
                print("🔈"*20 + "\n")
                
                # Adjust for ambient noise with longer calibration
                print("🔧 Calibrating microphone...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1.0)
                print("✅ Ready")
                
                # Listen with longer timeout for natural speech
                audio = self.recognizer.listen(
                    source,
                    timeout=8,
                    phrase_time_limit=10
                )
                
                print("🔍 Processing audio...")
                
                # Try multiple recognition methods
                text = self.recognize_audio(audio)
                
                if text:
                    print(f"📝 Recognized: '{text}'")
                    return text
                else:
                    print("❌ No speech detected or understood")
                    return ""
                    
            except sr.WaitTimeoutError:
                print("⏰ No speech detected within timeout")
                return ""
            except sr.RequestError as e:
                print(f"❌ API error: {e}")
                return ""
            except Exception as e:
                print(f"❌ Listening error: {e}")
                return ""
    
    def recognize_audio(self, audio):
        """Try multiple methods to recognize speech"""
        methods = [
            self.try_google_recognition,
            self.try_whisper_recognition
        ]
        
        for method in methods:
            try:
                text = method(audio)
                if text and len(text.strip()) > 2:
                    return text.strip()
            except:
                continue
        
        return ""
    
    def try_google_recognition(self, audio):
        """Try Google Speech Recognition"""
        try:
            return self.recognizer.recognize_google(audio, language="en-US")
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return ""
    
    def try_whisper_recognition(self, audio):
        """Try Whisper recognition"""
        try:
            # Save audio to temporary file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                f.write(audio.get_wav_data())
                temp_file = f.name
            
            # Transcribe with Whisper
            result = self.model.transcribe(
                temp_file,
                language="en",
                task="transcribe",
                temperature=0.0,
                best_of=5,
                beam_size=5
            )
            
            # Clean up
            os.unlink(temp_file)
            
            return result["text"].strip()
            
        except Exception:
            return ""
    
    def show_welcome(self):
        """Display welcome message"""
        welcome = """
        ╔══════════════════════════════════════════════════════════╗
        ║                🚀 ADVANCED VOICE ASSISTANT               ║
        ║                ===========================               ║
        ║                                                          ║
        ║  • File & Folder Management                              ║
        ║  • System Monitoring & Control                           ║
        ║  • Network Operations                                    ║
        ║  • Productivity Tools                                    ║
        ║  • Web Browsing & Search                                 ║
        ║  • Media Control                                         ║
        ║  • And much more!                                        ║
        ║                                                          ║
        ║  💡 Say 'help' for complete command list                 ║
        ║  🎯 Try: 'open youtube' or 'system info'                 ║
        ║  🚪 Say 'exit' to quit                                   ║
        ╚══════════════════════════════════════════════════════════╝
        """
        print(welcome)
    
    def run(self):
        """Main assistant loop"""
        self.show_welcome()
        
        # Greeting
        greetings = [
            "Hello! I'm your advanced voice assistant, ready to help!",
            "Assistant activated! I can help with files, system tasks, and more.",
            "Hello there! I'm here to assist you with various computer tasks.",
            "Voice assistant online! How can I be of service today?"
        ]
        
        self.speak(random.choice(greetings))
        
        command_count = 0
        session_start = time.time()
        
        while True:
            try:

                # Listen for command
                command_text = ""
                
                if self.cli_mode:
                    print("\n" + "⌨️"*20)
                    command_text = input("👉 Enter command (or 'exit'): ")
                    print("⌨️"*20 + "\n")
                else:
                    command_text = self.listen_for_command()
                
                if not command_text:
                    if not self.cli_mode and command_count == 0:
                        self.speak("I didn't hear anything. Please try speaking louder or check your microphone.")
                    continue
                
                # Clean and process command
                command_text = command_text.lower().strip()
                command_count += 1
                
                print(f"\n{'🎯'*20}")
                print(f"COMMAND #{command_count}: '{command_text}'")
                print(f"{'🎯'*20}\n")
                
                # Check for exit
                if any(word in command_text for word in ["exit", "quit", "goodbye", "stop", "shutdown"]):
                    session_duration = time.time() - session_start
                    minutes = int(session_duration // 60)
                    seconds = int(session_duration % 60)
                    
                    farewells = [
                        f"Goodbye! I assisted with {command_count} commands in {minutes}m {seconds}s.",
                        f"Shutting down. We processed {command_count} commands together!",
                        f"Assistant signing off. Have a great day!",
                        f"Goodbye! It was nice helping you with {command_count} tasks."
                    ]
                    
                    self.speak(random.choice(farewells))
                    break
                
                # Execute command
                start_time = time.time()
                response = execute_command(command_text)
                execution_time = time.time() - start_time
                
                # Handle exit signal
                if response == "EXIT_ASSISTANT":
                    self.speak("Goodbye!")
                    break
                
                # Speak response
                if response:
                    # Add execution time for long operations
                    if execution_time > 2:
                        response += f"\n⏱️ Command executed in {execution_time:.1f} seconds"
                    
                    self.speak(response)
                else:
                    self.speak("Command executed successfully!")
                
                # Brief pause between commands
                time.sleep(0.5)
                
            except KeyboardInterrupt:
                print("\n\n👋 User interrupted. Exiting...")
                self.speak("Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                self.speak_error("An unexpected error occurred. Let's try again.")

def main():
    """Main entry point"""
    try:
        cli_mode = "--cli" in sys.argv
        assistant = VoiceAssistantCore(cli_mode=cli_mode)
        assistant.run()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        print("Please check your dependencies and try again.")

if __name__ == "__main__":
    main()