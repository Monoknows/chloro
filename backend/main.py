import sys
import win32gui
import win32con
from brain import ask_chloro
from ears import listen
from voice import speak

# Identify your frontend's unique identification title (Must match Step 3)
CHLORO_UI_TITLE = "CHLORO_CORE_MATRIX_v1.0"

def terminate_chloro_system():
    """
    Locates the floating UI core window via native OS calls
    and forces a direct application exit on both layers.
    """
    print("[CHLORO]: Total system shutdown sequence initialized, Sir...")
    
    speak("Goodbye! Initiating shutdown sequence. Have a great day!")

    # Search the active Windows application table for Chloro's unique frontend title
    hwnd = win32gui.FindWindow(None, CHLORO_UI_TITLE)
    
    if hwnd:
        # Send a native Windows 'WM_CLOSE' message to simulate pressing 'X' (ALT+F4)
        # This will exit the mainloop() inside app.py instantly.
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
        print("[CHLORO]: Frontend Core successfully terminated.")
    else:
        # The UI was either not running or the title did not match.
        print("[CHLORO]: Frontend window was not detected active.")

    print("[CHLORO]: Going offline. Goodbye, Sir.")
    # Closes this backend terminal loop process completely
    sys.exit(0)

def main():
    # Initial startup greetings
    speak("Good day, Sir. CHLORO is online. How can I help?")

    # Dedicated main orchestrator loop
    while True:
        query = listen()
        if not query:
            continue
            
        # Phrase matching logic normalized to lowercase
        if query.lower() in ["exit", "quit", "goodbye"]:
            # optional: speak("Total system shutdown initialized.")
            
            # Execute the full coordinated application suite termination
            terminate_chloro_system()
            break # Loop broken, will exit after function returns
            
        ai_response = ask_chloro(query)
        print(f"CHLORO: {ai_response}")
        speak(ai_response)

if __name__ == "__main__":
    main()