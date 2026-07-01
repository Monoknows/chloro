import os
import sys
import time
import threading
import queue
import logging
import win32gui
import win32con
from datetime import datetime
from brain import ask_chloro
from ears import listen
from voice import speak
from eye import vision
from google_agent import get_google_services, check_job_emails

# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────
CHLORO_UI_CLASS = "CHLORO"
CHLORO_UI_TITLE = "CHLORO"
TARGET_SPREADSHEET_ID = "1sqI20dH8f9WoM2XpmUNeVB3DjSCotP26XtNy98B0lSw"

EMAIL_SCAN_INTERVAL = 60        # seconds between Gmail scans
MIC_COOLDOWN = 0.5              # seconds to debounce microphone input
MAX_RESPONSE_RETRIES = 2        # how many times to retry a failed AI call
LOG_FILE = "chloro.log"         # log file name in working directory

# ─────────────────────────────────────────────
# LOGGING SETUP
# Logs to both console and a file so you can
# review what Chloro said/did after the fact.
# ─────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
log = logging.getLogger("chloro")

# ─────────────────────────────────────────────
# SHARED STATE
# ─────────────────────────────────────────────
text_input_queue = queue.Queue()
input_ready_event = threading.Event()
shutdown_event = threading.Event()      # NEW: clean shutdown signal for all threads

system_state = {
    "unread_job_alerts": 0,
    "active_interviews": [
        "Junior Full Stack Developer at Mayan Solutions",
        "Consultant, Associate - US Shift at Infor"
    ],
    "pending_follow_ups": 0,
    "last_sync_time": "Never",
    "session_start": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),   # NEW: track session start
    "query_count": 0,                                                  # NEW: track total queries
}

state_lock = threading.Lock()

# ─────────────────────────────────────────────
# CONVERSATION HISTORY
# NEW: Keeps a rolling window of the last N
# exchanges so Chloro has short-term memory
# within a session, even without OpenClaw.
# ─────────────────────────────────────────────
MAX_HISTORY = 10
conversation_history = []
history_lock = threading.Lock()


def add_to_history(role: str, content: str):
    """Append a message to conversation history, trimming oldest if needed."""
    with history_lock:
        conversation_history.append({"role": role, "content": content})
        if len(conversation_history) > MAX_HISTORY * 2:
            # Keep only the last MAX_HISTORY exchanges (user + assistant pairs)
            del conversation_history[:-MAX_HISTORY * 2]


def build_context_query(query: str) -> str:
    """
    Prepends system metrics and recent conversation history to the query
    so the AI has full context for each turn.
    """
    with state_lock:
        context_header = (
            f"[SYSTEM METRICS - "
            f"Unread Job Emails: {system_state['unread_job_alerts']}, "
            f"Active Track Sequences: {', '.join(system_state['active_interviews'])}, "
            f"Last Sync: {system_state['last_sync_time']}, "
            f"Session Queries: {system_state['query_count']}] "
        )

    # NEW: Attach last few exchanges as context prefix
    with history_lock:
        history_snippet = ""
        for msg in conversation_history[-6:]:   # last 3 exchanges
            prefix = "User" if msg["role"] == "user" else "Chloro"
            history_snippet += f"{prefix}: {msg['content']}\n"

    return f"{context_header}\n{history_snippet}User: {query}"


# ─────────────────────────────────────────────
# SHUTDOWN
# ─────────────────────────────────────────────
def terminate_chloro_system():
    """Gracefully shut down all threads and the UI window."""
    log.info("[SHUTDOWN]: Terminating Chloro system and cleaning up resources...")
    shutdown_event.set()    # signal all threads to stop

    try:
        speak("Shutting down. Goodbye!")
    except Exception:
        pass

    try:
        hwnd = win32gui.FindWindow(None, CHLORO_UI_TITLE)
        if hwnd:
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
    except Exception as e:
        log.warning(f"[SHUTDOWN WARNING]: {e}")

    sys.exit(0)


# ─────────────────────────────────────────────
# BUILT-IN COMMANDS
# NEW: Special slash-style commands handled
# before hitting the AI — fast and reliable.
# ─────────────────────────────────────────────
SHUTDOWN_KEYWORDS = {"exit", "quit", "goodbye", "shutdown", "stop"}

def handle_builtin_command(query: str) -> bool:
    """
    Check if query is a built-in command and handle it.
    Returns True if handled (skip AI call), False otherwise.
    """
    q = query.strip().lower()

    # Shutdown
    if q in SHUTDOWN_KEYWORDS:
        terminate_chloro_system()
        return True

    # Status report
    if q in {"status", "system status", "chloro status"}:
        with state_lock:
            msg = (
                f"System status: "
                f"{system_state['unread_job_alerts']} unread job alerts, "
                f"{len(system_state['active_interviews'])} active interview tracks, "
                f"last sync at {system_state['last_sync_time']}, "
                f"{system_state['query_count']} queries this session."
            )
        log.info(f"[BUILTIN]: {msg}")
        speak(msg)
        return True

    # Clear conversation history
    if q in {"clear history", "forget", "reset memory"}:
        with history_lock:
            conversation_history.clear()
        msg = "Conversation history cleared."
        log.info(f"[BUILTIN]: {msg}")
        speak(msg)
        return True

    # Help
    if q in {"help", "commands", "what can you do"}:
        msg = (
            "Built-in commands: status, clear history, help, and exit. "
            "For everything else, just speak or type naturally."
        )
        log.info(f"[BUILTIN]: {msg}")
        speak(msg)
        return True

    return False


