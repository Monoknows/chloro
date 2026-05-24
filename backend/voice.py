import os
import wave
import tempfile
import pygame
from piper import PiperVoice

# Dynamically calculate the absolute path relative to this file's location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "piper_voices", "en_US-amy-medium.onnx")

# Load the local neural model once when the module is imported
try:
    if os.path.exists(MODEL_PATH):
        voice = PiperVoice.load(MODEL_PATH)
    else:
        print(f"[Voice Error] Piper model files missing from: {MODEL_PATH}")
        voice = None
except Exception as e:
    print(f"[Voice Error] Failed to initialize Piper model: {e}")
    voice = None

def speak(text):
    if not text.strip() or not voice:
        return
        
    # Create a safe temporary file path location
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
        temp_path = temp_wav.name
        
    try:
        # Use Python's built-in wave module to establish the correct stream target
        with wave.open(temp_path, "wb") as wav_file:
            # Crucial Fix: Use synthesize_wav to write structural audio headers properly
            voice.synthesize_wav(text, wav_file)
            
        # Initialize playback at Amy's native sample rate (usually 22050Hz)
        pygame.mixer.init(frequency=voice.config.sample_rate)
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()
        
        # Hold execution until audio frame processing finishes
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
        pygame.mixer.quit()
        
    except Exception as e:
        print(f"[Voice Error] Piper TTS execution failed: {e}")
        
    finally:
        # Unlink the temporary file track immediately off the storage drive
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        except:
            pass