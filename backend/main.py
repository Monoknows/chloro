import os
import time
import threading
import queue
import win32gui
import win32con

from brain import ask_chloro
from ears import listen
from voice import speak

from google_agent import get_google_services, check_job_emails

CHLORO_UI_CLASS = "CHLORO"
TARGET_SPREADSHEET_ID = "1sqI20dH8f9WoM2XpmUNeVB3DjSCotP26XtNy98B0lSw"

text_input_queue = queue.Queue()
input_ready_event = threading.Event()

system_state = {
    "unread_job_alerts": 0,
    "active_interviews": ["Junior Full Stack Developer at Mayan Solutions", "Consultant, Associate - US Shift at Infor"],
    "pending_follow_ups": 0,
    "last_sync_time": "Never"
}
state_lock = threading.Lock()


def terminate_chloro_system():
    print("\n[SHUTDOWN]: Terminating Chloro system and cleaning up resources...")
    speak("Shutting down. Goodbye!")
    hwnd = win32gui.FindWindow(None, CHLORO_UI_TITLE)
    if hwnd:
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
    sys.exit(0)

def console_input_thread():
    """Captures the keyboard input and signals instantly"""
    while True:
        try:
            user_text = input().strip()
            if user_text:
                text_input_queue.put(user_text)
                input_ready_event.set()
        except Exception as e:
            break 
            
def email_monitor_worker():
    """Background scanner updating the core system telemetry matrix every 60 seconds."""
    print("[SYSTEM]: Launching background Google Mail & Sheets agent...")
    try:
        gmail_srv, sheets_srv = get_google_services()
    except Exception as e:
        print(f"[SYSTEM ERROR]: Failed initializing Google clearance: {e}")
        return

    while True:
        try:
            notifications = check_job_emails(gmail_srv)
            
            with state_lock:
                system_state["unread_job_alerts"] = len(notifications)
                system_state["last_sync_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
            
            for alert in notifications:
                announcement = f"Notice, You recieved a job alert from {alert['sender']}."
                print(f"[CHLORO NOTIFICATION]: {announcement}")
                speak(announcement)
        except Exception as e:
           print(f"\n[BACKGROUND SYNC WARN]: Telemetry loop hiccup: {e}")   
        time.sleep(60)

def main():
    print("CHLORO HYBRID CORE INTERFACE")
    print("[SYSTEM]: Microphone streaming active...")
    print("[SYSTEM]: Console keyboard tracking active...")
    print("[SYSTEM]: Gmail background scanner running...")
    print("Speak naturally OR type below at any time, Sir.")

    threading.Thread(target=console_input_thread, daemon=True).start()
    threading.Thread(target=email_monitor_worker, daemon=True).start()

    speak("Operational.")

    while True:
        input_ready_event.wait(timeout=1)

        query = ""

        if not text_input_queue.empty():
            query = text_input_queue.get()
            print(f"Keyboard Input Detected: {query}")
            input_ready_event.clear()
        else 
            query = listen()
            if query:
                print(f"\n[Vocal Input Received]: {query}")

                if not query:
            continue

        
        query_lower = query.lower()
        if query_lower in ["exit", "quit", "goodbye"]:
            terminate_chloro_system()
            break 

    
        with state_lock:
            context_header = (
                f"[SYSTEM METRICS - Unread Job Emails: {system_state['unread_job_alerts']}, "
                f"Active Track Sequences: {', '.join(system_state['active_interviews'])}, "
                f"Last Sync: {system_state['last_sync_time']}] "
            )
        
        full_context_query = context_header + query

       
        ai_response = ask_chloro(full_context_query)
        print(f"CHLORO: {ai_response}")
        speak(ai_response)


if __name__ == "__main__":
    main()