# ─────────────────────────────────────────────
# AI RESPONSE WITH RETRY
# NEW: Retries failed AI calls up to
# MAX_RESPONSE_RETRIES times before giving up.
# ─────────────────────────────────────────────
def get_ai_response(full_query: str) -> str:
    """Call ask_chloro with retry logic on failure."""
    last_error = None

    for attempt in range(1, MAX_RESPONSE_RETRIES + 1):
        try:
            response = ask_chloro(full_query)
            if response:
                return response
            log.warning(f"[AI]: Empty response on attempt {attempt}.")
        except Exception as e:
            last_error = e
            log.warning(f"[AI]: Attempt {attempt} failed: {e}")
            time.sleep(1)   # brief pause before retry

    log.error(f"[AI]: All {MAX_RESPONSE_RETRIES} attempts failed. Last error: {last_error}")
    return "I encountered an issue and could not process your request."


# ─────────────────────────────────────────────
# THREADS
# ─────────────────────────────────────────────
def console_input_thread():
    """Captures keyboard input and signals the main loop instantly."""
    while not shutdown_event.is_set():
        try:
            user_text = input().strip()
            if user_text:
                text_input_queue.put(user_text)
                input_ready_event.set()
        except EOFError:
            break
        except Exception as e:
            log.error(f"[INPUT THREAD ERROR]: {e}")
            break


def email_monitor_worker():
    """
    Background scanner that checks Gmail every EMAIL_SCAN_INTERVAL seconds.
    Updates system_state with unread job alert counts.
    Now respects shutdown_event for clean exit.
    """
    log.info("[SYSTEM]: Launching background Google Mail & Sheets agent...")

    try:
        gmail_srv, sheets_srv = get_google_services()
    except Exception as e:
        log.error(f"[SYSTEM ERROR]: Failed initializing Google services: {e}")
        return

    while not shutdown_event.is_set():
        try:
            notifications = check_job_emails(gmail_srv)

            with state_lock:
                prev_count = system_state["unread_job_alerts"]
                system_state["unread_job_alerts"] = len(notifications)
                system_state["last_sync_time"] = time.strftime("%Y-%m-%d %H:%M:%S")

            # NEW: Only announce if count increased since last check
            new_alerts = [
                n for n in notifications
            ] if len(notifications) > prev_count else []

            for alert in new_alerts:
                sender = alert.get("sender", "Unknown Sender")
                announcement = f"Notice. You received a job alert from {sender}."
                log.info(f"[CHLORO NOTIFICATION]: {announcement}")
                try:
                    speak(announcement)
                except Exception:
                    pass

        except Exception as e:
            log.warning(f"[BACKGROUND SYNC WARN]: {e}")

        # NEW: Use shutdown_event.wait instead of time.sleep
        # so the thread exits immediately on shutdown
        shutdown_event.wait(timeout=EMAIL_SCAN_INTERVAL)


# ─────────────────────────────────────────────
# GREETING
# ─────────────────────────────────────────────
def greeting():
    """Time-aware greeting on startup."""
    hour = datetime.now().hour
    try:
        if hour < 12:
            speak("Good morning Sir! Chloro is online and ready.")
        elif hour < 18:
            speak("Good afternoon Sir! Chloro is online and ready.")
        else:
            speak("Good evening Sir! Chloro is online and ready.")
    except Exception as e:
        log.error(f"[GREETING ERROR]: {e}")


# ─────────────────────────────────────────────
# MAIN LOOP
# ─────────────────────────────────────────────
def main():
    print("=" * 44)
    print("       CHLORO HYBRID CORE INTERFACE")
    print("=" * 44)
    log.info("[SYSTEM]: Microphone streaming active...")
    log.info("[SYSTEM]: Console keyboard tracking active...")
    log.info("[SYSTEM]: Gmail background scanner running...")
    log.info(f"[SYSTEM]: Session started at {system_state['session_start']}")
    print("Speak naturally OR type below at any time.")
    print("Type 'help' for built-in commands.\n")

    # Start background threads
    threading.Thread(target=console_input_thread, daemon=True).start()
    threading.Thread(target=email_monitor_worker, daemon=True).start()
    threading.Thread(target=vision, daemon=True).start()

    greeting()

    last_mic_time = 0   # NEW: for mic debouncing

    while not shutdown_event.is_set():
        input_ready_event.wait(timeout=1)

        query = None

        # Priority 1: Keyboard input
        if not text_input_queue.empty():
            query = text_input_queue.get()
            log.info(f"[KEYBOARD INPUT]: {query}")
            if text_input_queue.empty():
                input_ready_event.clear()

        else:
            # NEW: Debounce mic — don't poll faster than MIC_COOLDOWN
            now = time.time()
            if now - last_mic_time < MIC_COOLDOWN:
                continue

            try:
                query = listen()
                if query:
                    last_mic_time = time.time()
                    log.info(f"[VOCAL INPUT]: {query}")
            except Exception as e:
                log.error(f"[MIC ERROR]: {e}")
                query = None

        if not query or not str(query).strip():
            continue

        query = str(query).strip()

        # Check built-in commands first (fast path, no AI needed)
        if handle_builtin_command(query):
            continue

        # Update query counter
        with state_lock:
            system_state["query_count"] += 1

        # Add user message to history
        add_to_history("user", query)

        # Build full context and call AI
        full_context_query = build_context_query(query)

        try:
            ai_response = get_ai_response(full_context_query)

            # Add AI response to history
            add_to_history("assistant", ai_response)

            log.info(f"CHLORO: {ai_response}")
            print(f"\nCHLORO: {ai_response}")

            try:
                speak(ai_response)
            except Exception as e:
                log.error(f"[VOICE ERROR]: {e}")

        except Exception as e:
            log.error(f"[AI ERROR]: {e}")
            try:
                speak("I encountered an internal error.")
            except Exception:
                pass


if __name__ == "__main__":
    main()