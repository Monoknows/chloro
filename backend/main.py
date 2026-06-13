import sys
import time
import threading
import queue
import win32gui
import win32con

# Main system processing pipelines
from brain import ask_chloro
from ears import listen
from voice import speak

# Background automated worker assets
from google_agent import get_google_services, check_job_emails, update_spreadsheet

# Identify your frontend's unique identification title
CHLORO_UI_TITLE = "CHLORO_CORE_MATRIX_v1.0"

# Target Google Spreadsheet ID for logging job applications
TARGET_SPREADSHEET_ID = "YOUR_GOOGLE_SHEET_LONG_ID_STRING"

# Thread-safe container to hold incoming console text inputs
text_input_queue = queue.Queue()


def terminate_chloro_system():
    """
    Locates the floating UI core window via native OS calls
    and forces a direct application exit on both layers.
    """
    print("\n[CHLORO]: Total system shutdown sequence initialized, Sir...")
    speak("Goodbye! Initiating shutdown sequence. Have a great day!")

    # Search the active Windows application table for Chloro's unique frontend title
    hwnd = win32gui.FindWindow(None, CHLORO_UI_TITLE)
    
    if hwnd:
        # Send a native Windows 'WM_CLOSE' message to simulate pressing 'X' (ALT+F4)
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
        print("[CHLORO]: Frontend Core successfully terminated.")
    else:
        print("[CHLORO]: Frontend window was not detected active.")

    print("[CHLORO]: Going offline. Goodbye, Sir.")
    sys.exit(0)


def console_input_thread():
    """Runs concurrently in the background to capture keyboard input without freezing the mic."""
    while True:
        try:
            user_text = input().strip()
            if user_text:
                text_input_queue.put(user_text)
        except Exception:
            break


def email_monitor_worker():
    """Runs continuously in the background, checking for new job alert notifications every 60 seconds."""
    print("[SYSTEM]: Launching background Google Mail & Sheets agent...")
    try:
        gmail_srv, sheets_srv = get_google_services()
    except Exception as e:
        print(f"[SYSTEM ERROR]: Failed initializing Google clearance: {e}")
        return

    while True:
        # Scan for unread items
        notifications = check_job_emails(gmail_srv)
        
        for alert in notifications:
            announcement = f"Notice, Sir. You received a job-related email from {alert['sender']}. Subject line: {alert['subject']}."
            print(f"\n📢 [CHLORO NOTIFICATION]: {announcement}")
            speak(announcement)
            
            # OPTIONAL: Automatically log to Google Sheets when an alert triggers
            # update_spreadsheet(sheets_srv, TARGET_SPREADSHEET_ID, "Extracted Company Name", "Extracted Role", "Reviewing Response")
            
        # Rest the scanner thread loop for 1 minute before hitting the API endpoints again
        time.sleep(60)


def main():
    print("==================================================")
    print("         CHLORO HYBRID CORE INTERFACE             ")
    print("==================================================")
    print("[SYSTEM]: Microphone streaming active...")
    print("[SYSTEM]: Console keyboard tracking active...")
    print("[SYSTEM]: Gmail background scanner running...")
    print("👉 Speak naturally OR type below at any time, Sir.")
    print("==================================================")
    
    # ─── THREAD INITIALIZATIONS ───
    # Spin up the concurrent console keyboard text listener
    input_worker = threading.Thread(target=console_input_thread, daemon=True)
    input_worker.start()

    # Spin up the concurrent Google Email background monitor
    bg_monitor = threading.Thread(target=email_monitor_worker, daemon=True)
    bg_monitor.start()

    # Initial system boot voice greeting
    speak("Good day, Sir. CHLORO dual matrix with workspace telemetry is fully operational.")

    # ─── MAIN ORCHESTRATOR LOOP ───
    while True:
        query = ""

        # Check for keyboard console input first
        if not text_input_queue.empty():
            query = text_input_queue.get()
            print(f"\n[Keyboard Input Received]: {query}")

        # If no text input is waiting, stream mic audio
        else:
            query = listen()
            if query:
                print(f"\n[Vocal Input Received]: {query}")

        # If neither path returned anything, continue looping
        if not query:
            continue

        # Phrase matching logic normalized to lowercase for system controls
        if query.lower() in ["exit", "quit", "goodbye"]:
            print("CHLORO: Understood, Sir. Shutting down systems.")
            terminate_chloro_system()
            break 

        # Forward query to the core AI engine
        ai_response = ask_chloro(query)
        print(f"CHLORO: {ai_response}")
        speak(ai_response)


if __name__ == "__main__":
    main()