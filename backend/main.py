import os
import sys
import time
import threading
import queue
import win32gui
import win32con
from datetime import datetime
from brain import ask_chloro
from ears import listen
from voice import speak
from eye import vision
from google_agent import get_google_services, check_job_emails

CHLORO_UI_CLASS = "CHLORO"
CHLORO_UI_TITLE = "CHLORO"

TARGET_SPREADSHEET_ID = "1sqI20dH8f9WoM2XpmUNeVB3DjSCotP26XtNy98B0lSw"

text_input_queue = queue.Queue()
input_ready_event = threading.Event()

system_state = {
    "unread_job_alerts": 0,
    "active_interviews": [
        "Junior Full Stack Developer at Mayan Solutions",
        "Consultant, Associate - US Shift at Infor"
    ],
    "pending_follow_ups": 0,
    "last_sync_time": "Never"
}

state_lock = threading.Lock()


def terminate_chloro_system():
    print("\n[SHUTDOWN]: Terminating Chloro system and cleaning up resources...")

    try:
        speak("Shutting down. Goodbye!")
    except Exception:
        pass

    try:
        hwnd = win32gui.FindWindow(None, CHLORO_UI_TITLE)

        if hwnd:
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
    except Exception as e:
        print(f"[SHUTDOWN WARNING]: {e}")

    sys.exit(0)


def console_input_thread():
    """Captures keyboard input and signals instantly."""
    while True:
        try:
            user_text = input().strip()

            if user_text:
                text_input_queue.put(user_text)
                input_ready_event.set()

        except Exception as e:
            print(f"[INPUT THREAD ERROR]: {e}")
            break


def email_monitor_worker():
    """Background scanner updating Gmail telemetry every 60 seconds."""

    print("[SYSTEM]: Launching background Google Mail & Sheets agent...")

    try:
        gmail_srv, sheets_srv = get_google_services()

    except Exception as e:
        print(f"[SYSTEM ERROR]: Failed initializing Google services: {e}")
        return

    while True:
        try:
            notifications = check_job_emails(gmail_srv)

            with state_lock:
                system_state["unread_job_alerts"] = len(notifications)
                system_state["last_sync_time"] = time.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

            for alert in notifications:
                sender = alert.get("sender", "Unknown Sender")

                announcement = (
                    f"Notice. You received a job alert from {sender}."
                )

                print(f"[CHLORO NOTIFICATION]: {announcement}")

                try:
                    speak(announcement)
                except Exception:
                    pass

        except Exception as e:
            print(f"[BACKGROUND SYNC WARN]: {e}")

        time.sleep(60)
        
def greeting():
    """Initial greeting message."""
    current_time = datetime.now()
    try:
        if(current_time.hour < 12):
            speak("Good morning! How can I assist you today?")
        elif(current_time.hour < 18):
            speak("Good afternoon! How can I assist you today?")
        else:
            speak("Good evening! How can I assist you today?")
    except Exception as e:
        print(f"[GREETING ERROR]: {e}")


def main():
    print("====================================")
    print("CHLORO HYBRID CORE INTERFACE")
    print("====================================")
    print("[SYSTEM]: Microphone streaming active...")
    print("[SYSTEM]: Console keyboard tracking active...")
    print("[SYSTEM]: Gmail background scanner running...")
    print("Speak naturally OR type below at any time.")

    threading.Thread(
        target=console_input_thread,
        daemon=True
    ).start()

    threading.Thread(
        target=email_monitor_worker,
        daemon=True
    ).start()

    # 👁️ Spawn Chloro's vision function concurrently
    threading.Thread(
        target=vision,
        daemon=True
    ).start()

    greeting()

    while True:
        input_ready_event.wait(timeout=1)

        query = None

        # Priority: Keyboard input
        if not text_input_queue.empty():
            query = text_input_queue.get()

            print(f"\n[KEYBOARD INPUT]: {query}")

            if text_input_queue.empty():
                input_ready_event.clear()

        else:
            try:
                query = listen()

                if query:
                    print(f"\n[VOCAL INPUT]: {query}")

            except Exception as e:
                print(f"[MIC ERROR]: {e}")
                query = None

        if not query:
            continue

        query = str(query).strip()

        if not query:
            continue

        query_lower = query.lower()

        if query_lower in [
            "exit",
            "quit",
            "goodbye",
            "shutdown",
            "stop"
        ]:
            terminate_chloro_system()
            break

        with state_lock:
            context_header = (
                f"[SYSTEM METRICS - "
                f"Unread Job Emails: {system_state['unread_job_alerts']}, "
                f"Active Track Sequences: "
                f"{', '.join(system_state['active_interviews'])}, "
                f"Last Sync: {system_state['last_sync_time']}] "
            )

        full_context_query = context_header + query

        try:
            ai_response = ask_chloro(full_context_query)

            if not ai_response:
                ai_response = (
                    "I processed your request but did not receive a response."
                )

            print(f"\nCHLORO: {ai_response}")

            try:
                speak(ai_response)
            except Exception as e:
                print(f"[VOICE ERROR]: {e}")

        except Exception as e:
            print(f"[AI ERROR]: {e}")

            try:
                speak("I encountered an internal error.")
            except Exception:
                pass


if __name__ == "__main__":
    main()