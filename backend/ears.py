import speech_recognition as sr
import queue


voice_queue = queue.Queue()

recognizer = sr.Recognizer()
microphone = sr.Microphone()
_bg_listener_handle = None


def _bg_callback(recognizer, audio):
    """Callback execution loop fired on an isolated thread whenever audio clears ambient thresholds."""
    try:
       
        text = recognizer.recognize_google(audio).strip()
        if text:
            voice_queue.put(text)
    except sr.UnknownValueError:
        pass  
    except sr.RequestError as e:
        print(f" [EARS AUDIO SERVICE ERROR]: {e}")


def init_ears():
    """Warms up audio target thresholds and binds the background non-blocking listener."""
    global _bg_listener_handle
    if _bg_listener_handle is None:
        try:
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
            
            _bg_listener_handle = recognizer.listen_in_background(microphone, _bg_callback)
        except Exception as e:
            print(f"\n[EARS INIT ERROR]: Failed to latch hardware audio stream: {e}")


def listen():
    """
    Exposes a unified drop-in hook for main.py.
    Checks the background voice queue cleanly with instantaneous execution.
    """
    
    init_ears()
    
    try:
        return voice_queue.get_nowait()
    except queue.Empty:
        return None