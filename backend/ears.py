import speech_recognition as sr
import queue

# Thread-safe queue to securely hold recognized speech strings without dropping frames
voice_queue = queue.Queue()

recognizer = sr.Recognizer()
microphone = sr.Microphone()
_bg_listener_handle = None


def _bg_callback(recognizer, audio):
    """Callback execution loop fired on an isolated thread whenever audio clears ambient thresholds."""
    try:
        # Convert captured audio chunks to text via the underlying OpenClaw mapping
        text = recognizer.recognize_google(audio).strip()
        if text:
            voice_queue.put(text)
    except sr.UnknownValueError:
        pass  # Omit raw ambient environment room noise
    except sr.RequestError as e:
        print(f"\n⚠️ [EARS AUDIO SERVICE ERROR]: {e}")


def init_ears():
    """Warms up audio target thresholds and binds the background non-blocking listener."""
    global _bg_listener_handle
    if _bg_listener_handle is None:
        try:
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
            # Spawn the long-running independent listening loop
            _bg_listener_handle = recognizer.listen_in_background(microphone, _bg_callback)
        except Exception as e:
            print(f"\n❌ [EARS INIT ERROR]: Failed to latch hardware audio stream: {e}")


def listen():
    """
    Exposes a unified drop-in hook for main.py.
    Checks the background voice queue cleanly with instantaneous execution.
    """
    # Ensure the audio listener thread engine is warmed up and alive
    init_ears()
    
    try:
        # Poll the queue. If empty, return None immediately to prevent blocking keyboard input.
        return voice_queue.get_nowait()
    except queue.Empty:
        return None