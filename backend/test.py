import time
from datetime import datetime

# Mocking the speak function for test output visibility
def speak(text):
    print(f"🗣️  [AUDIO OUTPUT]: '{text}'")

def test_greeting_logic(simulated_hour):
    """Evaluates greeting routing based on a forced hour input."""
    try:
        if simulated_hour < 12:
            speak("Good morning! How can I assist you today?")
        elif simulated_hour < 18:
            speak("Good afternoon! How can I assist you today?")
        else:
            speak("Good evening! How can I assist you today?")
    except Exception as e:
        print(f"[ERROR]: {e}")

if __name__ == "__main__":
    print("====================================")
    print("    CHLORO GREETING MATRIX TEST     ")
    print("====================================")
    
    # Test 1: Morning Check (e.g., 9:00 AM)
    print("\n[TEST 1] Testing Morning Route (Simulating 09:00)...")
    test_greeting_logic(9)
    
    # Test 2: Afternoon Check (e.g., 3:00 PM / 15:00)
    print("\n[TEST 2] Testing Afternoon Route (Simulating 15:00)...")
    test_greeting_logic(15)
    
    # Test 3: Evening Check (e.g., 8:00 PM / 20:00)
    print("\n[TEST 3] Testing Evening Route (Simulating 20:00)...")
    test_greeting_logic(20)
    
    print("\n====================================")
    print("          DIAGNOSTICS DONE          ")
    print("====================================")